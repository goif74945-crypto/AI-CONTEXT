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


class BrowserError(RuntimeError):
    pass


class BrowserAdapter:
    def __init__(self, workspace: Path):
        self.workspace = workspace
        self.pool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="AI.AI-Browser")
        self.playwright: Any = None
        self.browser: Any = None
        self.page: Any = None

    def _get_page(self) -> Any:
        if self.page is None:
            try:
                from playwright.sync_api import sync_playwright
                self.playwright = sync_playwright().start()
                self.browser = self.playwright.chromium.launch(
                    headless=os.getenv("AI_AI_BROWSER_HEADLESS") == "1", timeout=15000)
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
                response = page.goto(step.url, wait_until="domcontentloaded", timeout=15000)
                if response is None:
                    return "Opened browser document (no HTTP response)"
                if response.status >= 400:
                    raise BrowserError(f"HTTP navigation failed with status {response.status}")
                return f"Opened web document (HTTP {response.status})"
            if tool == "browser.click_text":
                locator = self._unique(page.get_by_text(step.text, exact=True), step.text)
                locator.click(timeout=10000)
                return f"Clicked unique browser text {step.text!r}"
            if tool == "browser.fill":
                labelled = page.get_by_label(step.label, exact=True)
                locator = labelled if labelled.count() != 0 else page.get_by_placeholder(step.label, exact=True)
                self._unique(locator, step.label).fill(step.text, timeout=10000)
                return f"Filled unique browser input {step.label!r} ({len(step.text)} characters)"
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

    def close(self) -> None:
        self.pool.submit(self._close).result()
        self.pool.shutdown(wait=True)
