# BiblioMania

Sistema de gestão de biblioteca pessoal em Python, com GUI Tkinter e banco SQLite local.

## Como executar

```bash
cd ~/Projects/BiblioMania
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -m bibliomania
```

Pillow é necessário para exibir capas (JPEG/PNG) na interface.

## Estrutura

```
BiblioMania/
├── bibliomania/
│   ├── __main__.py      # python -m bibliomania
│   ├── models.py        # dataclass Book
│   ├── database.py      # SQLite local (CRUD)
│   ├── services.py      # ISBN + download de capas (Open Library)
│   └── gui.py           # interface Tkinter
└── data/
    ├── bibliomania.db   # criado na primeira execução
    └── covers/          # capas baixadas por ISBN
```

## O que o sistema registra

| Campo        | Uso |
|--------------|-----|
| ISBN         | identificação e busca de capa/metadados |
| Título/autor | catálogo |
| Prateleira   | onde o livro está (ex.: Sala A, Estante 2) |
| Posição      | lugar na prateleira (ex.: 3ª, esquerda) |
| Capa         | arquivo local (download por ISBN ou escolha manual) |
| Incluído em  | data/hora de cadastro |

A busca filtra por título, autor, ISBN, prateleira e posição.

**Buscar ISBN** preenche título/autor/editora quando a Open Library tiver o registro, e tenta baixar a capa.
