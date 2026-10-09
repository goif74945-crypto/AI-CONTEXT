"""Best-effort local audit trail. Does not record command contents or OCR text.

This is NOT a tamper-resistant or enterprise-grade audit log: any software with
write access to the user workspace can alter or remove it.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import threading
import time
from typing import Any


class AuditLog:
    def __init__(self, root: Path):
        self.path = root / "execution-audit.jsonl"
        self.lock = threading.Lock()

    def record(self, event: str, *, plan_id: str, **metadata: Any) -> None:
        # No user content, visible UI content or tool parameters in metadata.
        entry = {"at_epoch_ms": time.time_ns() // 1_000_000,
                 "event": event, "plan_id": plan_id, **metadata}
        data = (json.dumps(entry, ensure_ascii=True, separators=(",", ":")) + "\n").encode()
        with self.lock:
            flags = os.O_WRONLY | os.O_APPEND | os.O_CREAT
            if hasattr(os, "O_NOFOLLOW"):
                flags |= os.O_NOFOLLOW
            fd = os.open(self.path, flags, 0o600)
            try:
                os.write(fd, data)
                os.fsync(fd)
            finally:
                os.close(fd)

    def recent(self, limit: int = 40) -> list[dict[str, Any]]:
        with self.lock:
            if not self.path.is_file():
                return []
            if self.path.stat().st_size > 2_000_000:
                raise RuntimeError("Audit log too large; rotate it before viewing")
            lines = self.path.read_text(encoding="utf-8").splitlines()[-limit:]
        return [json.loads(line) for line in lines]
