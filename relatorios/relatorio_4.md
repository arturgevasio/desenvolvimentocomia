# Relatório — Biblioteca pessoal — semana 4

## Viabilidade

- Grupo: Dupla 12
- Integrantes: Artur Gevasio Lira da Silva e João Vitor Bezerra Moura
- Repositório: https://github.com/arturgevasio/desenvolvimentocomia
- Links enviados: commits `c4346ef`, `cfc5d62`, `3c30c85` e `f4c705a`, e o PR 1 (https://github.com/arturgevasio/desenvolvimentocomia/pull/1)
- Veredito: Não atende a rastreabilidade

A semana pede tasks da semana 3, depois commits ou pull requests, depois o código, depois o estado da tela. Os quatro commits e o PR 1 foram abertos. Nenhum deles implementa as tarefas 01 a 09.

O PR 1 está fechado e incorporado. O título é “adição da constituicion”. O único arquivo é o PDF da constitution. `c4346ef` é o merge desse PR. `cfc5d62` é o mesmo PDF, enviado por upload. `3c30c85` cria o `README.md`. `f4c705a`, mensagem “chor: specs”, adiciona `spec/SPECIFY.md`, `spec/PLAN.md` e `spec/TASKS.md`. São documentos, não o cadastro.

## SWOT

### Forças

Os endereços abrem. Dá para ver o arquivo de cada um. O README da raiz descreve o `BiblioMania`: Tkinter, sqlite3, ISBN e capa pela Open Library.

### Fraquezas

Nenhuma mensagem cita Task 01 a Task 09. O código da aplicação está noutro commit, `06b6ec0`, “Add files via upload”, anterior a esses links e fora da entrega. Esse upload não segue a spec: inclui ISBN, consulta à Open Library, edição, exclusão, `__pycache__` e o arquivo `bibliomania.db`. A spec marcava API, edição e exclusão como fora. O estado atual no PDF da semana 4 não diz qual tela salva e qual busca responde, e os commits também não dizem.

### Oportunidades

A trilha que a semana pede ainda cabe em poucos commits, com o id da tarefa no assunto: tabela, formulário, insert, lista, filtro. O que a spec deixou fora permanece fora, ou ganha spec nova antes de voltar à `main`.

### Ameaças

Apresentar o PR da constitution como implementação faz a semana 4 parecer entregue. O código de capa e ISBN, sem tarefa correspondente, fica sem revisão humana amarrada a um critério.

## Stack técnica

**Parecer: O código não é a stack da spec.** A spec da semana 3 é Python, Tkinter e sqlite3, sem rede. O `BiblioMania` na `main` acrescenta Open Library e Pillow. Os commits citados não registram essa troca nem a justificam.

Pathlib aparece em `database.py`, `gui.py` e `services.py` como caminho local de capa baixada. A constitution aceitava isso só se a capa já existisse. O serviço baixa a capa.

## Recomendação

**Refaçam a trilha: cada tarefa do cadastro manual com um commit identificado, e o estado atual escrito a partir do que a tela faz.**

Os quatro SHAs e o PR 1 documentam constitution, README e spec. Não substituem a implementação. Edição, exclusão, ISBN e capa não entram nessa lista enquanto a spec da semana 3 os deixar de fora. Um exemplo de trecho gerado com IA, aceito, recusado ou reescrito, fecha a revisão que a semana pede.
