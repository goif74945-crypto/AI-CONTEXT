"""Strict tool contracts. Never pass model output directly into subprocess/OS APIs."""
from __future__ import annotations
from typing import Annotated, Literal, Union
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
import re

class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

class Click(Strict):
    tool: Literal["desktop.click"]
    x: int = Field(ge=0, le=16384)
    y: int = Field(ge=0, le=16384)

class TypeText(Strict):
    tool: Literal["desktop.type"]
    text: str = Field(min_length=1, max_length=8000)

ALLOWED_KEYS = {"ctrl", "alt", "shift", "win", "command", "enter", "tab", "esc", "space", "a", "c", "v", "x", "z", "s", "p", "t", "w", "f", "n", "backspace", "delete", "up", "down", "left", "right", "home", "end"}
class Hotkey(Strict):
    tool: Literal["desktop.hotkey"]
    keys: list[str] = Field(min_length=1, max_length=4)
    @field_validator("keys")
    @classmethod
    def keys_valid(cls, values: list[str]) -> list[str]:
        if any(key not in ALLOWED_KEYS for key in values) or len(set(values)) != len(values):
            raise ValueError("Unsupported or duplicate keyboard key")
        return values

class Scroll(Strict):
    tool: Literal["desktop.scroll"]
    amount: int = Field(ge=-25, le=25)

class Screenshot(Strict):
    tool: Literal["desktop.screenshot"]

class AppOpen(Strict):
    tool: Literal["app.open"]
    app: Literal["notepad", "calculator", "browser"]

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

Step = Annotated[Union[Click, TypeText, Hotkey, Scroll, Screenshot, AppOpen, FileRead, FileWrite, CodeRun, AndroidTap, AndroidText, AndroidOpen], Field(discriminator="tool")]

class ProposedPlan(Strict):
    steps: list[Step] = Field(min_length=1, max_length=12)

class PlanRequest(Strict):
    text: str = Field(min_length=1, max_length=4000)
    use_ai: bool = False

class ExecuteRequest(Strict):
    plan_id: str = Field(min_length=32, max_length=36)
    approval: Literal["I_APPROVE_THIS_PLAN"]

class PlanView(Strict):
    id: str
    steps: list[Step]
    warnings: list[str]
    clap_eligible: bool
    source: Literal["rules", "llm"]
