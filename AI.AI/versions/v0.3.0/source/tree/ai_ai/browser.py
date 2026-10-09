"""Owned, isolated browser context with one dedicated Playwright thread.

Does not attach to the user's existing browser profile or steal cookies.
All actions require the same single-use reviewed plan as other device tools.
"""
from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path
import tempfile
from typing import Any
from urllib.parse import urljoin, urlsplit


class BrowserError(RuntimeError):
    pass


class BrowserAdapter:
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.pool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="AI.AI-Browser")
        self.playwright: Any = None
        self.browser: Any = None
        self.page: Any = None
        self.approved_origin: tuple[str, str, int | None] | None = None

    @staticmethod
    def _origin(url: str) -> tuple[str, str, int | None]:
        try:
            parts = urlsplit(url)
            if parts.scheme not in ("https", "http") or not parts.hostname or parts.username or parts.password:
                raise ValueError("unsupported URL")
            port = parts.port or (443 if parts.scheme == "https" else 80)
            return (parts.scheme, parts.hostname.lower().rstrip("."), port)
        except ValueError as exc:
            raise BrowserError("Browser left an approved HTTP(S) origin") from exc

    def _check_origin(self, page: Any) -> None:
        if self.approved_origin is None:
            raise BrowserError("Open an explicitly approved URL before other browser actions")
        if self._origin(page.url) != self.approved_origin:
            raise BrowserError("Browser origin changed; create and approve a new plan")

    def _check_destination(self, locator: Any, page: Any) -> None:
        """Inspect clickable ancestors as well as nested labels before click."""
        destination = locator.evaluate("""element => {
          const anchor = element.closest('a[href]');
          const submit = element.closest('button, input[type="submit"], input[type="image"]');
          const form = submit ? submit.form : null;
          return {
            href: anchor ? anchor.getAttribute('href') : (submit?.getAttribute('formaction') || form?.getAttribute('action') || null),
            target: anchor ? anchor.getAttribute('target') : (submit?.getAttribute('formtarget') || form?.getAttribute('target') || null)
          };
        }""")
        if not isinstance(destination, dict):
            raise BrowserError("Cannot inspect browser click destination")
        href, target = destination.get("href"), destination.get("target")
        if target is not None and not isinstance(target, str):
            raise BrowserError("Cannot inspect browser click target")
        if target and isinstance(target, str) and target.lower() == "_blank":
            raise BrowserError("New browser tabs require a separate approved plan")
        if href and (not isinstance(href,str) or self._origin(urljoin(page.url, href)) != self.approved_origin):
            raise BrowserError("Cross-origin link requires a separate approved navigation")

    def _get_page(self) -> Any:
        if self.page is None:
            try:
                from playwright.sync_api import sync_playwright
                self.playwright = sync_playwright().start()
                launch: dict[str, Any] = {
                    "headless": os.getenv("AI_AI_BROWSER_HEADLESS") == "1", "timeout": 15000
                }
                executable = os.getenv("AI_AI_BROWSER_EXECUTABLE")
                if executable:
                    binary = Path(executable)
                    if not binary.is_absolute() or not binary.is_file():
                        raise BrowserError("Configured Chromium executable must be an existing absolute file")
                    launch["executable_path"] = str(binary)
                self.browser = self.playwright.chromium.launch(**launch)
                context = self.browser.new_context(accept_downloads=False)
                context.set_default_timeout(10000)
                self.page = context.new_page()
            except Exception as exc:
                self._close()
                raise BrowserError(
                    "Browser unavailable. Install optional 'browser' dependencies and run "
                    "`playwright install chromium`; launch requires a graphical desktop. "
                    f"({type(exc).__name__})"
                ) from exc
        return self.page

    @staticmethod
    def _unique(locator: Any, label: str) -> Any:
        count = locator.count()
        if count != 1:
            raise BrowserError(f"Browser target {label!r} requires exactly one match, found {count}")
        return locator

    def _work(self, step: Any) -> str:
        page = self._get_page()
        tool = step.tool
        try:
            if tool == "browser.open":
                self.approved_origin = None
                response = page.goto(step.url, wait_until="domcontentloaded", timeout=15000)
                # URL redirects must not silently widen the approved origin.
                target = self._origin(step.url)
                if self._origin(page.url) != target:
                    self.approved_origin = None
                    raise BrowserError("Navigation redirected to a different origin")
                if response is None:
                    self.approved_origin = target
                    return "Opened browser document (no HTTP response)"
                if response.status >= 400:
                    self.approved_origin = None
                    raise BrowserError(f"HTTP navigation failed with status {response.status}")
                self.approved_origin = target
                return f"Opened web document (HTTP {response.status})"
            self._check_origin(page)
            if tool in ("browser.click_text", "browser.click_role"):
                label = step.text if tool == "browser.click_text" else f"{step.role}:{step.name}"
                raw = (page.get_by_text(step.text, exact=True) if tool == "browser.click_text" else
                       page.get_by_role(step.role, name=step.name, exact=True))
                locator = self._unique(raw, label)
                if not locator.is_visible() or not locator.is_enabled():
                    raise BrowserError("Browser target is hidden or disabled")
                self._check_destination(locator, page)
                locator.click(timeout=10000)
                self._check_origin(page)
                return f"Clicked unique browser target {label!r}"
            if tool == "browser.fill":
                labelled = page.get_by_label(step.label, exact=True)
                locator = labelled if labelled.count() != 0 else page.get_by_placeholder(step.label, exact=True)
                self._unique(locator, step.label).fill(step.text, timeout=10000)
                self._check_origin(page)
                return f"Filled unique browser input {step.label!r} ({len(step.text)} characters)"
            if tool == "browser.assert_url":
                if page.url != step.url:
                    raise BrowserError("Browser URL does not equal the expected value")
                return "Verified browser URL"
            if tool == "browser.assert_text":
                locator = self._unique(page.get_by_text(step.text, exact=True), step.text)
                if not locator.is_visible():
                    raise BrowserError(f"Browser text {step.text!r} is not visible")
                return f"Verified browser text {step.text!r}"
            if tool == "browser.wait_text":
                locator = page.get_by_text(step.text, exact=True)
                locator.first.wait_for(state="visible", timeout=step.timeout_seconds * 1000)
                self._unique(locator, step.text)
                return f"Observed browser text {step.text!r}"
            if tool == "browser.screenshot":
                # Atomic replace avoids following a malicious screenshot symlink.
                png = page.screenshot(timeout=10000)
                if not png.startswith(b"\x89PNG\r\n\x1a\n") or len(png) > 16_000_000:
                    raise BrowserError("Browser screenshot is invalid or exceeds size limit")
                fd, tmp = tempfile.mkstemp(dir=self.workspace, prefix=".browser-capture-")
                try:
                    with os.fdopen(fd,"wb") as stream:
                        stream.write(png)
                    os.replace(tmp, self.workspace / "browser-screenshot.png")
                finally:
                    if os.path.exists(tmp): os.unlink(tmp)
                return "Browser screenshot saved to workspace/browser-screenshot.png"
        except BrowserError:
            raise
        except Exception as exc:
            raise BrowserError(f"Browser action failed ({type(exc).__name__}): {str(exc)[:180]}") from exc
        raise BrowserError("Unknown browser action")

    def act(self, step: Any) -> str:
        return self.pool.submit(self._work, step).result()

    def _close(self) -> None:
        for key in ("browser", "playwright"):
            handle = getattr(self, key)
            if handle is not None:
                try:
                    (handle.close() if key == "browser" else handle.stop())
                except Exception:
                    pass
                setattr(self, key, None)
        self.page = None
        self.approved_origin = None

    def close(self) -> None:
        self.pool.submit(self._close).result()
        self.pool.shutdown(wait=True)
