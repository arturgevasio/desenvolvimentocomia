from __future__ import annotations

from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageTk

from bibliomania.database import LibraryDB
from bibliomania.models import Book
from bibliomania.services import download_cover, fetch_isbn_metadata, normalize_isbn

PLACEHOLDER_SIZE = (160, 240)


class BookForm(tk.Toplevel):
    def __init__(
        self,
        master: tk.Tk,
        covers_dir: Path,
        book: Book | None = None,
        on_save=None,
    ) -> None:
        super().__init__(master)
        self.title("Editar livro" if book else "Novo livro")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.covers_dir = covers_dir
        self.book = book
        self.on_save = on_save
        self.cover_path = book.cover_path if book else ""

        pad = {"padx": 8, "pady": 4}
        form = ttk.Frame(self, padding=12)
        form.grid(row=0, column=0, sticky="nsew")

        self.vars = {
            "isbn": tk.StringVar(value=book.isbn if book else ""),
            "title": tk.StringVar(value=book.title if book else ""),
            "author": tk.StringVar(value=book.author if book else ""),
            "publisher": tk.StringVar(value=book.publisher if book else ""),
            "year": tk.StringVar(value=book.year if book else ""),
            "shelf": tk.StringVar(value=book.shelf if book else ""),
            "position": tk.StringVar(value=book.position if book else ""),
            "notes": tk.StringVar(value=book.notes if book else ""),
        }

        labels = [
            ("ISBN", "isbn"),
            ("Título *", "title"),
            ("Autor", "author"),
            ("Editora", "publisher"),
            ("Ano", "year"),
            ("Prateleira *", "shelf"),
            ("Posição *", "position"),
            ("Notas", "notes"),
        ]
        for i, (label, key) in enumerate(labels):
            ttk.Label(form, text=label).grid(row=i, column=0, sticky="e", **pad)
            ttk.Entry(form, textvariable=self.vars[key], width=42).grid(
                row=i, column=1, sticky="ew", **pad
            )

        btns = ttk.Frame(form)
        btns.grid(row=len(labels), column=0, columnspan=2, pady=(10, 0))
        ttk.Button(btns, text="Buscar ISBN", command=self._lookup_isbn).pack(
            side="left", padx=4
        )
        ttk.Button(btns, text="Escolher capa…", command=self._pick_cover).pack(
            side="left", padx=4
        )
        ttk.Button(btns, text="Salvar", command=self._save).pack(side="left", padx=4)
        ttk.Button(btns, text="Cancelar", command=self.destroy).pack(side="left", padx=4)

        self.bind("<Return>", lambda _e: self._save())
        self.bind("<Escape>", lambda _e: self.destroy())

    def _lookup_isbn(self) -> None:
        isbn = normalize_isbn(self.vars["isbn"].get())
        if not isbn:
            messagebox.showinfo("ISBN", "Informe um ISBN para buscar.", parent=self)
            return
        self.config(cursor="watch")
        self.update_idletasks()
        try:
            meta = fetch_isbn_metadata(isbn)
            cover = download_cover(isbn, self.covers_dir)
        finally:
            self.config(cursor="")
        if not meta and not cover:
            messagebox.showwarning(
                "ISBN",
                "Não foi possível obter dados da Open Library.",
                parent=self,
            )
            return
        if meta.get("title") and not self.vars["title"].get().strip():
            self.vars["title"].set(meta["title"])
        if meta.get("author") and not self.vars["author"].get().strip():
            self.vars["author"].set(meta["author"])
        if meta.get("publisher") and not self.vars["publisher"].get().strip():
            self.vars["publisher"].set(meta["publisher"])
        if meta.get("year") and not self.vars["year"].get().strip():
            self.vars["year"].set(meta["year"])
        self.vars["isbn"].set(isbn)
        if cover:
            self.cover_path = cover
        messagebox.showinfo("ISBN", "Dados preenchidos (quando disponíveis).", parent=self)

    def _pick_cover(self) -> None:
        path = filedialog.askopenfilename(
            parent=self,
            title="Escolher capa",
            filetypes=[
                ("Imagens", "*.jpg *.jpeg *.png *.webp *.gif"),
                ("Todos", "*.*"),
            ],
        )
        if path:
            self.cover_path = path

    def _save(self) -> None:
        title = self.vars["title"].get().strip()
        shelf = self.vars["shelf"].get().strip()
        position = self.vars["position"].get().strip()
        if not title or not shelf or not position:
            messagebox.showerror(
                "Campos obrigatórios",
                "Título, prateleira e posição são obrigatórios.",
                parent=self,
            )
            return
        book = Book(
            id=self.book.id if self.book else None,
            isbn=normalize_isbn(self.vars["isbn"].get()),
            title=title,
            author=self.vars["author"].get().strip(),
            publisher=self.vars["publisher"].get().strip(),
            year=self.vars["year"].get().strip(),
            shelf=shelf,
            position=position,
            cover_path=self.cover_path,
            added_at=self.book.added_at if self.book else Book.now_local(),
            notes=self.vars["notes"].get().strip(),
        )
        if self.on_save:
            self.on_save(book)
        self.destroy()


