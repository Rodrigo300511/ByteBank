import hashlib
import hmac
import secrets

from modulos.banco_dados import obter_conexao

ITERACOES_HASH = 100_000


def validar_cpf(cpf):
    cpf = "".join(caractere for caractere in cpf if caractere.isdigit())

    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    for posicao in (9, 10):
        soma = sum(int(cpf[indice]) * (posicao + 1 - indice) for indice in range(posicao))
        resto = (soma * 10) % 11
        digito_esperado = 0 if resto == 10 else resto
        if digito_esperado != int(cpf[posicao]):
            return False

    return True


def gerar_hash_senha(senha, salt=None):
    salt = salt or secrets.token_bytes(16)
    hash_senha = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), salt, ITERACOES_HASH)
    return salt.hex(), hash_senha.hex()


def cadastrar_usuario(cpf, senha):
    cpf_numerico = "".join(caractere for caractere in cpf if caractere.isdigit())

    if not validar_cpf(cpf_numerico):
        return "CPF inválido."
    if len(senha) < 6:
        return "A senha deve ter pelo menos 6 caracteres."

    conexao = obter_conexao()
    usuario_existente = conexao.execute(
        "SELECT cpf FROM usuarios WHERE cpf = ?", (cpf_numerico,)
    ).fetchone()

    if usuario_existente:
        return "Já existe uma conta cadastrada com esse CPF."

    salt, hash_senha = gerar_hash_senha(senha)
    conexao.execute(
        "INSERT INTO usuarios (cpf, salt, senha_hash) VALUES (?, ?, ?)",
        (cpf_numerico, salt, hash_senha),
    )
    conexao.commit()
    return "Conta criada com sucesso! Faça login para continuar."


def autenticar_usuario(cpf, senha):
    cpf_numerico = "".join(caractere for caractere in cpf if caractere.isdigit())

    conexao = obter_conexao()
    linha = conexao.execute(
        "SELECT salt, senha_hash FROM usuarios WHERE cpf = ?", (cpf_numerico,)
    ).fetchone()

    if linha is None:
        return False, "CPF ou senha inválidos."

    salt_armazenado, hash_armazenado = linha
    _, hash_calculado = gerar_hash_senha(senha, bytes.fromhex(salt_armazenado))

    if not hmac.compare_digest(hash_calculado, hash_armazenado):
        return False, "CPF ou senha inválidos."

    return True, cpf_numerico
