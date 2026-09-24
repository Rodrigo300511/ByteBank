# 🏦 ByteBank — FinTech em Python (Projeto AED)

Projeto Prático Avaliativo da disciplina de Algoritmo e Estrutura de Dados (BD015): uma FinTech simulada em **Python**, com menu interativo via terminal e persistência em **SQLite**.

## 👥 Equipe

* Rodrigo Aguiar
* Kiara Souza

## 🧩 Níveis do projeto

| Nível | Requisito | Onde está |
|---|---|---|
| 1 — Básico | Menu (`while`), depósito e saque com validação de saldo | [ByteBank.py](ByteBank.py) (opções 1-3), [modulos/conta.py](modulos/conta.py) |
| 2 — Múltiplas Contas | Contas em memória (lista de dicionários) e transferência PIX | [modulos/pix.py](modulos/pix.py) (opções 22-23) |
| 3 — Estruturas Lineares | Extrato, Estorno (TAD Pilha) e Fila de Pagamentos Agendados (TAD Fila) | [modulos/extrato.py](modulos/extrato.py), [modulos/estorno.py](modulos/estorno.py), [modulos/agendamentos.py](modulos/agendamentos.py) (opções 24-28) |
| Bônus | Cofrinhos, categorização de gastos, cartão de crédito, câmbio, fidelidade/cashback, empréstimos | Ver "Funcionalidades" abaixo |

## 📌 Funcionalidades

* 🔐 Cadastro e login por CPF (com validação do dígito verificador) e senha com hash seguro
* 💾 Persistência em banco de dados SQLite: os dados de cada usuário sobrevivem entre execuções do programa
* 💰 Depósito e saque em conta corrente
* 💸 Transferência PIX entre contas cadastradas, e listagem das contas do banco
* 📄 Extrato unificado com todas as movimentações da conta
* ↩️ Estorno/Desfazer da última operação (depósito, saque ou PIX), usando uma pilha
* 📅 Fila de pagamentos agendados (agendar e processar na ordem de chegada)
* 🏷️ Categorização de gastos no saque (Alimentação, Transporte, Lazer, Contas, Outros)
* 📊 Relatório de gastos por categoria (agregação + percentual do total)
* 🐷 Cofrinhos/caixinhas de investimento, com simulação de rendimento mensal
* 💳 Cartão de crédito: compras, pagamento de fatura e consulta de limite
* 💱 Carteira multimoedas (USD, EUR, BTC) com compra e venda pela taxa de câmbio
* 🎁 Programa de fidelidade (BytePoints) com resgate em cashback
* 🏦 Empréstimos pré-aprovados, com simulação, contratação e pagamento parcelado
* ⚠️ Validações de valores inválidos, saldo/limite insuficiente em todas as operações
* 🔄 Menu interativo em loop, até a opção de sair

## 📁 Estrutura do projeto

O projeto é dividido em um **script principal** (a interface de terminal) e um **pacote de módulos** (a lógica de negócio), separados para facilitar manutenção e a adição de novas funcionalidades:

```text
ByteBank/
│
├── ByteBank.py          # Ponto de entrada: tela de login/cadastro, menu e input/print
├── modulos/
│   ├── __init__.py
│   ├── banco_dados.py    # Conexão SQLite e criação das tabelas (schema)
│   ├── usuarios.py       # Cadastro/login: validação de CPF e hash de senha
│   ├── repositorio.py    # Camada de acesso a dados: carrega/salva o estado de cada usuário no banco
│   ├── conta.py          # Depósito, saque e consulta de saldo (usada por todos os outros módulos)
│   ├── cofrinhos.py      # Criar/guardar/resgatar caixinhas e simular rendimento
│   ├── categorias.py     # Lista de categorias e relatório agregado de gastos
│   ├── cartao_credito.py # Compra no crédito, pagamento e consulta de fatura
│   ├── cambio.py         # Taxas de câmbio, compra/venda de moeda estrangeira
│   ├── fidelidade.py     # Cálculo de BytePoints e resgate de cashback
│   ├── emprestimos.py    # Simulação, contratação e pagamento de empréstimos
│   ├── pix.py            # Múltiplas contas em memória (lista de dicionários) e transferência PIX
│   ├── extrato.py        # Formatação do extrato unificado de movimentações
│   ├── estorno.py        # Estorno/Desfazer da última operação (TAD Pilha)
│   └── agendamentos.py   # Fila de pagamentos agendados (TAD Fila)
├── bytebank.db           # Banco SQLite (criado automaticamente na 1ª execução; não versionado)
└── README.md
```

