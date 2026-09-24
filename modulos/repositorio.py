from modulos.banco_dados import obter_conexao
from modulos.cambio import TAXAS_CAMBIO


def carregar_conta(cpf):
    conexao = obter_conexao()
    linha = conexao.execute(
        "SELECT saldo, limite_credito, limite_disponivel, saldo_fatura, pontos_bytepoints, divida_emprestimo "
        "FROM usuarios WHERE cpf = ?",
        (cpf,),
    ).fetchone()

    saldo, limite_credito, limite_disponivel, saldo_fatura, pontos_bytepoints, divida_emprestimo = linha
    return {
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
    linhas = conexao.execute("SELECT cpf, saldo FROM usuarios").fetchall()
    return [{"cpf": cpf, "saldo": saldo} for cpf, saldo in linhas]
