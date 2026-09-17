from modulos.conta import deposito, saque

TAXA_JUROS_EMPRESTIMO = 0.05  # 5% sobre o valor emprestado


def simular_emprestimo(saldo, valor, parcelas):
    limite_emprestimo = saldo * 3

    if valor <= 0 or parcelas <= 0:
        return "Valor ou número de parcelas inválido."
    if valor > limite_emprestimo:
        return f"Valor solicitado excede o limite disponível de R$ {limite_emprestimo:.2f}."

    valor_total = valor * (1 + TAXA_JUROS_EMPRESTIMO)
    valor_parcela = valor_total / parcelas

    return (
        f"Simulação de Empréstimo:\n"
        f"Valor solicitado: R$ {valor:.2f}\n"
        f"Total a pagar (juros de {TAXA_JUROS_EMPRESTIMO * 100:.0f}%): R$ {valor_total:.2f}\n"
        f"{parcelas}x de R$ {valor_parcela:.2f}"
    )


def contratar_emprestimo(saldo, divida_emprestimo, parcelas_emprestimo, valor, parcelas):
    limite_emprestimo = saldo * 3

    if valor <= 0 or parcelas <= 0:
        return saldo, divida_emprestimo, "Valor ou número de parcelas inválido."
    if valor > limite_emprestimo:
        return saldo, divida_emprestimo, f"Valor solicitado excede o limite disponível de R$ {limite_emprestimo:.2f}."

    valor_total = valor * (1 + TAXA_JUROS_EMPRESTIMO)
    valor_parcela = valor_total / parcelas

    saldo = deposito(saldo, valor)
    divida_emprestimo = deposito(divida_emprestimo, valor_total)
    parcelas_emprestimo.extend([valor_parcela] * parcelas)

    return saldo, divida_emprestimo, f"Empréstimo de R$ {valor:.2f} aprovado! {parcelas}x de R$ {valor_parcela:.2f}."


def pagar_parcela_emprestimo(saldo, divida_emprestimo, parcelas_emprestimo):
    if not parcelas_emprestimo:
        return saldo, divida_emprestimo, "Não há parcelas pendentes."

    valor_parcela = parcelas_emprestimo[0]

    if valor_parcela > saldo:
        return saldo, divida_emprestimo, "Saldo insuficiente para pagar a parcela."

    saldo = saque(saldo, valor_parcela)
    divida_emprestimo = saque(divida_emprestimo, valor_parcela)
    parcelas_emprestimo.pop(0)

    return saldo, divida_emprestimo, f"Parcela de R$ {valor_parcela:.2f} paga! Parcelas restantes: {len(parcelas_emprestimo)}."


def mostrar_emprestimo(divida_emprestimo, parcelas_emprestimo):
    if not parcelas_emprestimo:
        return "Você não possui empréstimos ativos."

    return (
        f"Dívida total restante: R$ {divida_emprestimo:.2f}\n"
        f"Parcelas pendentes: {len(parcelas_emprestimo)} de R$ {parcelas_emprestimo[0]:.2f}"
    )
