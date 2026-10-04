from __future__ import annotations

import re
from dataclasses import dataclass

from .model import ContextBundle
from .serialization import canonical_json_text


@dataclass(frozen=True, slots=True)
class SensitiveFinding:
    atom_id: str
    kind: str


_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("openai_api_key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b")),
    ("github_token", re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b")),
    ("private_key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
)


def scan_sensitive(bundle: ContextBundle) -> tuple[SensitiveFinding, ...]:
    findings: list[SensitiveFinding] = []
    for atom in bundle.atoms:
        haystacks = [atom.text, *atom.provenance, *atom.evidence, canonical_json_text(atom.metadata)]
        for kind, pattern in _PATTERNS:
            if any(pattern.search(value) for value in haystacks):
                findings.append(SensitiveFinding(atom.atom_id, kind))
    return tuple(sorted(findings, key=lambda x: (x.atom_id, x.kind)))
