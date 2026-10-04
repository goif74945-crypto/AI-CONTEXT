from __future__ import annotations

import hashlib
import unittest

from nexy_proofgraph.graph import extract_link_edges, impact_closure, resolve_link
from nexy_proofgraph.model import Document


def doc(path: str, text: str) -> Document:
    raw = text.encode()
    return Document(path, hashlib.sha256(raw).hexdigest(), len(raw), "md", text)


class GraphTests(unittest.TestCase):
    def test_relative_link_resolution(self):
        self.assertEqual(resolve_link("a/b.md", "../c.md#x"), "c.md")

    def test_impact_walks_reverse_dependencies(self):
        docs = [
            doc("a.md", "[b](b.md)"),
            doc("b.md", "[c](c.md)"),
            doc("c.md", "leaf"),
        ]
        impact = impact_closure(extract_link_edges(docs), ["c.md"])
        self.assertEqual(impact, {"c.md": 0, "b.md": 1, "a.md": 2})

    def test_external_links_are_not_edges(self):
        docs = [doc("a.md", "[web](https://example.com) [mail](mailto:a@example.com)")]
        self.assertEqual(extract_link_edges(docs), [])


if __name__ == "__main__":
    unittest.main()
