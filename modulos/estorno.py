from modulos.conta import deposito, saque


def desfazer_ultima_operacao(saldo, pilha_desfazer):
    if not pilha_desfazer:
        return saldo, None, "Não há operações para desfazer."

    operacao = pilha_desfazer.pop()
    tipo = operacao["tipo"]
    valor = operacao["valor"]

    if tipo == "deposito":
        return saque(saldo, valor), None, f"Depósito de R$ {valor:.2f} desfeito."

    if tipo == "saque":
        return deposito(saldo, valor), None, f"Saque de R$ {valor:.2f} desfeito."

    if tipo == "pix":
        cpf_destino = operacao["cpf_destino"]
        return deposito(saldo, valor), (cpf_destino, valor), f"PIX de R$ {valor:.2f} para {cpf_destino} estornado."

    return saldo, None, "Operação desconhecida, não foi possível desfazer."
