from modulos.conta import deposito, saque


def buscar_conta(contas, cpf):
    for conta in contas:
        if conta["cpf"] == cpf:
            return conta

    return None


def transferir_pix(contas, cpf_origem, cpf_destino, valor):
    if cpf_origem == cpf_destino:
        return contas, False, "Não é possível transferir para a própria conta."

    conta_origem = buscar_conta(contas, cpf_origem)
    conta_destino = buscar_conta(contas, cpf_destino)

    if conta_origem is None or conta_destino is None:
        return contas, False, "CPF de origem ou destino não encontrado."
    if valor <= 0:
        return contas, False, "Valor de transferência inválido."
    if valor > conta_origem["saldo"]:
        return contas, False, "Saldo insuficiente para a transferência."

    conta_origem["saldo"] = saque(conta_origem["saldo"], valor)
    conta_destino["saldo"] = deposito(conta_destino["saldo"], valor)

    return contas, True, f"Transferência de R$ {valor:.2f} para {cpf_destino} realizada com sucesso!"


def mascarar_cpf(cpf):
    return f"{cpf[:3]}.***.***-{cpf[-2:]}"


def mostrar_contas(contas, cpf_atual):
    if not contas:
        return "Nenhuma conta cadastrada."

    linhas = ["\n--- Contas Cadastradas ---"]
    for conta in contas:
        indicador = " (você)" if conta["cpf"] == cpf_atual else ""
        linhas.append(f"CPF {mascarar_cpf(conta['cpf'])}: R$ {conta['saldo']:.2f}{indicador}")

    return "\n".join(linhas)
