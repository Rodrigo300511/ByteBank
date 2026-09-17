from modulos.conta import deposito, saque


def criar_cofrinho(cofrinhos, nome_caixinha):
    if nome_caixinha in cofrinhos:
        return "Já existe uma caixinha com esse nome."

    cofrinhos[nome_caixinha] = 0.0
    return f"Caixinha '{nome_caixinha}' criada com sucesso!"


def guardar_no_cofrinho(saldo, cofrinhos, nome_caixinha, valor):
    if nome_caixinha not in cofrinhos:
        return saldo, "Essa caixinha não existe."
    if valor <= 0:
        return saldo, "Valor inválido."
    if valor > saldo:
        return saldo, "Saldo insuficiente."

    saldo = saque(saldo, valor)
    cofrinhos[nome_caixinha] = deposito(cofrinhos[nome_caixinha], valor)
    return saldo, f"R$ {valor:.2f} guardado na caixinha '{nome_caixinha}'!"


def resgatar_do_cofrinho(saldo, cofrinhos, nome_caixinha, valor):
    if nome_caixinha not in cofrinhos:
        return saldo, "Essa caixinha não existe."
    if valor <= 0:
        return saldo, "Valor inválido."
    if valor > cofrinhos[nome_caixinha]:
        return saldo, "Saldo insuficiente na caixinha."

    cofrinhos[nome_caixinha] = saque(cofrinhos[nome_caixinha], valor)
    saldo = deposito(saldo, valor)
    return saldo, f"R$ {valor:.2f} resgatado da caixinha '{nome_caixinha}'!"


def mostrar_cofrinhos(cofrinhos):
    if not cofrinhos:
        return "Você ainda não tem nenhuma caixinha."

    linhas = [f"{nome}: R$ {valor:.2f}" for nome, valor in cofrinhos.items()]
    return "\n--- Suas Caixinhas ---\n" + "\n".join(linhas)


def simular_rendimento(cofrinhos, taxa=0.005):
    if not cofrinhos:
        return "Você ainda não tem nenhuma caixinha."

    for nome in cofrinhos:
        rendimento = cofrinhos[nome] * taxa
        cofrinhos[nome] = deposito(cofrinhos[nome], rendimento)

    return f"Rendimento de {taxa * 100:.2f}% aplicado em todas as caixinhas!"
