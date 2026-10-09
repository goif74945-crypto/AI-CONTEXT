"""Semantic web targeting, explicit failure on ambiguity, and URL validation."""
import pytest
from pydantic import ValidationError
from unittest.mock import Mock
from ai_ai.browser import BrowserAdapter, BrowserError
from ai_ai.contracts import ProposedPlan
from ai_ai.planner import parse_rules
from ai_ai.executor import Executor
import threading


def step(**kw):
    return ProposedPlan.model_validate({"steps":[kw]}).steps[0]


@pytest.mark.parametrize("text,tool", [
    ("เว็บเปิด https://example.org", "browser.open"),
    ("browser click Continue", "browser.click_text"),
    ("เว็บกรอก Email :: user@example.org", "browser.fill"),
    ("browser assert Success", "browser.assert_text"),
    ("browser wait Done :: 6", "browser.wait_text"),
    ("browser screenshot", "browser.screenshot"),
])
def test_browser_command_grammar(text, tool):
    assert parse_rules(text).steps[0].tool == tool


@pytest.mark.parametrize("url", [
    "file:///etc/passwd", "javascript:alert(1)", "https://u:p@example.com/",
    "ftp://example.com/file", "http://", "http://example.com:invalid",
    "https://example.com\\@evil.com", "https://example.org/\r\nX-Injected:1",
])
def test_browser_url_denied(url):
    with pytest.raises(ValidationError): step(tool="browser.open",url=url)


def fake_backend(tmp_path):
    adapter=BrowserAdapter(tmp_path)
    page=Mock()
    adapter._get_page=lambda:page
    return adapter,page


def test_browser_open_rejects_bad_status(tmp_path):
    adapter,page=fake_backend(tmp_path)
    page.goto.return_value.status=403
    with pytest.raises(BrowserError,match="403"):
        adapter.act(step(tool="browser.open",url="https://example.org"))
    page.goto.assert_called_once()
    adapter.close()


def test_browser_click_ambiguity_no_side_effect(tmp_path):
    adapter,page=fake_backend(tmp_path)
    locator=page.get_by_text.return_value
    locator.count.return_value=2
    with pytest.raises(BrowserError,match="found 2"):
        adapter.act(step(tool="browser.click_text",text="Save"))
    locator.click.assert_not_called()
    adapter.close()


def test_browser_click_unique(tmp_path):
    adapter,page=fake_backend(tmp_path)
    locator=page.get_by_text.return_value
    locator.count.return_value=1
    assert "Clicked" in adapter.act(step(tool="browser.click_text",text="Save"))
    page.get_by_text.assert_called_once_with("Save",exact=True)
    locator.click.assert_called_once_with(timeout=10000)
    adapter.close()


def test_browser_fill_by_label(tmp_path):
    adapter,page=fake_backend(tmp_path)
    locator=page.get_by_label.return_value
    locator.count.return_value=1
    assert "Filled" in adapter.act(step(tool="browser.fill",label="Username",text="John"))
    locator.fill.assert_called_once_with("John",timeout=10000)
    adapter.close()


def test_browser_fill_by_placeholder(tmp_path):
    adapter,page=fake_backend(tmp_path)
    page.get_by_label.return_value.count.return_value=0
    page.get_by_placeholder.return_value.count.return_value=1
    assert "Filled" in adapter.act(step(tool="browser.fill",label="Search",text="query"))
    page.get_by_placeholder.return_value.fill.assert_called_once()
    adapter.close()


def test_browser_wait_checks_uniqueness_after_wait(tmp_path):
    adapter,page=fake_backend(tmp_path)
    locator=page.get_by_text.return_value
    locator.count.return_value=2
    with pytest.raises(BrowserError,match="found 2"):
        adapter.act(step(tool="browser.wait_text",text="Loaded",timeout_seconds=4))
    locator.first.wait_for.assert_called_once_with(state="visible",timeout=4000)
    adapter.close()


def test_browser_assert_visible(tmp_path):
    adapter,page=fake_backend(tmp_path)
    locator=page.get_by_text.return_value
    locator.count.return_value=1
    locator.is_visible.return_value=False
    with pytest.raises(BrowserError,match="not visible"):
        adapter.act(step(tool="browser.assert_text",text="Ready"))
    adapter.close()


def test_browser_shared_executor_across_steps(monkeypatch,tmp_path):
    from ai_ai import executor as module
    class FakeBrowser:
        def __init__(self,root): self.actions=[]
        def act(self,step):
            self.actions.append(step.tool)
            return step.tool
    monkeypatch.setattr(module,"BrowserAdapter",FakeBrowser)
    e=Executor(tmp_path)
    for action in (step(tool="browser.open",url="https://example.org"), step(tool="browser.click_text",text="Continue")):
        e.perform(action,threading.Event())
    assert e.browser.actions==["browser.open","browser.click_text"]


def test_browser_screenshot_is_atomic(monkeypatch,tmp_path):
    adapter,page=fake_backend(tmp_path)
    png=b"\x89PNG\r\n\x1a\n"+b"data"
    page.screenshot.return_value=png
    outside=tmp_path/"outside"
    outside.write_text("not touched")
    dest=tmp_path/"browser-screenshot.png"
    try:dest.symlink_to(outside)
    except (OSError,NotImplementedError):pytest.skip("Symlink unavailable")
    assert "saved" in adapter.act(step(tool="browser.screenshot"))
    assert outside.read_text()=="not touched"
    assert dest.read_bytes()==png
    adapter.close()


def test_browser_screenshot_rejects_bad_payload(tmp_path):
    adapter,page=fake_backend(tmp_path)
    page.screenshot.return_value=b"not a PNG"
    with pytest.raises(BrowserError,match="invalid"):
        adapter.act(step(tool="browser.screenshot"))
    assert not (tmp_path/"browser-screenshot.png").exists()
    adapter.close()
