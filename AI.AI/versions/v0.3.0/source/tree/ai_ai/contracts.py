"""Strict tool contracts. Never pass model output directly into subprocess/OS APIs."""
from __future__ import annotations
from typing import Annotated, Literal, Union
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
import re
from urllib.parse import urlsplit

class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

class WindowBound(Strict):
    # Optional exact focus guard. Never guess which app receives input.
    window_title: str | None = Field(default=None, min_length=2, max_length=160)

class Click(WindowBound):
    tool: Literal["desktop.click"]
    x: int = Field(ge=0, le=16384)
    y: int = Field(ge=0, le=16384)

class TypeText(WindowBound):
    tool: Literal["desktop.type"]
    text: str = Field(min_length=1, max_length=8000)

ALLOWED_KEYS = {"ctrl", "alt", "shift", "win", "command", "enter", "tab", "esc", "space", "a", "c", "v", "x", "z", "s", "p", "t", "w", "f", "n", "backspace", "delete", "up", "down", "left", "right", "home", "end"}
class Hotkey(WindowBound):
    tool: Literal["desktop.hotkey"]
    keys: list[str] = Field(min_length=1, max_length=4)
    @field_validator("keys")
    @classmethod
    def keys_valid(cls, values: list[str]) -> list[str]:
        if any(key not in ALLOWED_KEYS for key in values) or len(set(values)) != len(values):
            raise ValueError("Unsupported or duplicate keyboard key")
        return values

class Scroll(WindowBound):
    tool: Literal["desktop.scroll"]
    amount: int = Field(ge=-25, le=25)

class Screenshot(Strict):
    tool: Literal["desktop.screenshot"]

class ClickText(WindowBound):
    tool: Literal["desktop.click_text"]
    text: str = Field(min_length=1, max_length=100)

class AssertText(Strict):
    tool: Literal["desktop.assert_text"]
    text: str = Field(min_length=1, max_length=100)

class WaitText(Strict):
    tool: Literal["desktop.wait_text"]
    text: str = Field(min_length=1, max_length=100)
    timeout_seconds: int = Field(default=5, ge=1, le=15)

class AssertWindow(Strict):
    tool: Literal["desktop.assert_window"]
    title: str = Field(min_length=2, max_length=160)

class BrowserOpen(Strict):
    tool: Literal["browser.open"]
    url: str = Field(min_length=8, max_length=2048)
    @field_validator("url")
    @classmethod
    def valid_url(cls, value: str) -> str:
        if any(ord(ch) <= 32 for ch in value) or "\\" in value:
            raise ValueError("URL contains disallowed whitespace/control characters")
        try:
            parts = urlsplit(value)
            if parts.scheme.lower() not in ("https", "http") or not parts.hostname or parts.username or parts.password:
                raise ValueError("URL must be http(s) and must not embed credentials")
            _ = parts.port  # Reject malformed ports
        except ValueError as exc:
            raise ValueError("Invalid web URL") from exc
        return value

class BrowserClickText(Strict):
    tool: Literal["browser.click_text"]
    text: str = Field(min_length=1, max_length=100)

class BrowserClickRole(Strict):
    tool: Literal["browser.click_role"]
    role: Literal["button", "link", "checkbox", "menuitem", "tab", "radio"]
    name: str = Field(min_length=1, max_length=100)

class BrowserFill(Strict):
    tool: Literal["browser.fill"]
    label: str = Field(min_length=1, max_length=100)
    text: str = Field(max_length=8000)

class BrowserAssertText(Strict):
    tool: Literal["browser.assert_text"]
    text: str = Field(min_length=1, max_length=100)

class BrowserWaitText(Strict):
    tool: Literal["browser.wait_text"]
    text: str = Field(min_length=1, max_length=100)
    timeout_seconds: int = Field(default=5, ge=1, le=15)

class BrowserScreenshot(Strict):
    tool: Literal["browser.screenshot"]

class BrowserAssertUrl(Strict):
    tool: Literal["browser.assert_url"]
    url: str = Field(min_length=8, max_length=2048)
    # Reuse the same strict validation as browser.open.
    _url_validator = field_validator("url")(BrowserOpen.valid_url.__func__)

class AppOpen(Strict):
    tool: Literal["app.open"]
    app: Literal["notepad", "calculator", "browser"]

class AppLaunch(Strict):
    tool: Literal["app.launch"]
    alias: str = Field(min_length=2, max_length=40)
    @field_validator("alias")
    @classmethod
    def validate_alias(cls, value: str) -> str:
        if not re.fullmatch(r"[a-z][a-z0-9_.-]{1,39}", value):
            raise ValueError("Application alias must be lowercase and contain no shell syntax")
        return value

class FileRead(Strict):
    tool: Literal["file.read"]
    path: str = Field(min_length=1, max_length=240)

