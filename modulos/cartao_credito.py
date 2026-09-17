from modulos.conta import deposito, saque


def comprar_no_credito(limite_disponivel, saldo_fatura, valor, estabelecimento):
    if valor <= 0:
        return limite_disponivel, saldo_fatura, "Valor de compra inválido."
    if valor > limite_disponivel:
        return limite_disponivel, saldo_fatura, "Limite de crédito insuficiente."

    limite_disponivel = saque(limite_disponivel, valor)
    saldo_fatura = deposito(saldo_fatura, valor)
    return limite_disponivel, saldo_fatura, f"Compra de R$ {valor:.2f} em '{estabelecimento}' realizada no crédito!"


def pagar_fatura(saldo, limite_disponivel, saldo_fatura):
    if saldo_fatura <= 0:
        return saldo, limite_disponivel, saldo_fatura, "Não há fatura para pagar."
    if saldo_fatura > saldo:
        return saldo, limite_disponivel, saldo_fatura, "Saldo insuficiente para quitar a fatura."

    valor_pago = saldo_fatura
    saldo = saque(saldo, valor_pago)
    limite_disponivel = deposito(limite_disponivel, valor_pago)
    saldo_fatura = 0.0
    return saldo, limite_disponivel, saldo_fatura, f"Fatura de R$ {valor_pago:.2f} paga com sucesso! Limite restabelecido."


def mostrar_fatura(limite_credito, limite_disponivel, saldo_fatura):
    return (
        f"Limite total: R$ {limite_credito:.2f}\n"
        f"Limite disponível: R$ {limite_disponivel:.2f}\n"
        f"Saldo da fatura: R$ {saldo_fatura:.2f}"
    )
