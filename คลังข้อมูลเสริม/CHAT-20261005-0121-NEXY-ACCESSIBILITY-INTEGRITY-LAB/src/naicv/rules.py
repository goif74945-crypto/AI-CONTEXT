from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RuleMeta:
    rule_id: str
    standard: str
    requirement: str
    default_severity: str
    claim_boundary: str


RULES = (
    RuleMeta("NAICV-NAME-001", "WCAG 2.2 / 4.1.2 modeled precondition", "Interactive component exposes an accessible name", "ERROR", "Abstract model only; DOM accessibility tree not tested"),
    RuleMeta("NAICV-KBD-001", "WCAG 2.2 / 2.1.1", "Interactive functionality is keyboard reachable", "ERROR", "Actual event behavior not tested"),
    RuleMeta("NAICV-FOCUS-001", "WCAG 2.2 / 2.4.7", "Keyboard focus has a visible indicator", "ERROR", "Contrast/obscuration require rendering tests"),
    RuleMeta("NAICV-TABINDEX-001", "WAI-ARIA APG guidance", "Avoid positive tabindex ordering", "WARNING", "APG guidance, not an independent WCAG conformance result"),
    RuleMeta("NAICV-BUTTON-001", "WAI-ARIA APG Button Pattern", "Custom button supports Enter and Space", "WARNING", "Pattern guidance; native buttons already provide semantics"),
    RuleMeta("NAICV-COLOR-001", "WCAG 2.2 / 1.4.1", "State/error/freeze meaning is not conveyed by color alone", "ERROR", "Visual rendering still requires inspection"),
    RuleMeta("NAICV-TARGET-001", "WCAG 2.2 / 2.5.8", "Pointer target is at least 24x24 CSS px or a valid exception applies", "ERROR", "Spacing/equivalent/inline/user-agent/essential exceptions require external evidence"),
    RuleMeta("NAICV-DRAG-001", "WCAG 2.2 / 2.5.7", "Dragging functionality has a single-pointer non-drag alternative unless exempt", "ERROR", "Actual pointer interaction not executed"),
    RuleMeta("NAICV-ERROR-001", "WCAG 2.2 / 3.3.1", "Detected input errors identify the field and describe the error in text", "ERROR", "Runtime validation timing not executed"),
    RuleMeta("NAICV-STATUS-001", "WCAG 2.2 / 4.1.3 modeled precondition", "Dynamic status messages expose programmatic status semantics", "ERROR", "Screen-reader announcement behavior not executed"),
    RuleMeta("NAICV-DIALOG-001", "WAI-ARIA APG Modal Dialog Pattern", "Modal dialog has name and contained/predictable focus", "WARNING", "APG guidance; assistive-technology testing remains required"),
    RuleMeta("NAICV-TABS-001", "WAI-ARIA APG Tabs Pattern", "Tabs expose selected tab/panel mapping and expected keyboard keys", "WARNING", "APG guidance; runtime keyboard behavior not executed"),
    RuleMeta("NAICV-TABLE-001", "WCAG 2.2 / 1.3.1 modeled precondition", "Data table exposes headers and an accessible label/caption", "ERROR", "Header associations in DOM not tested"),
    RuleMeta("NEXY-A11Y-FREEZE-001", "NEXY DOC-C UI Truth + accessibility proposal", "FREEZE must be perceivable programmatically and visually without color-only meaning", "BLOCKER", "Proposal combines project truth law with accessibility surface requirements"),
    RuleMeta("NEXY-A11Y-STOP-001", "NEXY DOC-C UI Truth + accessibility proposal", "STOP must expose a critical programmatic and visual signal", "BLOCKER", "Proposal, not current adopted build requirement"),
    RuleMeta("NEXY-A11Y-DISABLED-001", "NEXY DOC-D deterministic validation-copy direction / proposal", "Critical disabled controls expose a reason", "WARNING", "Product proposal; wording quality requires human review"),
)

RULE_BY_ID = {rule.rule_id: rule for rule in RULES}
