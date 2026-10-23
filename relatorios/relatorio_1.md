# Relatório — Biblioteca pessoal

## Viabilidade

- Grupo: Dupla 12
- Integrantes: Artur Gevasio Lira da Silva e João Vitor Bezerra Moura
- Repositório: https://github.com/arturgevasio/desenvolvimentocomia
- Stack: Python, Tkinter, sqlite3 e pathlib, no Cursor.
- Veredito: Viável com correção

O aplicativo em si cabe: cadastrar livros, tema e posição na estante, para quem tem mais de 35 volumes. A justificativa erra a ferramenta: pathlib manipula caminho de arquivo local e não busca capa, ISBN nem edição.

## SWOT

### Forças

Usuário e limite estão definidos. Interface de desktop, banco local e privacidade combinam com o uso. Python e Tkinter mantêm o projeto em um processo só. A IDE escolhida é a do curso.

### Fraquezas

O texto mistura duas coisas. Buscar capa, ISBN ou ficha do livro numa fonte externa é metadado automático. Isso foi colocado num módulo que não é o responsável por essa busca.

### Oportunidades

O caminho mais seguro para o primeiro recorte é cadastrar o livro à mão. Capa e ISBN podem vir depois, numa consulta à Open Library. Se o livro não for encontrado, o cadastro segue sem capa, em vez de falhar. pathlib entra só se existir uma pasta local de imagens de capa. Não é a base do sistema.

### Ameaças

Se todo livro depender de uma API de fora, a aplicação para quando não há rede, e a spec fica refém desse serviço.

## Stack técnica

**Parecer: Adequada com correção.** Python, Tkinter e sqlite3 estão adequados; pathlib não busca ISBN nem capa, então essa função sai da stack.

Para um cadastro local de livros, Python com interface Tkinter e banco sqlite3 é uma stack enxuta e suficiente. O programa abre numa janela, grava título, autor, tema e prateleira, e funciona sem servidor e sem internet. Cursor como IDE também combina com a disciplina. Não há razão para migrar a web.

O erro está no pathlib. Esse módulo manipula caminho de arquivo no computador. Ele não consulta edição, capa nem ISBN. A stack recomendada é Python, Tkinter e sqlite3. Se a dupla quiser metadado externo, entra um cliente HTTP para uma API nomeada, como a Open Library, e o cadastro manual continua válido quando a rede falhar. pathlib só guarda o caminho de uma capa já baixada.

## Recomendação

**Cadastrem os livros manualmente no sqlite e tratem ISBN e capa como acréscimo posterior, porque pathlib não busca esses dados.**

A biblioteca pessoal é um bom escopo de disciplina: quem tem muitos livros cadastra título, autor, tema e a posição na estante, e depois encontra a obra sem vasculhar a sala. A constitution precisa corrigir um equívoco da justificativa. O módulo pathlib organiza caminhos de arquivo no computador; ele não consulta ISBN, capa nem edição. O cadastro do MVP é manual e fica no sqlite, o que também preserva o uso sem internet. Se a dupla quiser capa ou ISBN, isso vem de uma API nomeada, por exemplo a Open Library, e o cadastro continua possível quando a rede falhar. O pathlib só aparece se existir uma pasta local para guardar as capas já baixadas. 
