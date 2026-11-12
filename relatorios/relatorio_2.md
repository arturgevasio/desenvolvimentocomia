# Relatório — Biblioteca pessoal — semana 2

## Viabilidade

- Grupo: Dupla 12
- Integrantes: Artur Gevasio Lira da Silva e João Vitor Bezerra Moura
- Link enviado: https://github.com/arturgevasio/desenvolvimentocomia/blob/main/CONSTITUTION.md
- Arquivo que está no repositório: `constituicion/Constituição do Projeto — Biblioteca Pessoal (DSAIA).pdf`, na `main`, incorporado pelo PR 1
- Veredito: Parcial

O `CONSTITUTION.md` citado não abre. O arquivo que existe é um PDF, numa pasta com o nome grafado `constituicion`. Ele não está em branco: nomeia os dois integrantes, fixa cadastro manual e consulta local, tira ISBN, câmera e nuvem do escopo, corrige o pathlib para caminho de arquivo local e exige spec antes de código e pull request aprovado pelo outro integrante. Não diz o que o agente de IA pode versionar sozinho.

## SWOT

### Forças

O PDF registra a correção da semana 1: Python, Tkinter e sqlite3, com pathlib só para pasta local de capa. A `main` não recebe commit direto. O merge depende da revisão do outro integrante. O escopo offline está escrito, não só prometido.

### Fraquezas

A trilha SDD desta semana pede o arquivo da constitution, com quem aprova a spec, quem aprova o merge e o que o agente versiona. O link enviado não abre. Quem aprova a spec não está nomeado como os dois antes do desenvolvimento. A faixa do agente não existe: não há o que ele pode commitar numa branch e o que exige diff humano. As regras misturam produto e processo, e a revisão de pull request fica genérica.

### Oportunidades

O mesmo PDF já tem o recorte certo para três regras de agente: não consultar ISBN nem capa sem a dupla autorizar; não alterar spec sozinho; não fazer merge. Isso cabe num `CONSTITUTION.md` na raiz da `main`, no lugar do PDF.

### Ameaças

O código que já está na `main`, em `BiblioMania/`, consulta a Open Library e baixa capa. A constitution diz que API externa está fora do escopo. Sem a faixa do agente, esse código entra como se a spec já o tivesse autorizado.

## Stack técnica

**Parecer: A constitution corrige a stack; o código ao lado dela não obedece.** O PDF deixa Python, Tkinter, sqlite3 e Cursor, e limita pathlib a arquivo local. Essa parte está alinhada à semana 1.

O repositório, no mesmo `main`, já tem `services.py` com Open Library para ISBN e capa. A constitution não escolheu essa consulta. Ela a deixou para depois.

## Recomendação

**Publiquem um `CONSTITUTION.md` na `main`, com os dois aprovando a spec, um aprovando o merge do outro, e a faixa do agente: texto e teste na branch, sem ISBN, sem capa e sem merge.**

O PDF pode permanecer como rascunho. O link da entrega tem de abrir nesse arquivo. Enquanto o código da Open Library estiver na `main`, a constitution e o repositório dizem coisas diferentes.
