from __future__ import annotations

import hashlib
import re
from pathlib import PurePosixPath

from .graph import extract_link_edges
from .model import Document, Finding, Severity
from .policy import NEXYPolicy

_CURRENT_WORDS = re.compile(r"\b(current|currently|total|exhaustive|all|denominator|system count|requirement count)\b", re.I)
_HISTORICAL_WORDS = re.compile(r"\b(historical|deprecated|legacy|provenance|do not use|unreliable|superseded)\b", re.I)
_REQUIREMENT_ROW_RE = re.compile(r"\b(\d{2,4})\s+(?:normalized\s+)?requirement\s+rows?\b", re.I)
_CURRENT_BUILD_PHRASE_RE = re.compile(r"\bcurrent\s+build\b", re.I)
_STANDALONE_NUMBER_RE = re.compile(r"(?<![A-Za-z0-9])\d{2,4}(?![A-Za-z0-9])")
_COMPLETE_RE = re.compile(r"\bSTATUS\s*:\s*(?:COMPLETE|PASS)\b", re.I)
_EVIDENCE_RE = re.compile(r"\b(EVIDENCE|VERIFIED|E[0-7]|test|command|artifact|commit)\b", re.I)
_PROPOSAL_MARKER_RE = re.compile(r"\b(AI[- ]PROPOSED|EXPERIMENTAL|NOT CANON|CONCEPT(?:UAL)?)\b", re.I)

_SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("openai_key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b")),
    ("github_pat", re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b")),
    ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
)


def _line_findings(doc: Document, regex: re.Pattern[str]):
    for line_no, line in enumerate(doc.text.splitlines(), start=1):
        if regex.search(line):
            yield line_no, line


def rule_broken_local_links(documents: list[Document], _: NEXYPolicy) -> list[Finding]:
    paths = {doc.path for doc in documents}
    # Directory existence matters for links that intentionally target a folder.
    directories: set[str] = {"."}
    for path in paths:
        p = PurePosixPath(path)
        for parent in p.parents:
            directories.add(parent.as_posix())

    findings: list[Finding] = []
    for edge in extract_link_edges(documents):
        if edge.target not in paths and edge.target not in directories:
            findings.append(Finding(
                "PG001",
                Severity.ERROR,
                edge.source,
                edge.line,
                "local Markdown link target does not exist in the scanned corpus",
                {"target": edge.target},
            ))
    return findings


def rule_deprecated_denominator(documents: list[Document], policy: NEXYPolicy) -> list[Finding]:
    findings: list[Finding] = []
    needle = re.compile(rf"\b{policy.deprecated_registry_count}\b")
    for doc in documents:
        for line_no, line in enumerate(doc.text.splitlines(), start=1):
            if not needle.search(line):
                continue
            if _CURRENT_WORDS.search(line) and not _HISTORICAL_WORDS.search(line):
                findings.append(Finding(
                    "PG002",
                    Severity.CRITICAL,
                    doc.path,
                    line_no,
                    f"deprecated {policy.deprecated_registry_count}-entry registry appears to be used as current truth",
                    {"deprecated_count": policy.deprecated_registry_count},
                ))
    return findings


def rule_current_requirement_denominator(documents: list[Document], policy: NEXYPolicy) -> list[Finding]:
    findings: list[Finding] = []
    for doc in documents:
        for line_no, line in enumerate(doc.text.splitlines(), start=1):
            for match in _REQUIREMENT_ROW_RE.finditer(line):
                value = int(match.group(1))
                context = line[max(0, match.start() - 100): match.end() + 100]
                if _HISTORICAL_WORDS.search(context):
                    continue
                if _CURRENT_WORDS.search(context) and value != policy.current_requirement_rows:
                    findings.append(Finding(
                        "PG003",
                        Severity.CRITICAL,
                        doc.path,
                        line_no,
                        "current normalized requirement-row denominator conflicts with policy",
                        {"observed": value, "expected": policy.current_requirement_rows},
                    ))
    return findings