class FileWrite(Strict):
    tool: Literal["file.write"]
    path: str = Field(min_length=1, max_length=240)
    content: str = Field(max_length=100000)

class CodeRun(Strict):
    tool: Literal["code.run"]
    path: str = Field(min_length=1, max_length=240)
    timeout_seconds: int = Field(default=10, ge=1, le=30)

class AndroidTap(Strict):
    tool: Literal["android.tap"]
    x: int = Field(ge=0, le=16384)
    y: int = Field(ge=0, le=16384)
    serial: str | None = None
    @field_validator("serial")
    @classmethod
    def valid_serial(cls, value: str | None) -> str | None:
        if value is not None and not re.fullmatch(r"[a-zA-Z0-9.:_-]{1,128}", value):
            raise ValueError("Invalid ADB serial")
        return value

class AndroidText(Strict):
    tool: Literal["android.text"]
    text: str = Field(min_length=1, max_length=200)
    serial: str | None = None
    @field_validator("serial")
    @classmethod
    def valid_serial(cls, value: str | None) -> str | None:
        if value is not None and not re.fullmatch(r"[a-zA-Z0-9.:_-]{1,128}", value):
            raise ValueError("Invalid ADB serial")
        return value
    @field_validator("text")
    @classmethod
    def ascii_only(cls, value: str) -> str:
        if not re.fullmatch(r"[A-Za-z0-9 ._-]+", value):
            raise ValueError("ADB text supports only simple ASCII; Thai and symbols need an Android IME bridge")
        return value

class AndroidOpen(Strict):
    tool: Literal["android.open"]
    package: str = Field(min_length=3, max_length=180)
    serial: str | None = None
    @field_validator("package")
    @classmethod
    def valid_package(cls, value: str) -> str:
        if not re.fullmatch(r"[A-Za-z0-9_]+(?:\.[A-Za-z0-9_]+)+", value):
            raise ValueError("Invalid Android package")
        return value
    @field_validator("serial")
    @classmethod
    def valid_serial(cls, value: str | None) -> str | None:
        if value is not None and not re.fullmatch(r"[a-zA-Z0-9.:_-]{1,128}", value):
            raise ValueError("Invalid ADB serial")
        return value

class AndroidTarget(Strict):
    serial: str | None = None
    @field_validator("serial")
    @classmethod
    def valid_serial(cls, value: str | None) -> str | None:
        if value is not None and not re.fullmatch(r"[a-zA-Z0-9.:_-]{1,128}", value):
            raise ValueError("Invalid ADB serial")
        return value

class AndroidSwipe(AndroidTarget):
    tool: Literal["android.swipe"]
    x1: int = Field(ge=0, le=16384)
    y1: int = Field(ge=0, le=16384)
    x2: int = Field(ge=0, le=16384)
    y2: int = Field(ge=0, le=16384)
    duration_ms: int = Field(default=350, ge=100, le=2000)

class AndroidKey(AndroidTarget):
    tool: Literal["android.keyevent"]
    key: Literal["BACK", "HOME", "ENTER", "TAB", "DPAD_UP", "DPAD_DOWN", "DPAD_LEFT", "DPAD_RIGHT"]

class AndroidScreenshot(AndroidTarget):
    tool: Literal["android.screenshot"]

class AndroidTapText(AndroidTarget):
    tool: Literal["android.tap_text"]
    text: str = Field(min_length=1, max_length=100)

class AndroidAssertText(AndroidTarget):
    tool: Literal["android.assert_text"]
    text: str = Field(min_length=1, max_length=100)

Step = Annotated[Union[
    Click, TypeText, Hotkey, Scroll, Screenshot, ClickText, AssertText, WaitText, AssertWindow,
    AppOpen, AppLaunch, FileRead, FileWrite, CodeRun, AndroidTap, AndroidText, AndroidOpen,
    AndroidSwipe, AndroidKey, AndroidScreenshot, AndroidTapText, AndroidAssertText,
    BrowserOpen, BrowserClickText, BrowserClickRole, BrowserFill, BrowserAssertText, BrowserWaitText, BrowserScreenshot, BrowserAssertUrl,
], Field(discriminator="tool")]

class ProposedPlan(Strict):
    steps: list[Step] = Field(min_length=1, max_length=24)

class PlanRequest(Strict):
    text: str = Field(min_length=1, max_length=4000)
    use_ai: bool = False
    share_screen_text: bool = False

    @model_validator(mode="after")
    def consent_for_visual_context(self) -> "PlanRequest":
        if self.share_screen_text and not self.use_ai:
            raise ValueError("Screen OCR sharing requires AI mode")
        return self

class ExecuteRequest(Strict):
    plan_id: str = Field(min_length=32, max_length=36)
    approval: Literal["I_APPROVE_THIS_PLAN"]

class PlanView(Strict):
    id: str
    steps: list[Step]
    warnings: list[str]
    clap_eligible: bool
    source: Literal["rules", "llm"]
