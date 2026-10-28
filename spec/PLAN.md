#  Plano de Implementação — Iteração 1

## 1. Arquitetura da Solução
A aplicação seguirá uma arquitetura em duas camadas simples (Interface + Persistência):
- `src/database.py`: Módulo SQLite para criação da tabela, inserção (`INSERT`) e consulta (`SELECT`).
- `src/gui.py`: Interface Tkinter contendo o formulário de cadastro e a tabela de listagem (`ttk.Treeview`).
- `src/main.py`: Ponto de entrada da aplicação.

## 2. Ordem das Etapas Principais
1. **Modelagem do Banco (`database.py`):** Criar função de inicialização da tabela `livros` (campos: `id`, `titulo`, `autor`, `tematica`, `posicao`).
2. **Camada de Dados:** Implementar `salvar_livro()` e `listar_livros(filtro=None)`.
3. **Interface Gráfica (`gui.py`):** Desenhar o formulário com `Entry` e a tabela com `ttk.Treeview`.
4. **Integração e Eventos:** Conectar o botão "Salvar" e o campo de busca com o módulo de banco de dados.
5. **Testes de Integração:** Validar funcionamento sem conexão e persistência dos dados.

## 3. Riscos e Pontos de Atenção
- **Tratamento de exceções no SQLite:** Garantir que erros de conexão com o ficheiro local sejam capturados sem travar a interface.
- **Usabilidade do Tkinter:** Manter layout responsivo simples para evitar sobreposição de botões em ecrãs menores.