def rule_current_build_denominator(documents: list[Document], policy: NEXYPolicy) -> list[Finding]:
    findings: list[Finding] = []
    for doc in documents:
        for line_no, line in enumerate(doc.text.splitlines(), start=1):
            phrase = _CURRENT_BUILD_PHRASE_RE.search(line)
            if not phrase or _HISTORICAL_WORDS.search(line):
                continue
            candidates = []
            for number in _STANDALONE_NUMBER_RE.finditer(line):
                # Use only values plausibly attached to the phrase, and choose the nearest one.
                if number.end() <= phrase.start():
                    gap = phrase.start() - number.end()
                elif number.start() >= phrase.end():
                    gap = number.start() - phrase.end()
                else:
                    gap = 0
                if gap <= 32:
                    candidates.append((gap, number.start(), int(number.group(0))))
            if not candidates:
                continue
            _, _, value = min(candidates)
            if value != policy.current_build_rows:
                findings.append(Finding(
                    "PG004",
                    Severity.ERROR,
                    doc.path,
                    line_no,
                    "current-build row count conflicts with policy",
                    {"observed": value, "expected": policy.current_build_rows},
                ))
    return findings


def rule_unlabeled_proposal(documents: list[Document], policy: NEXYPolicy) -> list[Finding]:
    findings: list[Finding] = []
    prefix = policy.proposal_root.rstrip("/") + "/"
    for doc in documents:
        if not doc.path.startswith(prefix):
            continue
        # Code, tests and evidence live under the proposal root too; only prose design artifacts need the marker.
        if doc.kind not in {"md", "markdown", "txt"}:
            continue
        lower_parts = {p.lower() for p in PurePosixPath(doc.path).parts}
        if lower_parts & {"src", "tests", "evidence"}:
            continue
        head = "\n".join(doc.text.splitlines()[:40])
        if not _PROPOSAL_MARKER_RE.search(head):
            findings.append(Finding(
                "PG005",
                Severity.ERROR,
                doc.path,
                1,
                "supplemental design/prose is missing an explicit AI-PROPOSED/EXPERIMENTAL/NOT-CANON marker near the top",
                {},
            ))
    return findings


def rule_completion_without_evidence(documents: list[Document], _: NEXYPolicy) -> list[Finding]:
    findings: list[Finding] = []
    for doc in documents:
        lines = doc.text.splitlines()
        for line_no, line in enumerate(lines, start=1):
            if not _COMPLETE_RE.search(line):
                continue
            window = "\n".join(lines[max(0, line_no - 4): min(len(lines), line_no + 8)])
            if not _EVIDENCE_RE.search(window):
                findings.append(Finding(
                    "PG006",
                    Severity.WARNING,
                    doc.path,
                    line_no,
                    "completion/PASS status is not accompanied by a nearby evidence marker",
                    {},
                ))
    return findings


def rule_secret_signatures(documents: list[Document], _: NEXYPolicy) -> list[Finding]:
    findings: list[Finding] = []
    for doc in documents:
        for line_no, line in enumerate(doc.text.splitlines(), start=1):
            for secret_type, pattern in _SECRET_PATTERNS:
                for match in pattern.finditer(line):
                    digest = hashlib.sha256(match.group(0).encode("utf-8")).hexdigest()[:12]
                    findings.append(Finding(
                        "PG007",
                        Severity.CRITICAL,
                        doc.path,
                        line_no,
                        "possible credential-like token detected; value intentionally redacted",
                        {"secret_type": secret_type, "fingerprint": digest},
                    ))
    return findings


RULES = (
    rule_broken_local_links,
    rule_deprecated_denominator,
    rule_current_requirement_denominator,
    rule_current_build_denominator,
    rule_unlabeled_proposal,
    rule_completion_without_evidence,
    rule_secret_signatures,
)


def run_rules(documents: list[Document], policy: NEXYPolicy) -> list[Finding]:
    findings: list[Finding] = []
    for rule in RULES:
        findings.extend(rule(documents, policy))
    return sorted(findings, key=lambda f: (-int(f.severity), f.path, f.line or 0, f.rule_id))
