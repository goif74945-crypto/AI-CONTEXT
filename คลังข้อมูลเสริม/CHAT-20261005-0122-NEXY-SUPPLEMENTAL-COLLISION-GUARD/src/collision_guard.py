from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Sequence

SCHEMA = "supplemental-collision-guard/v1"
RISK_ORDER = {"DISTINCT": 0, "RELATED": 1, "HIGH_OVERLAP": 2, "LIKELY_DUPLICATE": 3}
SUPPORTED_SUFFIXES = {".md", ".txt", ".json", ".jsonl", ".yaml", ".yml", ".toml", ".py", ".ts", ".tsx", ".js"}
IGNORED_DIR_NAMES = {"generated", ".git", ".pytest_cache", "__pycache__", ".mypy_cache", ".ruff_cache"}
GENERIC_TERMS = {
    "a", "an", "and", "ai", "chat", "context", "for", "future", "lab", "nexy",
    "of", "project", "supplement", "supplemental", "system", "systems", "the", "to",
    "vault", "with", "work", "workspace", "goif", "sol", "gpt56", "gpt", "engineering",
    "intelligence", "2026", "20261005",
}
TAG_RULES = {
    "knowledge": {"knowledge", "provenance", "ledger", "ontology", "memory", "decay", "lifecycle"},
    "verification": {"verify", "verification", "evidence", "proof", "assurance", "audit", "eval", "regression"},
    "reliability": {"reliability", "resilience", "failure", "recovery", "survivability", "chaos"},
    "semantics": {"semantic", "contract", "meaning", "intent", "spec", "requirement"},
    "experience": {"experience", "interaction", "journey", "friction", "delight", "ux", "user"},
    "governance": {"authority", "governance", "control", "policy", "decision", "human"},
    "temporal": {"temporal", "freshness", "stale", "validity", "decay", "time"},
    "counterfactual": {"counterfactual", "impact", "simulation", "scenario", "causal"},
    "coordination": {"collision", "duplicate", "overlap", "parallel", "coordination", "catalog", "registry"},
    "economics": {"economics", "cost", "capacity", "budget", "resource"},
    "security": {"security", "trust", "threat", "boundary", "poisoning"},
}

_TOKEN_RE = re.compile(r"[A-Za-z0-9]+|[\u0E00-\u0E7F]+", flags=re.UNICODE)
_DATE_LIKE_RE = re.compile(r"^(?:\d{4,}|\d{1,4}t\d+)$", flags=re.IGNORECASE)


def normalize_terms(text: str) -> set[str]:
    terms: set[str] = set()
    for raw in _TOKEN_RE.findall(text.lower()):
        token = raw.strip("_-")
        if not token or token in GENERIC_TERMS:
            continue
        if _DATE_LIKE_RE.match(token):
            continue
        if token.isdigit():
            continue
        if len(token) <= 1:
            continue
        terms.add(token)
    return terms


def infer_tags(terms: Iterable[str]) -> set[str]:
    term_set = set(terms)
    return {
        tag for tag, vocabulary in TAG_RULES.items()
        if term_set.intersection(vocabulary)
    }


def _safe_read(path: Path, max_bytes: int) -> str:
    try:
        data = path.read_bytes()[:max_bytes]
        return data.decode("utf-8", errors="ignore")
    except (OSError, UnicodeError):
        return ""


def _collect_project_text(project_dir: Path, max_files: int = 80, max_bytes_per_file: int = 32_000) -> tuple[str, int, int]:
    parts = [project_dir.name]
    files_read = 0
    bytes_read = 0
    candidates = sorted(
        p for p in project_dir.rglob("*")
        if p.is_file()
        and not p.is_symlink()
        and p.suffix.lower() in SUPPORTED_SUFFIXES
        and not set(p.relative_to(project_dir).parts[:-1]).intersection(IGNORED_DIR_NAMES)
    )
    for path in candidates[:max_files]:
        text = _safe_read(path, max_bytes_per_file)
        if not text:
            continue
        parts.append(path.relative_to(project_dir).as_posix())
        parts.append(text)
        files_read += 1
        bytes_read += len(text.encode("utf-8"))
    return "\n".join(parts), files_read, bytes_read


