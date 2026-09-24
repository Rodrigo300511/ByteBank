def mostrar_extrato(movimentacoes):
    if not movimentacoes:
        return "Nenhuma movimentação registrada ainda."

    linhas = ["\n--- Extrato ---"]
    for movimentacao in movimentacoes:
        sinal = "+" if movimentacao["valor"] >= 0 else "-"
        linhas.append(
            f"[{movimentacao['tipo']}] {movimentacao['descricao']}: {sinal}R$ {abs(movimentacao['valor']):.2f}"
        )

    return "\n".join(linhas)
