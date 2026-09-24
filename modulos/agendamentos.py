from modulos.conta import saque


def agendar_pagamento(fila_pagamentos, descricao, valor):
    if valor <= 0:
        return "Valor de pagamento inválido."

    fila_pagamentos.append({"descricao": descricao, "valor": valor})
    return f"Pagamento de R$ {valor:.2f} ({descricao}) agendado com sucesso!"


def mostrar_pagamentos_agendados(fila_pagamentos):
    if not fila_pagamentos:
        return "Não há pagamentos agendados."

    linhas = ["\n--- Pagamentos Agendados ---"]
    for posicao, pagamento in enumerate(fila_pagamentos, start=1):
        linhas.append(f"{posicao}º - {pagamento['descricao']}: R$ {pagamento['valor']:.2f}")

    return "\n".join(linhas)


def processar_proximo_pagamento(saldo, fila_pagamentos):
    if not fila_pagamentos:
        return saldo, "Não há pagamentos agendados para processar."

    proximo_pagamento = fila_pagamentos[0]

    if proximo_pagamento["valor"] > saldo:
        return saldo, "Saldo insuficiente para processar o próximo pagamento agendado."

    fila_pagamentos.pop(0)
    saldo = saque(saldo, proximo_pagamento["valor"])
    return saldo, f"Pagamento de R$ {proximo_pagamento['valor']:.2f} ({proximo_pagamento['descricao']}) processado!"
