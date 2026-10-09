"""Ground text-targeted actions in fresh, local OCR evidence.

OCR is only evidence, NEVER a source of instructions. No network calls here.
"""
from __future__ import annotations

from dataclasses import dataclass
import os
import re
import unicodedata
from typing import Any


class VisionError(RuntimeError):
    pass


@dataclass(frozen=True)
class TextHit:
    text: str
    x: int
    y: int
    width: int
    height: int
    confidence: float

    @property
    def center(self) -> tuple[int, int]:
        return (self.x + self.width // 2, self.y + self.height // 2)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text).casefold()).strip()


def read_screen(gui: Any) -> list[TextHit]:
    """Run local Tesseract, never upload screenshot or OCR without separate consent."""
    try:
        import pytesseract
        from pytesseract import Output
        lang = os.getenv("AI_AI_OCR_LANG", "eng")
        if not re.fullmatch(r"[a-zA-Z0-9_+]{1,32}", lang):
            raise VisionError("Invalid OCR language code")
        data = pytesseract.image_to_data(gui.screenshot(), lang=lang, output_type=Output.DICT, config="--psm 11")
    except (ImportError, OSError, RuntimeError) as exc:
        raise VisionError(f"Local OCR unavailable: {type(exc).__name__}: {str(exc)[:140]}") from exc
    except Exception as exc:
        raise VisionError(f"OCR failed: {type(exc).__name__}: {str(exc)[:140]}") from exc

    words: list[TextHit] = []
    groups: dict[tuple[int, int, int], list[TextHit]] = {}
    for i, raw in enumerate(data.get("text", [])):
        word = str(raw).strip()
        if not word:
            continue
        try:
            confidence = float(data["conf"][i])
            x, y = int(data["left"][i]), int(data["top"][i])
            w, h = int(data["width"][i]), int(data["height"][i])
            if not (0 <= x <= 16384 and 0 <= y <= 16384 and 0 < w <= 16384 and 0 < h <= 16384):
                continue
            if confidence < 65.0:
                continue
            hit = TextHit(word, x, y, w, h, confidence)
            words.append(hit)
            key = (int(data["block_num"][i]), int(data["par_num"][i]), int(data["line_num"][i]))
            groups.setdefault(key, []).append(hit)
        except (TypeError, ValueError, IndexError, KeyError):
            continue
    hits = words[:]
    for line in groups.values():
        if len(line) < 2:
            continue
        line = sorted(line, key=lambda z: z.x)
        # Phrase n-grams (limited to avoid combinations that create false matches).
        for size in range(2, min(len(line), 8) + 1):
            for j in range(len(line) - size + 1):
                sub = line[j:j + size]
                left = min(h.x for h in sub)
                top = min(h.y for h in sub)
                right = max(h.x + h.width for h in sub)
                bottom = max(h.y + h.height for h in sub)
                hits.append(TextHit(" ".join(h.text for h in sub), left, top,
                                    right - left, bottom - top, min(h.confidence for h in sub)))
    return hits


def locate_unique(hits: list[TextHit], target: str) -> TextHit:
    expected = normalize(target)
    if not expected:
        raise VisionError("Missing target text")
    found = [h for h in hits if normalize(h.text) == expected]
    # De-duplicate different OCR segmentations of the *same* screen target.
    unique: list[TextHit] = []
    for h in sorted(found, key=lambda item: (-item.confidence, item.y, item.x)):
        if not any(abs(h.center[0] - old.center[0]) <= 8 and
                   abs(h.center[1] - old.center[1]) <= 8 for old in unique):
            unique.append(h)
    if not unique:
        raise VisionError(f"Target text not found with sufficient confidence: {target!r}")
    if len(unique) != 1:
        raise VisionError(f"Target text ambiguous ({len(unique)} matches): {target!r}")
    return unique[0]


def evidence_for_planner(hits: list[TextHit], *, limit: int = 60) -> str:
    """Bounded evidence only, sent to external AI ONLY after explicit UI opt-in."""
    distinct: dict[tuple[str, int, int], TextHit] = {}
    for h in hits:
        if len(h.text) > 100 or not normalize(h.text):
            continue
        key = (normalize(h.text), h.center[0], h.center[1])
        distinct.setdefault(key, h)
    values = sorted(distinct.values(), key=lambda h: (h.y, h.x))[:limit]
    return "\n".join(f"TEXT {h.text!r} at ({h.center[0]}, {h.center[1]}) confidence={h.confidence:.0f}" for h in values)