@dataclass(frozen=True)
class Candidate:
    title: str
    summary: str = ""
    tags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("candidate title must not be blank")

    @property
    def terms(self) -> set[str]:
        return normalize_terms(f"{self.title}\n{self.summary}\n{' '.join(self.tags)}")

    @property
    def inferred_tags(self) -> set[str]:
        return infer_tags(self.terms).union(t.lower() for t in self.tags)


@dataclass
class ProjectRecord:
    name: str
    path: str
    terms: set[str] = field(default_factory=set)
    tags: set[str] = field(default_factory=set)
    content_hash: str = ""
    files_read: int = 0
    bytes_read: int = 0

    @classmethod
    def from_text(cls, name: str, path: str, text: str, files_read: int = 0, bytes_read: int = 0) -> "ProjectRecord":
        terms = normalize_terms(f"{name}\n{text}")
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        return cls(
            name=name,
            path=path,
            terms=terms,
            tags=infer_tags(terms),
            content_hash=digest,
            files_read=files_read,
            bytes_read=bytes_read,
        )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": self.path,
            "terms": sorted(self.terms),
            "tags": sorted(self.tags),
            "content_hash": self.content_hash,
            "files_read": self.files_read,
            "bytes_read": self.bytes_read,
        }


def discover_projects(root: Path | str) -> list[ProjectRecord]:
    root = Path(root)
    if not root.exists() or not root.is_dir():
        raise ValueError(f"supplemental root does not exist or is not a directory: {root}")

    records: list[ProjectRecord] = []
    for child in sorted(root.iterdir(), key=lambda p: p.name.casefold()):
        if child.is_symlink() or not child.is_dir() or child.name.startswith("."):
            continue
        text, files_read, bytes_read = _collect_project_text(child)
        records.append(
            ProjectRecord.from_text(
                name=child.name,
                path=str(child.relative_to(root)),
                text=text,
                files_read=files_read,
                bytes_read=bytes_read,
            )
        )
    return records


def _jaccard(a: set[str], b: set[str]) -> float:
    union = a | b
    if not union:
        return 0.0
    return len(a & b) / len(union)


def _containment(a: set[str], b: set[str]) -> float:
    if not a:
        return 0.0
    return len(a & b) / len(a)


def score_candidate(candidate: Candidate, project: ProjectRecord) -> dict:
    c_terms = candidate.terms
    p_terms = project.terms
    c_tags = candidate.inferred_tags
    p_tags = project.tags

    term_jaccard = _jaccard(c_terms, p_terms)
    candidate_containment = _containment(c_terms, p_terms)
    tag_jaccard = _jaccard(c_tags, p_tags)

    # Containment matters most because project records are usually much larger than a short candidate brief.
    score = (0.60 * candidate_containment) + (0.25 * term_jaccard) + (0.15 * tag_jaccard)
    score = round(min(1.0, score), 6)

    return {
        "project": project.name,
        "path": project.path,
        "score": score,
        "shared_terms": sorted(c_terms & p_terms)[:24],
        "shared_tags": sorted(c_tags & p_tags),
        "term_jaccard": round(term_jaccard, 6),
        "candidate_containment": round(candidate_containment, 6),
        "tag_jaccard": round(tag_jaccard, 6),
    }


def classify_score(score: float) -> str:
    if score >= 0.93:
        return "LIKELY_DUPLICATE"
    if score >= 0.62:
        return "HIGH_OVERLAP"
    if score >= 0.38:
        return "RELATED"
    return "DISTINCT"


