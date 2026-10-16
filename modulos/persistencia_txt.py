import csv
import os

CAMINHO_CONTAS_TXT = "contas.txt"
CAMPOS = ("cpf", "nome", "saldo", "limite_conta")


def salvar_contas_txt(contas, caminho=CAMINHO_CONTAS_TXT):
    """Grava uma linha por conta, no formato cpf;nome;saldo;limite_conta."""
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        for conta in contas:
            escritor.writerow(
                [conta["cpf"], conta.get("nome", ""), conta["saldo"], conta.get("limite_conta", 0.0)]
            )


def carregar_contas_txt(caminho=CAMINHO_CONTAS_TXT):
    """Lê o arquivo e devolve a lista de contas; sem arquivo, devolve lista vazia."""
    if not os.path.exists(caminho):
        return []

    contas = []
    with open(caminho, newline="", encoding="utf-8") as arquivo:
        for linha in csv.reader(arquivo, delimiter=";"):
            if len(linha) != len(CAMPOS):
                continue  # ignora linhas corrompidas ou em branco

            cpf, nome, saldo, limite_conta = linha
            try:
                contas.append(
                    {"cpf": cpf, "nome": nome, "saldo": float(saldo), "limite_conta": float(limite_conta)}
                )
            except ValueError:
                continue

    return contas
