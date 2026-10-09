"""Deterministic pre-execution plan review, not proof that UI steps will succeed.

The operator receives explicit information about missing observations and ambiguous
contexts before approving a potentially irreversible UI action. No model can override
these invariants. Verification steps remain explicitly authored in the plan.
"""
from __future__ import annotations
from collections.abc import Sequence
from typing import Any


class PlanScopeError(ValueError):
    pass


def analyze_plan(steps: Sequence[Any]) -> list[str]:
    """Return warnings; reject browser plans with no explicit starting URL authority.

    The current browser's origin is *never* implicitly inherited from a previous
    approved plan. Every plan containing a browser action must pin its own URL.
    """
    warnings: list[str] = []
    has_browser_origin = False
    for index, action in enumerate(steps):
        tool = action.tool
        if tool == "browser.open":
            has_browser_origin = True
        elif tool.startswith("browser.") and not has_browser_origin:
            raise PlanScopeError(
                f"Step {index + 1} ({tool}) needs browser.open with an explicit URL earlier in this same plan"
            )
        if tool in ("desktop.click", "desktop.type", "desktop.hotkey", "desktop.scroll", "desktop.click_text"):
            if getattr(action, "window_title", None) is None:
                warnings.append(f"Step {index + 1}: desktop input has no active-window identity guard")
        if tool in ("desktop.click", "android.tap"):
            warnings.append(f"Step {index + 1}: coordinate-based action may miss moving UI elements")
        if tool == "code.run":
            warnings.append(f"Step {index + 1}: trusted script runs without an OS-level security sandbox")
        if tool in ("desktop.click_text", "desktop.click", "desktop.type", "android.tap", "android.tap_text",
                    "android.text", "browser.click_text", "browser.click_role", "browser.fill", "file.write"):
            # A later explicit assertion is stronger evidence than a tool returning
            # successfully; still does not prove the entire user's goal is achieved.
            checks = {
                "desktop": ("desktop.assert_text", "desktop.wait_text", "desktop.assert_window", "desktop.wait_window"),
                "android": ("android.assert_text", "android.wait_text"),
                "browser": ("browser.assert_text", "browser.wait_text", "browser.assert_url", "browser.assert_value", "browser.wait_role"),
                "file": ("file.assert_sha256", "file.read"),
            }
            domain = tool.split(".")[0]
            later = [step.tool for step in steps[index+1:]]
            if not any(t in checks[domain] for t in later):
                warnings.append(f"Step {index + 1}: no explicit later {domain} verification; action success is not goal verification")
    return warnings
