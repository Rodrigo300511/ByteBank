import sqlite3

CAMINHO_BANCO = "bytebank.db"

_conexao = None


def obter_conexao():
    global _conexao

    if _conexao is None:
        _conexao = sqlite3.connect(CAMINHO_BANCO)
        _conexao.execute("PRAGMA foreign_keys = ON")

    return _conexao


def inicializar_banco():
    conexao = obter_conexao()
    conexao.executescript(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            cpf TEXT PRIMARY KEY,
            salt TEXT NOT NULL,
            senha_hash TEXT NOT NULL,
            saldo REAL NOT NULL DEFAULT 0,
            limite_credito REAL NOT NULL DEFAULT 1000,
            limite_disponivel REAL NOT NULL DEFAULT 1000,
            saldo_fatura REAL NOT NULL DEFAULT 0,
            pontos_bytepoints INTEGER NOT NULL DEFAULT 0,
            divida_emprestimo REAL NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS caixinhas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpf TEXT NOT NULL REFERENCES usuarios(cpf),
            nome TEXT NOT NULL,
            valor REAL NOT NULL DEFAULT 0,
            UNIQUE(cpf, nome)
        );

        CREATE TABLE IF NOT EXISTS historico_gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpf TEXT NOT NULL REFERENCES usuarios(cpf),
            categoria TEXT NOT NULL,
            valor REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS historico_credito (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpf TEXT NOT NULL REFERENCES usuarios(cpf),
            estabelecimento TEXT NOT NULL,
            valor REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS saldos_moedas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpf TEXT NOT NULL REFERENCES usuarios(cpf),
            moeda TEXT NOT NULL,
            quantidade REAL NOT NULL DEFAULT 0,
            UNIQUE(cpf, moeda)
        );

        CREATE TABLE IF NOT EXISTS parcelas_emprestimo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpf TEXT NOT NULL REFERENCES usuarios(cpf),
            valor REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS extrato (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpf TEXT NOT NULL REFERENCES usuarios(cpf),
            tipo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS pagamentos_agendados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cpf TEXT NOT NULL REFERENCES usuarios(cpf),
            descricao TEXT NOT NULL,
            valor REAL NOT NULL
        );
        """
    )
    conexao.commit()
