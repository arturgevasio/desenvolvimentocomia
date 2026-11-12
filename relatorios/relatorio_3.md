# Relatório — Biblioteca pessoal — semana 3

## Viabilidade

- Grupo: Dupla 12
- Integrantes: Artur Gevasio Lira da Silva e João Vitor Bezerra Moura
- Specify: https://github.com/arturgevasio/desenvolvimentocomia/blob/main/spec/SPECIFY.md
- Plan: https://github.com/arturgevasio/desenvolvimentocomia/blob/main/spec/PLAN.md
- Tasks: https://github.com/arturgevasio/desenvolvimentocomia/blob/main/spec/TASKS.md
- Veredito: Atende os três arquivos; o código na `main` está fora deles

Os três arquivos abrem na `main`. A spec pede cadastro manual de título, autor, temática e posição, sqlite local, lista e busca por título ou temática, 100% offline, Tkinter. Capa, ISBN, API, edição e exclusão ficam de fora. O plano separa `database.py` e `gui.py`. As nove tarefas estão todas desmarcadas. No mesmo repositório, `BiblioMania/` já consulta ISBN, baixa capa, edita e exclui.

## SWOT

### Forças

O recorte cabe numa iteração: formulário, tabela `livros`, insert, lista e filtro. O “pronto” é abrir com `python src/main.py`, cadastrar e achar o livro, com a tabela criada na primeira execução. O que fica fora está numa lista, não numa frase solta.

### Fraquezas

Em SDD a spec manda no código. Aqui a spec descreve `src/database.py` e `src/gui.py`, e a `main` tem `BiblioMania/bibliomania/`, com `services.py` na Open Library. A task 03 fala em CRUD, enquanto a spec proíbe edição e exclusão. Nenhuma tarefa cita quem aprova a mudança de requisito. As caixas continuam vazias, então o backlog não registra o que já estaria feito.

### Oportunidades

Cada tarefa ainda pode virar um commit com o número no assunto: tabela, insert, formulário, lista, filtro, validação. O código de ISBN e capa sai da `main` ou entra numa spec futura, aprovada pelos dois, antes de permanecer.

### Ameaças

Tratar o `BiblioMania` atual como implementação desta spec quebra a semana 4: o commit não corresponde à tarefa. “Aplicação 100% funcional” no plano de pronto, somado a um repositório que já tem exclusão e API, puxa o escopo de volta.

## Stack técnica

**Parecer: A spec está adequada; o repositório não está.** Python, Tkinter e sqlite3 são a stack dos três arquivos. Não há chamada de API neles.

O código versionado acrescenta cliente HTTP da Open Library e Pillow para capa. Isso é outra stack, e a spec não a autorizou.

## Recomendação

**Mantenham a spec manual e façam o código da `main` caber nela, ou abram outra spec para ISBN e capa antes de deixar esse código valer.**

Entra formulário, sqlite e busca por título ou temática. Ficam fora capa, ISBN, edição e exclusão. As tarefas 01 a 09 seguem desmarcadas até existir o commit de cada uma. Task que não servir ao cadastro manual não é desta iteração.
