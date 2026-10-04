# NEXY Accessibility Integrity Lab

**Status:** PROPOSAL_AI / standalone reference implementation / not adopted NEXY law or build scope.

This lab defines an abstract UI-surface contract and a deterministic validator for accessibility-integrity properties that are especially important to NEXY's truth surface: keyboard operability, visible focus, accessible names, non-color status cues, pointer target sizing, drag alternatives, dynamic status semantics, form-error associations, modal focus behavior, tabs, data tables, and explicit FREEZE/STOP exposure.

It intentionally does **not** claim WCAG conformance. The validator sees JSON assertions, not a rendered DOM, CSS, browser accessibility tree, real keyboard events, screen-reader speech, zoom/reflow, or mobile assistive technology.

## Why NEXY benefits

NEXY's source-derived UI laws require real state to be visible, FREEZE not to be masked, fake success to be forbidden, and critical controls/status to tell the truth. A surface that communicates truth only to a mouse user or only through color is still an incomplete truth surface. This lab makes that failure class machine-reviewable before real browser/AT verification.

## Quick start

```bash
PYTHONPATH=src python -m naicv rules
PYTHONPATH=src python -m naicv validate fixtures/valid/freeze.json
PYTHONPATH=src python -m unittest discover -s tests -v
```

CLI exit codes: `0=PASS`, `1=FAIL`, `2=PARTIAL/manual evidence required`.
