from modulos.conta import deposito

VALOR_POR_PONTO = 0.05  # 100 pontos = R$ 5,00


def calcular_pontos(valor):
    return int(valor // 10)


def consultar_pontos(pontos):
    return f"Você possui {pontos} BytePoints acumulados."


def resgatar_cashback(saldo, pontos, pontos_resgatar):
    if pontos_resgatar <= 0:
        return saldo, pontos, "Quantidade de pontos inválida."
    if pontos_resgatar > pontos:
        return saldo, pontos, "Você não possui pontos suficientes."

    valor_cashback = pontos_resgatar * VALOR_POR_PONTO
    saldo = deposito(saldo, valor_cashback)
    pontos -= pontos_resgatar
    return saldo, pontos, f"Cashback de R$ {valor_cashback:.2f} resgatado com {pontos_resgatar} pontos!"
