#  Especificação do Recorte — Iteração 1: Cadastro Manual e Consulta Básica

## 1. Descrição do Recorte
Esta iteração contempla o desenvolvimento do fluxo principal (MVP) do sistema de gestão de biblioteca pessoal: o cadastro manual de livros físicos e a listagem/pesquisa local dos itens registados.

## 2. Comportamentos Esperados
- **Cadastro de Livro:** O utilizador deve conseguir preencher um formulário com Título, Autor, Temática e Posição na Estante (ex.: "Prateleira A2") e guardar no sistema.
- **Validação de Entrada:** O sistema impede o registo se Título, Autor ou Posição estiverem em branco.
- **Listagem e Pesquisa:** O sistema exibe os livros cadastrados em tabela/lista e permite filtrar por Título ou Temática.
- **Persistência Local:** Todos os dados gravados permanecem guardados no ficheiro SQLite local após fechar a aplicação.

## 3. Restrições Técnicas
- 100% offline (sem chamadas a APIs de terceiros).
- Interface construída exclusivamente com Tkinter nativo do Python.
- Banco de dados SQLite de ficheiro único local (`biblioteca.db`).

## 4. Definição de Pronto (Definition of Done)
- Aplicação abre sem erros via terminal (`python src/main.py`).
- É possível cadastrar, listar e pesquisar um livro com sucesso.
- O banco de dados SQLite cria a tabela automaticamente na primeira execução se ela não existir.

## 5. Explicitamente Fora de Escopo
- Busca automática de capa, edição ou ISBN via internet.
- Edição ou exclusão de livros já cadastrados (ficam para iterações futuras).
- Importação/Exportação de dados (CSV/JSON).