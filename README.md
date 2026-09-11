# 🏦 Sistema Bancário em Python

Projeto desenvolvido em **Python** para praticar conceitos básicos de programação através da criação de um sistema bancário simples.

## 📌 Funcionalidades

* 💰 Depósito de valores
* 💸 Saque de valores
* 💳 Consulta de saldo
* ⚠️ Validação de valores inválidos
* 🚫 Verificação de saldo insuficiente
* 🔄 Menu interativo em loop
* ❌ Opção para sair do programa

## 🖥️ Menu

Ao iniciar o programa, o usuário verá o seguinte menu:

```text
===== BANCO =====
1 - Depósito
2 - Saque
3 - Saldo
4 - Sair
```

O programa continuará funcionando até que o usuário escolha a opção **4 - Sair**.

## 💰 Depósito

O usuário informa o valor que deseja depositar.

O programa verifica se o valor é maior que zero. Caso seja válido, o valor é adicionado ao saldo.

Exemplo:

```text
Digite o valor do depósito: 500
Depósito realizado com sucesso!
```

## 💸 Saque

O usuário informa o valor que deseja sacar.

O programa verifica:

* Se o valor é maior que zero.
* Se o saldo é suficiente para realizar o saque.

Caso o saldo seja insuficiente, o saque não será realizado.

Exemplo:

```text
Digite o valor do saque: 100
Saque realizado com sucesso!
```

Caso o saldo seja insuficiente:

```text
Saldo insuficiente!
```

## 💳 Consulta de saldo

A opção de saldo mostra o valor disponível na conta.

Exemplo:

```text
Seu saldo é de: R$ 500.00
```

## 🔄 Loop do programa

O sistema utiliza um loop **`while`** para manter o menu funcionando.

```python
while True:
    # Menu do sistema
```

O programa só é encerrado quando o usuário escolhe a opção **4**, utilizando:

```python
break
```

## 🧩 Funções

O projeto utiliza funções para organizar e reaproveitar o código.

### Depósito

```python
def deposito(saldo, valor_deposito):
    return saldo + valor_deposito
```

A função recebe o saldo atual e o valor do depósito e retorna o novo saldo.

### Saque

```python
def saque(saldo, valor_saque):
    return saldo - valor_saque
```

A função recebe o saldo atual e o valor do saque e retorna o saldo após a retirada.

### Saldo

```python
def mostrar_saldo(saldo):
    return saldo
```

A função recebe o saldo e retorna o seu valor atual.

## 📚 Conceitos praticados

Durante o desenvolvimento do projeto foram praticados os seguintes conceitos de Python:

* Variáveis
* Funções com **`def`**
* Parâmetros
* **`return`**
* **`if`**
* **`elif`**
* **`else`**
* **`while`**
* **`break`**
* **`input()`**
* **`print()`**
* **`int()`**
* **`float()`**
* Operadores matemáticos
* Operadores de comparação
* F-strings

## ▶️ Como executar

É necessário ter o **Python** instalado no computador.

No terminal, acesse a pasta do projeto e execute:

```bash
python ByteBank.py
```

Caso o comando acima não funcione, tente:

```bash
python3 ByteBank.py
```

## 📁 Estrutura do projeto

A estrutura básica do projeto é:

```text
sistema-bancario/
│
├── ByteBank.py
└── README.md
```

### `ByteBank.py`

Contém o código principal do sistema bancário.

### `README.md`

Contém a documentação e as informações sobre o projeto.

## 🎯 Objetivo

O objetivo deste projeto é praticar os fundamentos da programação em Python através da criação de um sistema bancário simples, utilizando **funções, condicionais e estruturas de repetição**.

---

## 🚀 Próximos passos

Algumas funcionalidades que podem ser adicionadas futuramente:

* 📋 Extrato bancário
* 🔢 Limite de saques
* 👤 Cadastro de usuários
* 🏦 Múltiplas contas
* 🔐 Sistema de login
* 💾 Salvamento dos dados
* 📊 Histórico de transações
