# 🏦 ByteBank — Sistema Bancário em Python

Projeto desenvolvido em **Python** para praticar Algoritmos e Estruturas de Dados (AED) através da criação de um sistema bancário simulado, com menu interativo via terminal e persistência em **SQLite**.

## 📌 Funcionalidades

* 🔐 Cadastro e login por CPF (com validação do dígito verificador) e senha com hash seguro
* 💾 Persistência em banco de dados SQLite: os dados de cada usuário sobrevivem entre execuções do programa
* 💰 Depósito e saque em conta corrente
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
│   └── emprestimos.py    # Simulação, contratação e pagamento de empréstimos
├── bytebank.db           # Banco SQLite (criado automaticamente na 1ª execução; não versionado)
└── README.md
```

### Por que essa divisão?

* **`ByteBank.py`** cuida só de interface: mostra as telas, lê o `input()` do usuário e decide qual função chamar. Ele não sabe *como* cada operação funciona por dentro.
* **`conta.py`, `cofrinhos.py`, `categorias.py`, `cartao_credito.py`, `cambio.py`, `fidelidade.py` e `emprestimos.py`** contêm só a regra de negócio de cada domínio: recebem valores simples (números, dicionários, listas), calculam e **retornam** o resultado + uma mensagem — nenhuma delas usa `print()`, lê `input()` ou conhece o banco de dados. Isso as torna testáveis isoladamente e reutilizáveis em qualquer interface (terminal, web, testes automatizados).
* **`banco_dados.py`** e **`repositorio.py`** são a camada de persistência: sabem *onde* e *como* os dados são guardados (SQLite), mas não sabem nada sobre regras de saldo/limite/juros. `ByteBank.py` busca o estado do usuário logado no `repositorio`, passa para a função de negócio correspondente, e salva o resultado de volta — as duas camadas nunca se misturam.
* **`usuarios.py`** isola tudo relacionado a autenticação (validação de CPF e hash de senha), separado das regras bancárias.
* Módulos que precisam somar/subtrair valores (`cofrinhos`, `cartao_credito`, `cambio`, `fidelidade`, `emprestimos`) importam e reaproveitam `deposito()`/`saque()` de `conta.py`, em vez de duplicar a conta.

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
* Todos os dados da conta (saldo, caixinhas, histórico de gastos, fatura, carteira de moedas, BytePoints e empréstimo) ficam vinculados ao CPF no banco `bytebank.db` e continuam disponíveis da próxima vez que o usuário fizer login — mesmo depois de fechar o programa.

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
22 - Sair
```

O programa continua funcionando em loop até que o usuário escolha a opção **22 - Sair**.

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
* Dicionários (simples e aninhados) e listas de dicionários
* Agregação de dados com dicionários (simulando um `GROUP BY` em memória)
* Cálculos financeiros simples (juros simples, percentuais, parcelamento)
* Organização de código em **módulos e pacotes** (`import`)
* Funções puras (sem efeito colateral de I/O) separadas da camada de apresentação e da camada de dados
* Banco de dados relacional com **SQLite** (`CREATE TABLE`, `INSERT`, `UPDATE`, `DELETE`, `SELECT`, chaves estrangeiras)
* Autenticação: hash de senha com salt (**PBKDF2-HMAC-SHA256**) e comparação em tempo constante (`hmac.compare_digest`)
* Validação de CPF pelo algoritmo do dígito verificador (módulo 11)
* F-strings, `input()`, `print()`, `int()`, `float()`

## 🎯 Objetivo

O objetivo deste projeto é praticar Algoritmos e Estruturas de Dados através de um sistema bancário simulado, evoluindo de operações básicas (depósito/saque/saldo) para um conjunto de módulos financeiros mais completo — mantendo o código organizado para facilitar manutenção futura.

---