### Por que essa divisão?

* **`ByteBank.py`** cuida só de interface: mostra as telas, lê o `input()` do usuário e decide qual função chamar. Ele não sabe *como* cada operação funciona por dentro.
* **`conta.py`, `cofrinhos.py`, `categorias.py`, `cartao_credito.py`, `cambio.py`, `fidelidade.py` e `emprestimos.py`** contêm só a regra de negócio de cada domínio: recebem valores simples (números, dicionários, listas), calculam e **retornam** o resultado + uma mensagem — nenhuma delas usa `print()`, lê `input()` ou conhece o banco de dados. Isso as torna testáveis isoladamente e reutilizáveis em qualquer interface (terminal, web, testes automatizados).
* **`banco_dados.py`** e **`repositorio.py`** são a camada de persistência: sabem *onde* e *como* os dados são guardados (SQLite), mas não sabem nada sobre regras de saldo/limite/juros. `ByteBank.py` busca o estado do usuário logado no `repositorio`, passa para a função de negócio correspondente, e salva o resultado de volta — as duas camadas nunca se misturam.
* **`usuarios.py`** isola tudo relacionado a autenticação (validação de CPF e hash de senha), separado das regras bancárias.
* Módulos que precisam somar/subtrair valores (`cofrinhos`, `cartao_credito`, `cambio`, `fidelidade`, `emprestimos`, `pix`, `estorno`, `agendamentos`) importam e reaproveitam `deposito()`/`saque()` de `conta.py`, em vez de duplicar a conta.
* **`pix.py`** materializa as contas como uma **lista de dicionários** (`[{"cpf": ..., "saldo": ...}, ...]`) carregada do banco, faz uma **busca linear** nessa lista para achar origem/destino e move o valor entre os dois dicionários — é a estrutura "múltiplas contas em memória" pedida no Nível 2, mesmo com o SQLite persistindo o resultado depois.
* **`estorno.py`** implementa o TAD **Pilha**: `ByteBank.py` mantém uma lista `pilha_desfazer` só da sessão atual, empilhando (`append`) cada operação reversível; "Desfazer" desempilha (`pop()`) a mais recente e a reverte.
* **`agendamentos.py`** implementa o TAD **Fila**: os pagamentos agendados entram no fim da lista (`append`) e são processados sempre pelo início (`pop(0)`) — ordem de chegada (FIFO).

## 🔐 Cadastro, login e segurança

Antes de acessar o menu bancário, o usuário passa por uma tela de acesso:

```text
===== BYTEBANK =====
1 - Entrar
2 - Criar conta
3 - Sair
```

* **Cadastro:** pede CPF e senha. O CPF é validado pelo algoritmo real do dígito verificador (rejeita CPFs com formato ou dígitos inválidos, incluindo sequências como `111.111.111-11`); a senha precisa ter pelo menos 6 caracteres.
* **Senha com segurança:** a senha nunca é guardada em texto puro. É gerada uma *salt* aleatória por usuário (`secrets.token_bytes`) e o hash é calculado com **PBKDF2-HMAC-SHA256** (100 mil iterações) — tudo com a biblioteca padrão do Python, sem dependências externas. No login, a comparação do hash usa `hmac.compare_digest` para evitar *timing attacks*.
* **Login:** autentica pelo CPF (aceita com ou sem pontuação/traço — só os dígitos são considerados) e a senha. Cada usuário só enxerga e altera os próprios dados.
* Todos os dados da conta (saldo, caixinhas, histórico de gastos, fatura, carteira de moedas, BytePoints, empréstimo, extrato e pagamentos agendados) ficam vinculados ao CPF no banco `bytebank.db` e continuam disponíveis da próxima vez que o usuário fizer login — mesmo depois de fechar o programa. A única exceção é a pilha de desfazer, que existe só durante a sessão atual.

