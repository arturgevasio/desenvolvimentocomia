from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Book:
    id: int | None
    isbn: str
    title: str
    author: str
    publisher: str
    year: str
    shelf: str
    position: str
    cover_path: str
    added_at: str
    notes: str = ""

    @classmethod
    def from_row(cls, row: tuple) -> Book:
        return cls(
            id=row[0],
            isbn=row[1] or "",
            title=row[2] or "",
            author=row[3] or "",
            publisher=row[4] or "",
            year=row[5] or "",
            shelf=row[6] or "",
            position=row[7] or "",
            cover_path=row[8] or "",
            added_at=row[9] or "",
            notes=row[10] or "",
        )

    @staticmethod
    def now_local() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M")
