"""Locally-executed, narrowly typed device actions. NOT an OS security sandbox."""
from __future__ import annotations
import os
import json
import hashlib
import pathlib
import platform
import re
import signal
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import webbrowser
from typing import Any
from .contracts import Step
from .vision import VisionError, locate_unique, read_screen, evidence_for_planner
from .android_ui import locate_android, inspect_android_controls, MAX_XML
from .browser import BrowserAdapter
from .vision import normalize

class ActionError(RuntimeError):
    pass

class Executor:
    def __init__(self, workspace: pathlib.Path, *, enable_code_run: bool = False):
        self.workspace = workspace.resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.enable_code_run = enable_code_run
        self.browser: BrowserAdapter | None = None

    def safe_path(self, name: str) -> pathlib.Path:
        p = pathlib.Path(name)
        if p.is_absolute() or not name or '\x00' in name or ':' in name or '\\' in name:
            raise ActionError("File paths must be relative, portable and inside workspace")
        candidate = (self.workspace / p).resolve()
        if not candidate.is_relative_to(self.workspace) or candidate == self.workspace:
            raise ActionError("Path escapes the workspace")
        return candidate

    @staticmethod
    def gui():
        try:
            import pyautogui as gui
            gui.FAILSAFE = True  # Move cursor to upper-left corner for emergency stop
            gui.PAUSE = 0.08
            return gui
        except Exception as exc:
            raise ActionError(f"Desktop GUI unavailable: {type(exc).__name__}") from exc

    def _type(self, text: str) -> str:
        gui = self.gui()
        if text.isascii():
            gui.write(text, interval=0.003)
        else:
            try:
                import pyperclip
                pyperclip.copy(text)
                gui.hotkey("command", "v") if sys.platform == "darwin" else gui.hotkey("ctrl", "v")
            except Exception as exc:
                raise ActionError("Unicode input requires working clipboard support (pyperclip and OS clipboard)") from exc
        return f"Typed {len(text)} characters"

    def _adb_command(self, serial: str | None) -> list[str]:
        adb = shutil.which("adb")
        if not adb:
            raise ActionError("Android platform-tools (adb) not found")
        try:
            devices = subprocess.run([adb, "devices"], capture_output=True, text=True, timeout=8, check=True).stdout
            attached = [line.split()[0] for line in devices.splitlines()[1:] if line.strip().endswith("\tdevice")]
            if serial:
                if serial not in attached:
                    raise ActionError("Specified Android device is not connected and authorized")
            elif len(attached) != 1:
                raise ActionError("Connect exactly one authorized Android device or specify its serial")
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise ActionError(f"ADB unavailable: {type(exc).__name__}") from exc
        return [adb, "-s", serial or attached[0]]

    def _adb(self, serial: str | None, *command: str, output_limit: int = 500) -> str:
        argv = self._adb_command(serial) + list(command)
        try:
            result = subprocess.run(argv, capture_output=True, text=True, timeout=12, check=False)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise ActionError(f"ADB unavailable: {type(exc).__name__}") from exc
        if result.returncode:
            raise ActionError(f"ADB command failed ({result.returncode}): {result.stderr[:180]}")
        if len(result.stdout) > output_limit:
            raise ActionError("ADB output exceeds permitted size")
        return result.stdout or "ADB action completed"

    def _android_xml(self, serial: str | None) -> str:
        # XML is generated from the *current* screen and can contain sensitive UI text.
        self._adb(serial, "shell", "uiautomator", "dump", "/sdcard/window.xml")
        return self._adb(serial, "exec-out", "cat", "/sdcard/window.xml", output_limit=MAX_XML)

    def _android_screenshot(self, serial: str | None) -> str:
        argv = self._adb_command(serial) + ["exec-out", "screencap", "-p"]
        try:
            result = subprocess.run(argv, capture_output=True, timeout=15, check=False)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise ActionError(f"Android screenshot unavailable: {type(exc).__name__}") from exc
        if result.returncode or not result.stdout.startswith(b"\x89PNG\r\n\x1a\n"):
            raise ActionError("Android screenshot was not a successful PNG capture")
        if len(result.stdout) > 16_000_000:
            raise ActionError("Android screenshot exceeds 16 MB")
        destination = self.workspace / "android-screenshot.png"
        fd, temp = tempfile.mkstemp(dir=self.workspace, prefix=".android-capture-")
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(result.stdout)
            os.replace(temp, destination)
        finally:
            if os.path.exists(temp):
                os.unlink(temp)
        return "Captured Android screenshot in workspace/android-screenshot.png"

    def read_screen_evidence(self) -> str:
        """Only call when the operator explicitly requests sharing OCR to a cloud LLM."""
        return evidence_for_planner(read_screen(self.gui()))

    def _desktop_text(self, label: str, *, click: bool = False,
                      expected_window: str | None = None,
                      cancel: threading.Event | None = None) -> str:
        hit = locate_unique(read_screen(self.gui()), label)
        if click:
            # The GUI may change between a potentially slow OCR scan and click.
            # Require a second independent observation at the same position.
            confirmed = locate_unique(read_screen(self.gui()), label)
            if abs(confirmed.center[0] - hit.center[0]) > 8 or abs(confirmed.center[1] - hit.center[1]) > 8:
                raise ActionError("Visible target moved during OCR; refusing stale click")
            # OCR may take seconds; check the target window again immediately
            # before injecting the actual pointer event.
            if expected_window is not None:
                self._assert_window(expected_window)
            if cancel is not None and cancel.is_set():
                raise ActionError("Stopped by user")
            self.gui().click(*hit.center)
            return f"Clicked unique visible text {label!r} at {hit.center} (OCR confidence {hit.confidence:.0f})"
        return f"Verified visible text {label!r} (OCR confidence {hit.confidence:.0f})"

    def _assert_window(self, title: str) -> str:
        """Fail closed if active-window identity is unavailable or changed.

        Only supported where pyautogui exposes getActiveWindow (generally
        Windows). A title alone is NOT an authentication mechanism.
        """
        gui = self.gui()
        getter = getattr(gui, "getActiveWindow", None)
        if not callable(getter):
            raise ActionError("Active-window detection unavailable on this desktop")
        try:
            window = getter()
            actual = getattr(window, "title", None)
        except Exception as exc:
            raise ActionError(f"Active-window detection failed: {type(exc).__name__}") from exc
        if not isinstance(actual, str) or normalize(actual) != normalize(title):
            raise ActionError("Active window does not match the approved window title")
        return "Verified active window title"

    def _wait_text(self, label: str, timeout: int, cancel: threading.Event) -> str:
        end = time.monotonic() + timeout
        while True:
            if cancel.is_set():
                raise ActionError("Stopped by user")
            try:
                return self._desktop_text(label)
            except VisionError as exc:
                if "not found" not in str(exc):
                    raise
            if time.monotonic() >= end:
                raise ActionError(f"Timed out waiting for visible text {label!r}")
            # Interruptible wait; does not block emergency stop for a full sleep.
            cancel.wait(min(0.25, max(0, end - time.monotonic())))

    def _wait_window(self, title: str, timeout: int, cancel: threading.Event) -> str:
        end = time.monotonic() + timeout
        while True:
            if cancel.is_set():
                raise ActionError("Stopped by user")
            try:
                return self._assert_window(title)
            except ActionError as exc:
                # Capability failures cannot be repaired by waiting.
                if "does not match" not in str(exc):
                    raise
            if time.monotonic() >= end:
                raise ActionError("Timed out waiting for approved window")
            cancel.wait(min(0.2, max(0, end - time.monotonic())))

    def _wait_android_text(self, serial: str | None, label: str, timeout: int,
                           cancel: threading.Event) -> str:
        end = time.monotonic() + timeout
        while True:
            if cancel.is_set():
                raise ActionError("Stopped by user")
            try:
                locate_android(self._android_xml(serial), label)
                return f"Verified Android UI text {label!r}"
            except VisionError as exc:
                if "found 0" not in str(exc):
                    raise
            if time.monotonic() >= end:
                raise ActionError(f"Timed out waiting for Android text {label!r}")
            cancel.wait(min(0.2, max(0, end - time.monotonic())))

    def _open_app(self, alias: str) -> str:
        if alias == "browser":
            if not webbrowser.open("about:blank"):
                raise ActionError("No default browser registered")
            return "Opened default browser"
        candidates = {
            "Windows": {"notepad": [["notepad.exe"]], "calculator": [["calc.exe"]]},
            "Darwin": {"notepad": [["open", "-a", "TextEdit"]], "calculator": [["open", "-a", "Calculator"]]},
            "Linux": {"notepad": [["mousepad"], ["gedit"], ["xed"]], "calculator": [["gnome-calculator"], ["kcalc"]]},
        }
        for argv in candidates.get(platform.system(), {}).get(alias, []):
            if shutil.which(argv[0]):
                subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True)
                return f"Opened {alias}"
        raise ActionError(f"No supported installed application for alias: {alias}")

    def _launch_alias(self, alias: str) -> str:
        """Launch only owner-configured app aliases, without a shell interpreter."""
        try:
            config = json.loads(os.getenv("AI_AI_APP_ALLOWLIST_JSON", "{}"))
        except json.JSONDecodeError as exc:
            raise ActionError("Invalid AI_AI_APP_ALLOWLIST_JSON") from exc
        if not isinstance(config, dict) or alias not in config:
            raise ActionError(f"Application alias {alias!r} is not in the owner allowlist")
        args = config[alias]
        if (not isinstance(args, list) or not 1 <= len(args) <= 8 or
            any(not isinstance(v, str) or not v or len(v) > 512 or "\x00" in v for v in args)):
            raise ActionError("Application allowlist entry must be a nonempty argv string array")
        if not shutil.which(args[0]):
            raise ActionError("Configured application executable not available")
        try:
            subprocess.Popen(args, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL, close_fds=True)
        except OSError as exc:
            raise ActionError(f"Application launch failed: {type(exc).__name__}") from exc
        return f"Launched allowed application {alias!r}"

    def _run_code(self, path: str, timeout: int, cancel: threading.Event) -> str:
        if not self.enable_code_run:
            raise ActionError("Code execution disabled. Set AI_AI_ENABLE_CODE_RUN=1 and restart to enable trusted scripts")
        p = self.safe_path(path)
        if p.suffix.lower() != ".py" or not p.is_file():
            raise ActionError("Only existing .py files inside workspace can be executed")
        # An isolated Python interpreter is not a security sandbox. User must trust script source.
        env = {k: v for k,v in os.environ.items() if k in ("PATH", "SYSTEMROOT", "WINDIR", "HOME", "TMP", "TEMP", "LANG", "LC_ALL")}
        with tempfile.TemporaryFile(mode="w+b") as log:
            proc = subprocess.Popen([sys.executable, "-I", "-B", str(p)], cwd=self.workspace,
                                    stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT, env=env,
                                    start_new_session=os.name != "nt",
                                    creationflags=(subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0))
            deadline = time.monotonic() + timeout
            try:
                while proc.poll() is None:
                    if cancel.is_set():
                        raise ActionError("Stopped by user")
                    if time.monotonic() > deadline:
                        raise ActionError("Script execution timed out")
                    time.sleep(0.05)
            finally:
                if proc.poll() is None:
                    # On POSIX a new process group permits terminating children
                    # that remain in the same group when their parent is stopped.
                    # This is best effort, not a container/process-tree sandbox.
                    if os.name != "nt":
                        try:
                            os.killpg(proc.pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                    else:
                        try:
                            subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                                           capture_output=True, timeout=3, check=False)
                        except (OSError, subprocess.TimeoutExpired):
                            pass
                        if proc.poll() is None:
                            proc.kill()
                    proc.wait(timeout=3)
            log.seek(0)
            snippet = log.read(4000).decode("utf-8", "replace")
        if proc.returncode:
            raise ActionError(f"Script exit code {proc.returncode}: {snippet}")
        return f"Script exited 0\n{snippet}"

    def perform(self, step: Step, cancel: threading.Event) -> str:
        if cancel.is_set():
            raise ActionError("Stopped by user")
        t = step.tool
        if t == "desktop.assert_window":
            return self._assert_window(step.title)
        if t == "desktop.wait_window":
            return self._wait_window(step.title, step.timeout_seconds, cancel)
        if t in ("desktop.click", "desktop.type", "desktop.hotkey", "desktop.scroll", "desktop.click_text"):
            if step.window_title is not None:
                self._assert_window(step.window_title)
        if t == "desktop.click":
            self.gui().click(x=step.x, y=step.y)
            return f"Clicked at ({step.x}, {step.y})"
        if t == "desktop.type":
            return self._type(step.text)
        if t == "desktop.hotkey":
            self.gui().hotkey(*[("win" if k == "win" else k) for k in step.keys])
            return "Pressed " + "+".join(step.keys)
        if t == "desktop.scroll":
            self.gui().scroll(step.amount)
            return f"Scrolled {step.amount}"
        if t == "desktop.screenshot":
            dest = self.workspace / "screenshot.png"
            fd, tmp = tempfile.mkstemp(dir=self.workspace, prefix=".desktop-capture-", suffix=".png")
            try:
                os.close(fd)
                self.gui().screenshot().save(tmp)
                os.replace(tmp, dest)
            finally:
                if os.path.exists(tmp):
                    os.unlink(tmp)
            return "Screenshot saved in workspace/screenshot.png"
        if t == "desktop.inspect_text":
            return evidence_for_planner(read_screen(self.gui()), limit=40)[:6000] or "No high-confidence screen text found"
        if t == "desktop.click_text":
            return self._desktop_text(step.text, click=True, expected_window=step.window_title, cancel=cancel)
        if t == "desktop.assert_text":
            return self._desktop_text(step.text)
        if t == "desktop.wait_text":
            return self._wait_text(step.text, step.timeout_seconds, cancel)
        if t == "app.open":
            return self._open_app(step.app)
        if t == "app.launch":
            return self._launch_alias(step.alias)
        if t == "file.read":
            p = self.safe_path(step.path)
            if not p.is_file() or p.stat().st_size > 200000:
                raise ActionError("Readable file not found or exceeds 200 KB")
            return p.read_text(encoding="utf-8")[:20000]
        if t == "file.write":
            p = self.safe_path(step.path)
            p.parent.mkdir(parents=True, exist_ok=True)
            fd, tmp = tempfile.mkstemp(dir=p.parent, prefix=".ai-ai-")
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as stream:
                    stream.write(step.content)
                    stream.flush()
                    os.fsync(stream.fileno())
                # Verify parent again to protect against redirected directory paths
                self.safe_path(step.path)
                os.replace(tmp, p)
            finally:
                if os.path.exists(tmp):
                    os.unlink(tmp)
            return f"Wrote {p.relative_to(self.workspace)} ({len(step.content)} characters)"
        if t == "file.assert_sha256":
            p = self.safe_path(step.path)
            if not p.is_file() or p.stat().st_size > 5_000_000:
                raise ActionError("File verification requires an existing regular file <= 5 MB")
            hasher = hashlib.sha256()
            with p.open("rb") as stream:
                for chunk in iter(lambda: stream.read(65536), b""):
                    hasher.update(chunk)
            if hasher.hexdigest() != step.sha256:
                raise ActionError("File SHA-256 does not match approved digest")
            return "Verified file SHA-256"
        if t == "code.run":
            return self._run_code(step.path, step.timeout_seconds, cancel)
        if t == "android.tap":
            return self._adb(step.serial, "shell", "input", "tap", str(step.x), str(step.y))
        if t == "android.text":
            return self._adb(step.serial, "shell", "input", "text", step.text.replace(" ", "%s"))
        if t == "android.open":
            return self._adb(step.serial, "shell", "monkey", "-p", step.package,
                             "-c", "android.intent.category.LAUNCHER", "1")
        if t == "android.swipe":
            return self._adb(step.serial, "shell", "input", "swipe", str(step.x1), str(step.y1),
                             str(step.x2), str(step.y2), str(step.duration_ms))
        if t == "android.keyevent":
            return self._adb(step.serial, "shell", "input", "keyevent", "KEYCODE_" + step.key)
        if t == "android.screenshot":
            return self._android_screenshot(step.serial)
        if t == "android.inspect_controls":
            return json.dumps(inspect_android_controls(self._android_xml(step.serial)), ensure_ascii=False)
        if t.startswith("browser."):
            if self.browser is None:
                self.browser = BrowserAdapter(self.workspace)
            return self.browser.act(step)
        if t in ("android.tap_text", "android.assert_text"):
            x, y = locate_android(self._android_xml(step.serial), step.text, for_click=t == "android.tap_text")
            if t == "android.assert_text":
                return f"Verified unique Android UI text {step.text!r} at ({x}, {y})"
            newer = locate_android(self._android_xml(step.serial), step.text, for_click=True)
            if abs(x - newer[0]) > 8 or abs(y - newer[1]) > 8:
                raise ActionError("Android UI target moved before tap; refusing stale coordinates")
            if cancel.is_set():
                raise ActionError("Stopped by user")
            self._adb(step.serial, "shell", "input", "tap", str(x), str(y))
            return f"Tapped unique Android UI text {step.text!r} at ({x}, {y})"
        if t == "android.wait_text":
            return self._wait_android_text(step.serial, step.text, step.timeout_seconds, cancel)
        raise ActionError("Unrecognized action type")
