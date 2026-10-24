from __future__ import annotations

import sqlite3
from pathlib import Path

from bibliomania.models import Book

SCHEMA = """
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    isbn TEXT,
    title TEXT NOT NULL,
    author TEXT DEFAULT '',
    publisher TEXT DEFAULT '',
    year TEXT DEFAULT '',
    shelf TEXT NOT NULL,
    position TEXT NOT NULL,
    cover_path TEXT DEFAULT '',
    added_at TEXT NOT NULL,
    notes TEXT DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_books_isbn ON books(isbn);
CREATE INDEX IF NOT EXISTS idx_books_shelf ON books(shelf);
CREATE INDEX IF NOT EXISTS idx_books_title ON books(title);
"""


class LibraryDB:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(db_path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON")
        self._conn.executescript(SCHEMA)
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()

    def list_books(self, query: str = "") -> list[Book]:
        sql = """
            SELECT id, isbn, title, author, publisher, year, shelf, position,
                   cover_path, added_at, notes
            FROM books
        """
        params: tuple = ()
        if query.strip():
            like = f"%{query.strip()}%"
            sql += """
                WHERE title LIKE ? COLLATE NOCASE
                   OR author LIKE ? COLLATE NOCASE
                   OR isbn LIKE ?
                   OR shelf LIKE ? COLLATE NOCASE
                   OR position LIKE ? COLLATE NOCASE
            """
            params = (like, like, like, like, like)
        sql += " ORDER BY shelf, position, title"
        cur = self._conn.execute(sql, params)
        return [Book.from_row(tuple(row)) for row in cur.fetchall()]

    def get(self, book_id: int) -> Book | None:
        cur = self._conn.execute(
            """
            SELECT id, isbn, title, author, publisher, year, shelf, position,
                   cover_path, added_at, notes
            FROM books WHERE id = ?
            """,
            (book_id,),
        )
        row = cur.fetchone()
        return Book.from_row(tuple(row)) if row else None

    def insert(self, book: Book) -> int:
        cur = self._conn.execute(
            """
            INSERT INTO books (
                isbn, title, author, publisher, year, shelf, position,
                cover_path, added_at, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                book.isbn,
                book.title,
                book.author,
                book.publisher,
                book.year,
                book.shelf,
                book.position,
                book.cover_path,
                book.added_at or Book.now_local(),
                book.notes,
            ),
        )
        self._conn.commit()
        return int(cur.lastrowid)

    def update(self, book: Book) -> None:
        if book.id is None:
            raise ValueError("Livro sem id não pode ser atualizado")
        self._conn.execute(
            """
            UPDATE books SET
                isbn = ?, title = ?, author = ?, publisher = ?, year = ?,
                shelf = ?, position = ?, cover_path = ?, notes = ?
            WHERE id = ?
            """,
            (
                book.isbn,
                book.title,
                book.author,
                book.publisher,
                book.year,
                book.shelf,
                book.position,
                book.cover_path,
                book.notes,
                book.id,
            ),
        )
        self._conn.commit()

    def delete(self, book_id: int) -> None:
        self._conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
        self._conn.commit()

    def shelves(self) -> list[str]:
        cur = self._conn.execute(
            "SELECT DISTINCT shelf FROM books WHERE shelf != '' ORDER BY shelf"
        )
        return [row[0] for row in cur.fetchall()]
