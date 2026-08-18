from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


@dataclass
class MemoryItem:
    kind: str
    content: str
    confidence: float = 0.5


class MemoryStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.items: list[MemoryItem] = []
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            self.items = [MemoryItem(**item) for item in data.get("items", [])]
        except (OSError, json.JSONDecodeError, TypeError):
            self.items = []

    def add(self, kind: str, content: str, confidence: float = 0.5) -> None:
        self.items.append(MemoryItem(kind=kind, content=content, confidence=confidence))
        self.items = self.items[-200:]
        self.save()

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload: dict[str, Any] = {"items": [asdict(item) for item in self.items]}
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def relevant(self, limit: int = 12) -> list[MemoryItem]:
        return self.items[-limit:]

    def as_text(self, limit: int = 12) -> str:
        items = self.relevant(limit)
        if not items:
            return "Ainda não há memórias persistentes registradas."
        return "\n".join(f"- [{item.kind}] {item.content}" for item in items)
