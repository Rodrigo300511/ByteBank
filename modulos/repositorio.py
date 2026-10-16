import secrets
from datetime import date

from modulos.banco_dados import obter_conexao
from modulos.cambio import TAXAS_CAMBIO
from modulos.modelos import CartaoCredito, Cliente, ContaCorrente


def carregar_conta(cpf):
    conexao = obter_conexao()
    linha = conexao.execute(
        "SELECT saldo, limite_credito, limite_disponivel, saldo_fatura, pontos_bytepoints, divida_emprestimo, "
        "limite_conta FROM usuarios WHERE cpf = ?",
        (cpf,),
    ).fetchone()

    saldo, limite_credito, limite_disponivel, saldo_fatura, pontos_bytepoints, divida_emprestimo, limite_conta = linha
    return {
        "limite_conta": limite_conta,
        "saldo": saldo,
        "limite_credito": limite_credito,
        "limite_disponivel": limite_disponivel,
        "saldo_fatura": saldo_fatura,
        "pontos_bytepoints": pontos_bytepoints,
        "divida_emprestimo": divida_emprestimo,
    }


def salvar_conta(cpf, **campos):
    if not campos:
        return

    conexao = obter_conexao()
    # As chaves de `campos` vêm só de chamadas internas (nomes de coluna fixos),
    # nunca de entrada do usuário, então montar o SET por f-string aqui é seguro.
    atribuicoes = ", ".join(f"{campo} = ?" for campo in campos)
    valores = list(campos.values()) + [cpf]
    conexao.execute(f"UPDATE usuarios SET {atribuicoes} WHERE cpf = ?", valores)
    conexao.commit()


def carregar_caixinhas(cpf):
    conexao = obter_conexao()
    linhas = conexao.execute("SELECT nome, valor FROM caixinhas WHERE cpf = ?", (cpf,)).fetchall()
    return {nome: valor for nome, valor in linhas}


def salvar_caixinhas(cpf, caixinhas):
    conexao = obter_conexao()
    for nome, valor in caixinhas.items():
        conexao.execute(
            "INSERT INTO caixinhas (cpf, nome, valor) VALUES (?, ?, ?) "
            "ON CONFLICT(cpf, nome) DO UPDATE SET valor = excluded.valor",
            (cpf, nome, valor),
        )
    conexao.commit()


def registrar_gasto(cpf, categoria, valor):
    conexao = obter_conexao()
    conexao.execute(
        "INSERT INTO historico_gastos (cpf, categoria, valor) VALUES (?, ?, ?)",
        (cpf, categoria, valor),
    )
    conexao.commit()


def carregar_historico_gastos(cpf):
    conexao = obter_conexao()
    linhas = conexao.execute(
        "SELECT categoria, valor FROM historico_gastos WHERE cpf = ?", (cpf,)
    ).fetchall()
    return [{"categoria": categoria, "valor": valor} for categoria, valor in linhas]


def registrar_compra_credito(cpf, estabelecimento, valor):
    conexao = obter_conexao()
    conexao.execute(
        "INSERT INTO historico_credito (cpf, estabelecimento, valor) VALUES (?, ?, ?)",
        (cpf, estabelecimento, valor),
    )
    conexao.commit()


def carregar_saldos_moedas(cpf):
    conexao = obter_conexao()
    saldos = {moeda: 0.0 for moeda in TAXAS_CAMBIO}
    linhas = conexao.execute(
        "SELECT moeda, quantidade FROM saldos_moedas WHERE cpf = ?", (cpf,)
    ).fetchall()
    saldos.update(dict(linhas))
    return saldos


def salvar_saldos_moedas(cpf, saldos_moedas):
    conexao = obter_conexao()
    for moeda, quantidade in saldos_moedas.items():
        conexao.execute(
            "INSERT INTO saldos_moedas (cpf, moeda, quantidade) VALUES (?, ?, ?) "
            "ON CONFLICT(cpf, moeda) DO UPDATE SET quantidade = excluded.quantidade",
            (cpf, moeda, quantidade),
        )
    conexao.commit()


def carregar_parcelas(cpf):
    conexao = obter_conexao()
    linhas = conexao.execute(
        "SELECT valor FROM parcelas_emprestimo WHERE cpf = ? ORDER BY id ASC", (cpf,)
    ).fetchall()
    return [valor for (valor,) in linhas]


def adicionar_parcelas(cpf, valores):
    conexao = obter_conexao()
    conexao.executemany(
        "INSERT INTO parcelas_emprestimo (cpf, valor) VALUES (?, ?)",
        [(cpf, valor) for valor in valores],
    )
    conexao.commit()


def remover_proxima_parcela(cpf):
    conexao = obter_conexao()
    linha = conexao.execute(
        "SELECT id FROM parcelas_emprestimo WHERE cpf = ? ORDER BY id ASC LIMIT 1", (cpf,)
    ).fetchone()

    if linha:
        conexao.execute("DELETE FROM parcelas_emprestimo WHERE id = ?", (linha[0],))
        conexao.commit()


def listar_contas():
    conexao = obter_conexao()
    linhas = conexao.execute("SELECT cpf, saldo, limite_conta FROM usuarios").fetchall()
    return [{"cpf": cpf, "saldo": saldo, "limite_conta": limite} for cpf, saldo, limite in linhas]


def registrar_extrato(cpf, tipo, descricao, valor):
    conexao = obter_conexao()
    conexao.execute(
        "INSERT INTO extrato (cpf, tipo, descricao, valor) VALUES (?, ?, ?, ?)",
        (cpf, tipo, descricao, valor),
    )
    conexao.commit()


