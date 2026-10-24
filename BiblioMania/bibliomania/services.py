from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from pathlib import Path

OPENLIBRARY_ISBN = "https://openlibrary.org/isbn/{isbn}.json"
OPENLIBRARY_COVER = "https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg"
USER_AGENT = "BiblioMania/0.1 (biblioteca pessoal)"


def normalize_isbn(raw: str) -> str:
    return re.sub(r"[^0-9Xx]", "", raw).upper()


def fetch_isbn_metadata(isbn: str, timeout: float = 8.0) -> dict[str, str]:
    """Consulta metadados na Open Library. Retorna dict vazio se não achar."""
    isbn = normalize_isbn(isbn)
    if not isbn:
        return {}
    req = urllib.request.Request(
        OPENLIBRARY_ISBN.format(isbn=isbn),
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError):
        return {}

    publishers = data.get("publishers") or []
    publisher = publishers[0] if publishers else ""
    year = str(data.get("publish_date") or "")
    authors = data.get("authors") or []
    author_names: list[str] = []
    for author in authors[:3]:
        key = author.get("key")
        if not key:
            continue
        name = _fetch_author_name(key, timeout)
        if name:
            author_names.append(name)

    return {
        "title": data.get("title") or "",
        "author": ", ".join(author_names),
        "publisher": publisher if isinstance(publisher, str) else "",
        "year": year,
        "isbn": isbn,
    }


def _fetch_author_name(author_key: str, timeout: float) -> str:
    url = f"https://openlibrary.org{author_key}.json"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data.get("name") or ""
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError):
        return ""


def download_cover(isbn: str, dest_dir: Path, timeout: float = 8.0) -> str:
    """Baixa a capa pelo ISBN. Retorna caminho relativo vazio se falhar."""
    isbn = normalize_isbn(isbn)
    if not isbn:
        return ""
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{isbn}.jpg"
    req = urllib.request.Request(
        OPENLIBRARY_COVER.format(isbn=isbn),
        headers={"User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = resp.read()
        if len(payload) < 800:
            return ""
        dest.write_bytes(payload)
        return str(dest)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
        return ""
