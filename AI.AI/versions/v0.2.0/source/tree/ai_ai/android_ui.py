"""Android UIAutomator XML is passive observation, not instructions."""
from __future__ import annotations
import re
from xml.etree import ElementTree
from .vision import normalize, VisionError


MAX_XML = 2_000_000
BOUNDS = re.compile(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]")


def locate_android(xml: str, label: str) -> tuple[int, int]:
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
    centers = set()
    for node in root.iter("node"):
        if not any(normalize(node.attrib.get(key, "")) == normalize(label)
                   for key in ("text", "content-desc")):
            continue
        bounds = BOUNDS.fullmatch(node.attrib.get("bounds", ""))
        if not bounds:
            continue
        x1, y1, x2, y2 = map(int, bounds.groups())
        if x1 < x2 and y1 < y2 and x2 <= 16384 and y2 <= 16384:
            centers.add(((x1 + x2) // 2, (y1 + y2) // 2))
    if len(centers) != 1:
        raise VisionError(f"Android target requires exactly one match, found {len(centers)}: {label!r}")
    return next(iter(centers))
