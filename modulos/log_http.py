import re
import sys

# Formato Common/Combined Log Format: ... "GET /pagina HTTP/1.1" 200 1234
PADRAO_REQUISICAO = re.compile(r'"[^"]*"\s+(\d{3})\b')


def analisar_log(caminho):
    """Conta as requisições com status 200 e 404 em um arquivo de log de servidor."""
    contagem = {200: 0, 404: 0}

    with open(caminho, encoding="utf-8", errors="replace") as arquivo:
        for linha in arquivo:
            correspondencia = PADRAO_REQUISICAO.search(linha)
            if correspondencia:
                codigo = int(correspondencia.group(1))
                if codigo in contagem:
                    contagem[codigo] += 1

    return contagem


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Uso: python -m modulos.log_http <arquivo_de_log>")

    resultado = analisar_log(sys.argv[1])
    print(f"200 (Sucesso): {resultado[200]}")
    print(f"404 (Não Encontrado): {resultado[404]}")
