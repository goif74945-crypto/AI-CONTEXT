"""Locally-executed, narrowly typed device actions. NOT an OS security sandbox."""
from __future__ import annotations
import os
import pathlib
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import webbrowser
from typing import Any
from .contracts import Step

class ActionError(RuntimeError):
    pass

class Executor:
    def __init__(self, workspace: pathlib.Path, *, enable_code_run: bool = False):
        self.workspace = workspace.resolve()
        self.workspace.mkdir(parents=True, exist_ok=True)
        self.enable_code_run = enable_code_run

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

    def _adb(self, serial: str | None, *command: str) -> str:
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
            argv = [adb] + (["-s", serial] if serial else ["-s", attached[0]]) + list(command)
            result = subprocess.run(argv, capture_output=True, text=True, timeout=12, check=False)
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise ActionError(f"ADB unavailable: {type(exc).__name__}") from exc
        if result.returncode:
            raise ActionError(f"ADB command failed ({result.returncode}): {result.stderr[:180]}")
        return result.stdout[:500] or "ADB action completed"

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
                                    stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT, env=env)
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
            self.gui().screenshot().save(dest)
            return "Screenshot saved in workspace/screenshot.png"
        if t == "app.open":
            return self._open_app(step.app)
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
        if t == "code.run":
            return self._run_code(step.path, step.timeout_seconds, cancel)
        if t == "android.tap":
            return self._adb(step.serial, "shell", "input", "tap", str(step.x), str(step.y))
        if t == "android.text":
            return self._adb(step.serial, "shell", "input", "text", step.text.replace(" ", "%s"))
        if t == "android.open":
            return self._adb(step.serial, "shell", "monkey", "-p", step.package,
                             "-c", "android.intent.category.LAUNCHER", "1")
        raise ActionError("Unrecognized action type")
