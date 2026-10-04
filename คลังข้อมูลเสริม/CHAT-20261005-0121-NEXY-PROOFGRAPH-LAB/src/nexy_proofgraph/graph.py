from __future__ import annotations

import posixpath
import re
from collections import defaultdict, deque
from pathlib import PurePosixPath
from urllib.parse import unquote

from .model import Document, Edge

_MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


def _clean_link(raw: str) -> str | None:
    target = raw.strip()
    if not target:
        return None
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    target = target.split("#", 1)[0].strip()
    target = target.split("?", 1)[0].strip()
    if not target or "://" in target or target.startswith(("mailto:", "data:", "#")):
        return None
    return unquote(target)


def resolve_link(source: str, raw_target: str) -> str | None:
    cleaned = _clean_link(raw_target)
    if cleaned is None:
        return None
    if cleaned.startswith("/"):
        return posixpath.normpath(cleaned.lstrip("/"))
    base = str(PurePosixPath(source).parent)
    return posixpath.normpath(posixpath.join(base, cleaned))


def extract_link_edges(documents: list[Document]) -> list[Edge]:
    edges: list[Edge] = []
    for doc in documents:
        for line_no, line in enumerate(doc.text.splitlines(), start=1):
            for match in _MD_LINK_RE.finditer(line):
                target = resolve_link(doc.path, match.group(1))
                if target:
                    edges.append(Edge(doc.path, target, "markdown-link", line_no))
    return edges


def build_reverse_index(edges: list[Edge]) -> dict[str, set[str]]:
    reverse: dict[str, set[str]] = defaultdict(set)
    for edge in edges:
        reverse[edge.target].add(edge.source)
    return reverse


def impact_closure(edges: list[Edge], changed: list[str], max_depth: int = 32) -> dict[str, int]:
    """Return files that may be affected by changed files, keyed by minimum reverse-link distance."""
    reverse = build_reverse_index(edges)
    distance: dict[str, int] = {}
    queue: deque[tuple[str, int]] = deque()
    for raw in changed:
        item = posixpath.normpath(raw.replace("\\", "/"))
        distance[item] = 0
        queue.append((item, 0))

    while queue:
        node, depth = queue.popleft()
        if depth >= max_depth:
            continue
        for parent in sorted(reverse.get(node, ())):
            next_depth = depth + 1
            old = distance.get(parent)
            if old is None or next_depth < old:
                distance[parent] = next_depth
                queue.append((parent, next_depth))
    return dict(sorted(distance.items(), key=lambda item: (item[1], item[0])))
