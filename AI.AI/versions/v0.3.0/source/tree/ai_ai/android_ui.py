"""Android UIAutomator XML is passive observation, not instructions."""
from __future__ import annotations
import re
from xml.etree import ElementTree
from .vision import normalize, VisionError


MAX_XML = 2_000_000
BOUNDS = re.compile(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]")


def locate_android(xml: str, label: str, *, for_click: bool = False) -> tuple[int, int]:
    if len(xml.encode('utf-8')) > MAX_XML:
        raise VisionError("Android UI hierarchy exceeds size limit")
    if "<!DOCTYPE" in xml.upper() or "<!ENTITY" in xml.upper():
        raise VisionError("Android XML entity definitions are not accepted")
    try:
        root = ElementTree.fromstring(xml)
    except ElementTree.ParseError as exc:
        raise VisionError("Invalid Android UI hierarchy XML") from exc
    if not normalize(label):
        raise VisionError("Empty Android UI target")
    centers: set[tuple[int,int]] = set()
    expected = normalize(label)
    def walk(node, parents):
        path = parents + (node,)
        if node.tag == "node" and any(normalize(node.attrib.get(key, "")) == expected
                   for key in ("text", "content-desc")):
            if (not for_click or all(p.attrib.get("enabled", "true").lower() != "false" for p in path)):
                # Text children are often not tappable. Prefer their closest
                # clickable parent while preserving the exact unique label.
                target = next((p for p in reversed(path) if p.attrib.get("clickable") == "true"), node) if for_click else node
                bounds = BOUNDS.fullmatch(target.attrib.get("bounds", ""))
                if bounds:
                    x1,y1,x2,y2 = map(int,bounds.groups())
                    if 0 <= x1 < x2 <= 16384 and 0 <= y1 < y2 <= 16384:
                        centers.add(((x1+x2)//2,(y1+y2)//2))
        for child in node:
            walk(child, path)
    walk(root, ())
    if len(centers) != 1:
        raise VisionError(f"Android target requires exactly one match, found {len(centers)}: {label!r}")
    return next(iter(centers))
