from modulos.conta import deposito, saque

TAXAS_CAMBIO = {"USD": 5.50, "EUR": 6.00, "BTC": 350000.0}


def comprar_moeda_estrangeira(saldo, saldos_moedas, moeda, valor_brl):
    if moeda not in TAXAS_CAMBIO:
        return saldo, "Moeda não suportada."
    if valor_brl <= 0:
        return saldo, "Valor inválido."
    if valor_brl > saldo:
        return saldo, "Saldo insuficiente."

    quantidade = valor_brl / TAXAS_CAMBIO[moeda]
    saldo = saque(saldo, valor_brl)
    saldos_moedas[moeda] = deposito(saldos_moedas[moeda], quantidade)
    return saldo, f"Compra de {quantidade:.6f} {moeda} realizada por R$ {valor_brl:.2f}!"


def vender_moeda_estrangeira(saldo, saldos_moedas, moeda, quantidade):
    if moeda not in TAXAS_CAMBIO:
        return saldo, "Moeda não suportada."
    if quantidade <= 0:
        return saldo, "Quantidade inválida."
    if quantidade > saldos_moedas[moeda]:
        return saldo, f"Você não possui {moeda} suficiente."

    valor_brl = quantidade * TAXAS_CAMBIO[moeda]
    saldos_moedas[moeda] = saque(saldos_moedas[moeda], quantidade)
    saldo = deposito(saldo, valor_brl)
    return saldo, f"Venda de {quantidade:.6f} {moeda} realizada por R$ {valor_brl:.2f}!"


def mostrar_carteira(saldos_moedas):
    if not any(saldos_moedas.values()):
        return "Você ainda não possui moedas estrangeiras."

    linhas = ["\n--- Carteira de Moedas ---"]
    for moeda, quantidade in saldos_moedas.items():
        valor_em_reais = quantidade * TAXAS_CAMBIO[moeda]
        linhas.append(f"{moeda}: {quantidade:.6f} (R$ {valor_em_reais:.2f})")

    return "\n".join(linhas)
