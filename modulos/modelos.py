from modulos.usuarios import validar_cpf


class Cliente:
    def __init__(self, cpf, nome, contatos=None):
        cpf_numerico = "".join(caractere for caractere in cpf if caractere.isdigit())
        if not validar_cpf(cpf_numerico):
            raise ValueError("CPF inválido.")

        self.cpf = cpf_numerico
        self.nome = nome
        self.contatos = dict(contatos or {})

    def adicionar_contato(self, tipo, valor):
        self.contatos[tipo] = valor

    def consultar_contatos(self):
        if not self.contatos:
            return "Nenhum contato cadastrado."
        return "\n".join(f"{tipo}: {valor}" for tipo, valor in self.contatos.items())


class ContaCorrente:
    def __init__(self, id_cliente, saldo=0.0, limite=0.0):
        self.id_cliente = id_cliente
        self.saldo = saldo
        self.limite = limite

    def sacar(self, valor):
        if valor <= 0:
            return "Valor de saque inválido."
        if valor > self.saldo + self.limite:
            return "Saldo e limite insuficientes."

        self.saldo -= valor
        return f"Saque de R$ {valor:.2f} realizado com sucesso!"

    def depositar(self, valor):
        if valor <= 0:
            return "Valor de depósito inválido."

        self.saldo += valor
        return f"Depósito de R$ {valor:.2f} realizado com sucesso!"

    def consultar_saldo(self):
        return self.saldo

    def consultar_limite(self):
        return self.limite

    def aumentar_limite(self, valor):
        if valor <= 0:
            return "Valor de aumento inválido."

        self.limite += valor
        return f"Limite aumentado para R$ {self.limite:.2f}."


class CartaoCredito:
    def __init__(self, nome, numero, validade, cvv, limite, data_pagamento):
        self.nome = nome
        self.numero = numero
        self.validade = validade
        self.cvv = cvv
        self.limite = limite
        self.data_pagamento = data_pagamento
        self.saldo = 0.0  # valor da fatura em aberto
        self.parcelas = []

    def consultar_limite(self):
        return self.limite - self.saldo

    def consultar_saldo(self):
        return self.saldo

    def comprar(self, valor):
        if valor <= 0:
            return "Valor de compra inválido."
        if valor > self.consultar_limite():
            return "Limite de crédito insuficiente."

        self.saldo += valor
        return f"Compra de R$ {valor:.2f} realizada no crédito!"

    def pagar(self, valor):
        if valor <= 0:
            return "Valor de pagamento inválido."
        if valor > self.saldo:
            return "Valor maior que a fatura em aberto."

        self.saldo -= valor
        return f"Pagamento de R$ {valor:.2f} realizado! Limite restabelecido."

    def parcelar_saldo(self, quantidade_parcelas, juros_mensal=0.0):
        if self.saldo <= 0:
            return "Não há saldo para parcelar."
        if quantidade_parcelas < 1:
            return "Quantidade de parcelas inválida."

        total = self.saldo * (1 + juros_mensal) ** quantidade_parcelas
        valor_parcela = round(total / quantidade_parcelas, 2)
        self.parcelas = [valor_parcela] * quantidade_parcelas
        return f"Saldo parcelado em {quantidade_parcelas}x de R$ {valor_parcela:.2f}."