def analyze_candidate(candidate: Candidate, records: Sequence[ProjectRecord], top_n: int = 8) -> dict:
    if not candidate.terms:
        raise ValueError("candidate has no discriminating terms after normalization")

    ranked = sorted(
        (score_candidate(candidate, record) for record in records),
        key=lambda item: (-item["score"], item["project"].casefold(), item["path"].casefold()),
    )
    top_matches = ranked[: max(1, top_n)] if ranked else []
    top_score = top_matches[0]["score"] if top_matches else 0.0
    classification = classify_score(top_score)

    return {
        "schema": SCHEMA,
        "candidate": {
            "title": candidate.title,
            "summary": candidate.summary,
            "terms": sorted(candidate.terms),
            "tags": sorted(candidate.inferred_tags),
        },
        "classification": classification,
        "top_score": top_score,
        "top_matches": top_matches,
        "decision_guidance": {
            "LIKELY_DUPLICATE": "Do not create a parallel project until the overlap is explicitly justified.",
            "HIGH_OVERLAP": "Prefer extending or differentiating from the top match; record the unique delta before creation.",
            "RELATED": "Creation can proceed if the unique responsibility boundary is explicit.",
            "DISTINCT": "No lexical collision strong enough to block creation; still inspect the top matches manually.",
        }[classification],
    }


def build_catalog(records: Sequence[ProjectRecord]) -> dict:
    ordered = sorted(records, key=lambda record: (record.name.casefold(), record.path.casefold()))
    return {
        "schema": SCHEMA,
        "project_count": len(ordered),
        "projects": [record.to_dict() for record in ordered],
    }


def render_markdown_report(result: dict) -> str:
    lines = [
        "# Supplemental Collision Guard Report",
        "",
        f"- Classification: **{result['classification']}**",
        f"- Top score: `{result['top_score']:.3f}`",
        f"- Candidate: `{result['candidate']['title']}`",
        "",
        result["decision_guidance"],
        "",
        "## Top matches",
        "",
        "| Score | Project | Shared tags | Shared terms |",
        "|---:|---|---|---|",
    ]
    for item in result["top_matches"]:
        lines.append(
            f"| {item['score']:.3f} | `{item['project']}` | "
            f"{', '.join(item['shared_tags']) or '-'} | {', '.join(item['shared_terms']) or '-'} |"
        )
    return "\n".join(lines) + "\n"


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Detect overlap between AI-CONTEXT supplemental projects.")
    sub = parser.add_subparsers(dest="command", required=True)

    scan = sub.add_parser("scan", help="Build a deterministic catalog of immediate supplemental project directories.")
    scan.add_argument("--root", required=True, type=Path)
    scan.add_argument("--output", type=Path)

    check = sub.add_parser("check", help="Check a proposed project against existing supplemental projects.")
    check.add_argument("--root", required=True, type=Path)
    check.add_argument("--title", required=True)
    check.add_argument("--summary", default="")
    check.add_argument("--tag", action="append", default=[])
    check.add_argument("--json-output", type=Path)
    check.add_argument("--markdown-output", type=Path)
    check.add_argument("--fail-at", choices=("RELATED", "HIGH_OVERLAP", "LIKELY_DUPLICATE"))

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        records = discover_projects(args.root)

        if args.command == "scan":
            catalog = build_catalog(records)
            if args.output:
                _write_json(args.output, catalog)
            else:
                print(json.dumps(catalog, ensure_ascii=False, indent=2, sort_keys=True))
            return 0

        candidate = Candidate(title=args.title, summary=args.summary, tags=tuple(args.tag))
        result = analyze_candidate(candidate, records)
    except ValueError as exc:
        parser.error(str(exc))
    if args.json_output:
        _write_json(args.json_output, result)
    if args.markdown_output:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(render_markdown_report(result), encoding="utf-8")
    if not args.json_output and not args.markdown_output:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    if args.fail_at and RISK_ORDER[result["classification"]] >= RISK_ORDER[args.fail_at]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