def carregar_extrato(cpf):
    conexao = obter_conexao()
    linhas = conexao.execute(
        "SELECT tipo, descricao, valor FROM extrato WHERE cpf = ? ORDER BY id ASC", (cpf,)
    ).fetchall()
    return [{"tipo": tipo, "descricao": descricao, "valor": valor} for tipo, descricao, valor in linhas]


def carregar_pagamentos_agendados(cpf):
    conexao = obter_conexao()
    linhas = conexao.execute(
        "SELECT descricao, valor FROM pagamentos_agendados WHERE cpf = ? ORDER BY id ASC", (cpf,)
    ).fetchall()
    return [{"descricao": descricao, "valor": valor} for descricao, valor in linhas]


def adicionar_pagamento_agendado(cpf, descricao, valor):
    conexao = obter_conexao()
    conexao.execute(
        "INSERT INTO pagamentos_agendados (cpf, descricao, valor) VALUES (?, ?, ?)",
        (cpf, descricao, valor),
    )
    conexao.commit()


def remover_proximo_pagamento_agendado(cpf):
    conexao = obter_conexao()
    linha = conexao.execute(
        "SELECT id FROM pagamentos_agendados WHERE cpf = ? ORDER BY id ASC LIMIT 1", (cpf,)
    ).fetchone()

    if linha:
        conexao.execute("DELETE FROM pagamentos_agendados WHERE id = ?", (linha[0],))
        conexao.commit()


def carregar_cliente(cpf):
    conexao = obter_conexao()
    (nome,) = conexao.execute("SELECT nome FROM usuarios WHERE cpf = ?", (cpf,)).fetchone()
    linhas = conexao.execute("SELECT tipo, valor FROM contatos WHERE cpf = ? ORDER BY id ASC", (cpf,)).fetchall()
    return Cliente(cpf, nome, dict(linhas))


def salvar_cliente(cliente):
    conexao = obter_conexao()
    conexao.execute("UPDATE usuarios SET nome = ? WHERE cpf = ?", (cliente.nome, cliente.cpf))
    for tipo, valor in cliente.contatos.items():
        conexao.execute(
            "INSERT INTO contatos (cpf, tipo, valor) VALUES (?, ?, ?) "
            "ON CONFLICT(cpf, tipo) DO UPDATE SET valor = excluded.valor",
            (cliente.cpf, tipo, valor),
        )
    conexao.commit()


def carregar_conta_corrente(cpf):
    dados = carregar_conta(cpf)
    return ContaCorrente(cpf, dados["saldo"], dados["limite_conta"])


def salvar_conta_corrente(conta_corrente):
    salvar_conta(conta_corrente.id_cliente, saldo=conta_corrente.saldo, limite_conta=conta_corrente.limite)


def carregar_cartao(cpf):
    conexao = obter_conexao()
    linha = conexao.execute(
        "SELECT numero, validade, cvv, data_pagamento FROM cartoes WHERE cpf = ?", (cpf,)
    ).fetchone()

    if linha is None:
        # Cartão emitido na primeira consulta, com dados gerados localmente.
        hoje = date.today()
        numero = "".join(str(secrets.randbelow(10)) for _ in range(16))
        validade = f"{hoje.month:02d}/{(hoje.year + 5) % 100:02d}"
        cvv = f"{secrets.randbelow(1000):03d}"
        data_pagamento = 10
        conexao.execute(
            "INSERT INTO cartoes (cpf, numero, validade, cvv, data_pagamento) VALUES (?, ?, ?, ?, ?)",
            (cpf, numero, validade, cvv, data_pagamento),
        )
        conexao.commit()
    else:
        numero, validade, cvv, data_pagamento = linha

    dados = carregar_conta(cpf)
    nome = carregar_cliente(cpf).nome or cpf
    cartao = CartaoCredito(nome, numero, validade, cvv, dados["limite_credito"], data_pagamento)
    cartao.saldo = dados["saldo_fatura"]
    cartao.parcelas = [
        valor
        for (valor,) in conexao.execute(
            "SELECT valor FROM parcelas_cartao WHERE cpf = ? ORDER BY id ASC", (cpf,)
        ).fetchall()
    ]
    return cartao


def salvar_cartao(cpf, cartao):
    conexao = obter_conexao()
    conexao.execute(
        "UPDATE usuarios SET limite_credito = ?, limite_disponivel = ?, saldo_fatura = ? WHERE cpf = ?",
        (cartao.limite, cartao.consultar_limite(), cartao.saldo, cpf),
    )
    conexao.execute("DELETE FROM parcelas_cartao WHERE cpf = ?", (cpf,))
    conexao.executemany(
        "INSERT INTO parcelas_cartao (cpf, valor) VALUES (?, ?)",
        [(cpf, valor) for valor in cartao.parcelas],
    )
    conexao.commit()


def listar_contas_completas():
    conexao = obter_conexao()
    linhas = conexao.execute("SELECT cpf, nome, saldo, limite_conta FROM usuarios").fetchall()
    return [
        {"cpf": cpf, "nome": nome, "saldo": saldo, "limite_conta": limite_conta}
        for cpf, nome, saldo, limite_conta in linhas
    ]


def restaurar_contas(contas):
    """Atualiza contas já cadastradas; CPFs ausentes do banco não são criados (faltam salt e senha)."""
    conexao = obter_conexao()
    restauradas = 0

    for conta in contas:
        cursor = conexao.execute(
            "UPDATE usuarios SET nome = ?, saldo = ?, limite_conta = ? WHERE cpf = ?",
            (conta["nome"], conta["saldo"], conta["limite_conta"], conta["cpf"]),
        )
        restauradas += cursor.rowcount

    conexao.commit()
    return restauradas


def limpar_parcelas_cartao(cpf):
    conexao = obter_conexao()
    conexao.execute("DELETE FROM parcelas_cartao WHERE cpf = ?", (cpf,))
    conexao.commit()