## 🖥️ Menu

Depois de entrar ou criar a conta, o usuário verá o menu principal:

```text
===== BANCO =====
1 - Depósito
2 - Saque
3 - Saldo
4 - Criar Caixinha
5 - Guardar na Caixinha
6 - Resgatar da Caixinha
7 - Ver Caixinhas
8 - Simular Rendimento das Caixinhas
9 - Relatório de Gastos por Categoria
10 - Comprar no Crédito
11 - Pagar Fatura
12 - Ver Fatura
13 - Comprar Moeda Estrangeira
14 - Vender Moeda Estrangeira
15 - Ver Carteira de Moedas
16 - Consultar BytePoints
17 - Resgatar Cashback
18 - Simular Empréstimo
19 - Contratar Empréstimo
20 - Pagar Parcela do Empréstimo
21 - Ver Empréstimo
22 - Transferir PIX
23 - Ver Contas
24 - Extrato
25 - Desfazer Última Operação
26 - Agendar Pagamento
27 - Ver Pagamentos Agendados
28 - Processar Próximo Pagamento Agendado
29 - Sair
```

O programa continua funcionando em loop até que o usuário escolha a opção **29 - Sair**.

## ▶️ Como executar

É necessário ter o **Python 3** instalado no computador.

No terminal, acesse a pasta raiz do projeto (a que contém `ByteBank.py` e a pasta `modulos/`) e execute:

```bash
python ByteBank.py
```

Caso o comando acima não funcione, tente:

```bash
python3 ByteBank.py
```

Nenhuma dependência externa é necessária — `sqlite3`, `hashlib`, `hmac` e `secrets` fazem parte da biblioteca padrão do Python. Na primeira execução, o arquivo `bytebank.db` é criado automaticamente na pasta do projeto (ele fica fora do controle de versão, veja `.gitignore`).

## 📚 Conceitos praticados

Durante o desenvolvimento do projeto foram praticados os seguintes conceitos:

* Variáveis e funções com **`def`** / **`return`**
* Estruturas condicionais: **`if`** / **`elif`** / **`else`**, incluindo condicionais encadeadas
* Estruturas de repetição: **`while`** / **`for`** / **`break`**
* Estruturas lineares: **listas**, **listas de dicionários** (múltiplas contas, com busca linear), **TAD Pilha** (`append`/`pop()` para o estorno) e **TAD Fila** (`append`/`pop(0)` para os pagamentos agendados e para as parcelas de empréstimo)
* Agregação de dados com dicionários (simulando um `GROUP BY` em memória)
* Cálculos financeiros simples (juros simples, percentuais, parcelamento)
* Organização de código em **módulos e pacotes** (`import`)
* Funções puras (sem efeito colateral de I/O) separadas da camada de apresentação e da camada de dados
* Banco de dados relacional com **SQLite** (`CREATE TABLE`, `INSERT`, `UPDATE`, `DELETE`, `SELECT`, chaves estrangeiras)
* Autenticação: hash de senha com salt (**PBKDF2-HMAC-SHA256**) e comparação em tempo constante (`hmac.compare_digest`)
* Validação de CPF pelo algoritmo do dígito verificador (módulo 11)
* F-strings, `input()`, `print()`, `int()`, `float()`

## 🎯 Objetivo

O objetivo deste projeto é praticar Algoritmos e Estruturas de Dados através de uma FinTech simulada, evoluindo de operações básicas de conta (Nível 1) para múltiplas contas com transferência PIX (Nível 2) e estruturas lineares como Pilha e Fila (Nível 3) — além de um conjunto de módulos financeiros bônus — mantendo o código organizado para facilitar manutenção futura.

---