class BiblioManiaApp(tk.Tk):
    def __init__(self, root_dir: Path) -> None:
        super().__init__()
        self.title("BiblioMania — biblioteca pessoal")
        self.geometry("1100x620")
        self.minsize(900, 520)

        self.root_dir = root_dir
        self.data_dir = root_dir / "data"
        self.covers_dir = self.data_dir / "covers"
        self.covers_dir.mkdir(parents=True, exist_ok=True)
        self.db = LibraryDB(self.data_dir / "bibliomania.db")
        self._cover_photo: ImageTk.PhotoImage | None = None
        self._selected_id: int | None = None

        self._build()
        self.refresh()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build(self) -> None:
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        toolbar = ttk.Frame(self, padding=(10, 8))
        toolbar.grid(row=0, column=0, columnspan=2, sticky="ew")
        ttk.Label(toolbar, text="Buscar:").pack(side="left")
        self.search_var = tk.StringVar()
        search = ttk.Entry(toolbar, textvariable=self.search_var, width=36)
        search.pack(side="left", padx=6)
        search.bind("<KeyRelease>", lambda _e: self.refresh())
        ttk.Button(toolbar, text="Novo livro", command=self._new_book).pack(
            side="left", padx=4
        )
        ttk.Button(toolbar, text="Editar", command=self._edit_book).pack(
            side="left", padx=4
        )
        ttk.Button(toolbar, text="Excluir", command=self._delete_book).pack(
            side="left", padx=4
        )

        detail = ttk.Frame(self, padding=(10, 0, 10, 10))
        detail.grid(row=1, column=0, sticky="ns")
        ttk.Label(detail, text="Capa", font=("TkDefaultFont", 10, "bold")).pack(
            anchor="w"
        )
        self.cover_label = ttk.Label(detail, relief="groove", anchor="center")
        self.cover_label.pack(pady=8)
        self._set_cover("")

        self.detail_text = tk.Text(detail, width=28, height=14, wrap="word", state="disabled")
        self.detail_text.pack(fill="both", expand=True)

        table_frame = ttk.Frame(self, padding=(0, 0, 10, 10))
        table_frame.grid(row=1, column=1, sticky="nsew")
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        columns = ("title", "author", "isbn", "shelf", "position", "added_at")
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", selectmode="browse"
        )
        headings = {
            "title": ("Título", 240),
            "author": ("Autor", 160),
            "isbn": ("ISBN", 120),
            "shelf": ("Prateleira", 110),
            "position": ("Posição", 90),
            "added_at": ("Incluído em", 130),
        }
        for col, (text, width) in headings.items():
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, minwidth=70)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.bind("<Double-1>", lambda _e: self._edit_book())

        self.status = ttk.Label(self, text="", padding=(10, 4), relief="sunken", anchor="w")
        self.status.grid(row=2, column=0, columnspan=2, sticky="ew")

    def refresh(self) -> None:
        query = self.search_var.get()
        books = self.db.list_books(query)
        for item in self.tree.get_children():
            self.tree.delete(item)
        for book in books:
            self.tree.insert(
                "",
                "end",
                iid=str(book.id),
                values=(
                    book.title,
                    book.author,
                    book.isbn,
                    book.shelf,
                    book.position,
                    book.added_at,
                ),
            )
        suffix = "livro" if len(books) == 1 else "livros"
        self.status.config(text=f"{len(books)} {suffix}")
        if self._selected_id and str(self._selected_id) in self.tree.get_children():
            self.tree.selection_set(str(self._selected_id))
        elif books:
            self.tree.selection_set(str(books[0].id))
        else:
            self._show_book(None)

    def _on_select(self, _event=None) -> None:
        sel = self.tree.selection()
        if not sel:
            return
        book = self.db.get(int(sel[0]))
        self._selected_id = book.id if book else None
        self._show_book(book)

    def _show_book(self, book: Book | None) -> None:
        self._set_cover(book.cover_path if book else "")
        self.detail_text.configure(state="normal")
        self.detail_text.delete("1.0", "end")
        if book:
            lines = [
                book.title,
                "",
                f"Autor: {book.author or '—'}",
                f"ISBN: {book.isbn or '—'}",
                f"Editora: {book.publisher or '—'}",
                f"Ano: {book.year or '—'}",
                "",
                f"Prateleira: {book.shelf}",
                f"Posição: {book.position}",
                f"Incluído em: {book.added_at}",
            ]
            if book.notes:
                lines += ["", f"Notas: {book.notes}"]
            self.detail_text.insert("1.0", "\n".join(lines))
        self.detail_text.configure(state="disabled")

    def _set_cover(self, path: str) -> None:
        image = None
        if path and Path(path).is_file():
            try:
                image = Image.open(path)
                image.thumbnail(PLACEHOLDER_SIZE)
            except OSError:
                image = None
        if image is None:
            image = Image.new("RGB", PLACEHOLDER_SIZE, "#d9d9d9")
        self._cover_photo = ImageTk.PhotoImage(image)
        self.cover_label.configure(image=self._cover_photo)

    def _current_book(self) -> Book | None:
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Seleção", "Selecione um livro na lista.")
            return None
        return self.db.get(int(sel[0]))

    def _new_book(self) -> None:
        BookForm(self, self.covers_dir, on_save=self._save_new)

    def _save_new(self, book: Book) -> None:
        new_id = self.db.insert(book)
        self._selected_id = new_id
        self.refresh()

    def _edit_book(self) -> None:
        book = self._current_book()
        if not book:
            return
        BookForm(self, self.covers_dir, book=book, on_save=self._save_edit)

    def _save_edit(self, book: Book) -> None:
        self.db.update(book)
        self._selected_id = book.id
        self.refresh()

    def _delete_book(self) -> None:
        book = self._current_book()
        if not book:
            return
        if not messagebox.askyesno(
            "Excluir", f"Excluir “{book.title}” da biblioteca?"
        ):
            return
        self.db.delete(book.id)  # type: ignore[arg-type]
        self._selected_id = None
        self.refresh()

    def _on_close(self) -> None:
        self.db.close()
        self.destroy()


def run() -> None:
    root_dir = Path(__file__).resolve().parent.parent
    app = BiblioManiaApp(root_dir)
    app.mainloop()
