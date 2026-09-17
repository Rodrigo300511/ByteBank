CATEGORIAS = ["Alimentação", "Transporte", "Lazer", "Contas", "Outros"]


def relatorio_categoria(historico):
    if not historico:
        return "Nenhum gasto registrado ainda."

    gastos_por_categoria = {}
    for gasto in historico:
        categoria = gasto["categoria"]
        valor = gasto["valor"]
        gastos_por_categoria[categoria] = gastos_por_categoria.get(categoria, 0) + valor

    total_gasto = sum(gastos_por_categoria.values())

    linhas = ["\n--- Relatório de Gastos por Categoria ---"]
    for categoria, valor in gastos_por_categoria.items():
        percentual = (valor / total_gasto) * 100
        linhas.append(f"{categoria}: R$ {valor:.2f} ({percentual:.1f}% do total gasto)")
    linhas.append(f"Total gasto: R$ {total_gasto:.2f}")

    return "\n".join(linhas)
