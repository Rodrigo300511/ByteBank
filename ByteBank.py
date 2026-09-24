import sys

from modulos import (
    agendamentos,
    banco_dados,
    cambio,
    cartao_credito,
    categorias,
    cofrinhos,
    conta,
    emprestimos,
    estorno,
    extrato,
    fidelidade,
    pix,
    repositorio,
    usuarios,
)

banco_dados.inicializar_banco()

cpf = None

while cpf is None:
    print("\n===== BYTEBANK =====")
    print("1 - Entrar")
    print("2 - Criar conta")
    print("3 - Sair")

    opcao_acesso = int(input("Escolha uma opção: "))

    if opcao_acesso == 1:
        cpf_digitado = input("CPF: ")
        senha_digitada = input("Senha: ")
        sucesso, resultado = usuarios.autenticar_usuario(cpf_digitado, senha_digitada)

        if sucesso:
            cpf = resultado
        else:
            print(resultado)

    elif opcao_acesso == 2:
        cpf_digitado = input("CPF: ")
        senha_digitada = input("Crie uma senha (mínimo 6 caracteres): ")
        print(usuarios.cadastrar_usuario(cpf_digitado, senha_digitada))

    elif opcao_acesso == 3:
        sys.exit()

    else:
        print("Opção inválida.")

print(f"\nBem-vindo(a), {cpf}!")

# Pilha (TAD) de operações reversíveis desta sessão, usada pela opção "Desfazer".
pilha_desfazer = []

while True:

    print("\n===== BANCO =====")
    print("1 - Depósito")
    print("2 - Saque")
    print("3 - Saldo")
    print("4 - Criar Caixinha")
    print("5 - Guardar na Caixinha")
    print("6 - Resgatar da Caixinha")
    print("7 - Ver Caixinhas")
    print("8 - Simular Rendimento das Caixinhas")
    print("9 - Relatório de Gastos por Categoria")
    print("10 - Comprar no Crédito")
    print("11 - Pagar Fatura")
    print("12 - Ver Fatura")
    print("13 - Comprar Moeda Estrangeira")
    print("14 - Vender Moeda Estrangeira")
    print("15 - Ver Carteira de Moedas")
    print("16 - Consultar BytePoints")
    print("17 - Resgatar Cashback")
    print("18 - Simular Empréstimo")
    print("19 - Contratar Empréstimo")
    print("20 - Pagar Parcela do Empréstimo")
    print("21 - Ver Empréstimo")
    print("22 - Transferir PIX")
    print("23 - Ver Contas")
    print("24 - Extrato")
    print("25 - Desfazer Última Operação")
    print("26 - Agendar Pagamento")
    print("27 - Ver Pagamentos Agendados")
    print("28 - Processar Próximo Pagamento Agendado")
    print("29 - Sair")

    opcao = int(input("Escolha uma opção: "))

    if opcao == 1:
        valor_deposito = float(input("Digite o valor do depósito: "))

        if valor_deposito > 0:
            dados_conta = repositorio.carregar_conta(cpf)
            saldo = conta.deposito(dados_conta["saldo"], valor_deposito)
            repositorio.salvar_conta(cpf, saldo=saldo)
            pilha_desfazer.append({"tipo": "deposito", "valor": valor_deposito})
            repositorio.registrar_extrato(cpf, "deposito", "Depósito em conta", valor_deposito)
            print(f"Depósito realizado! Saldo: R$ {saldo:.2f}")
        else:
            print("Valor de depósito inválido.")

    elif opcao == 2:
        valor_saque = float(input("Digite o valor do saque: "))
        dados_conta = repositorio.carregar_conta(cpf)

        if valor_saque <= 0:
            print("Valor de saque inválido.")

        elif valor_saque > dados_conta["saldo"]:
            print("Saldo insuficiente.")

        else:
            print("\nCategorias disponíveis:")
            for i, categoria in enumerate(categorias.CATEGORIAS, start=1):
                print(f"{i} - {categoria}")

            indice_categoria = int(input("Escolha a categoria do gasto: "))

            if 1 <= indice_categoria <= len(categorias.CATEGORIAS):
                categoria_escolhida = categorias.CATEGORIAS[indice_categoria - 1]
                saldo = conta.saque(dados_conta["saldo"], valor_saque)
                pontos_ganhos = fidelidade.calcular_pontos(valor_saque)
                pontos_bytepoints = dados_conta["pontos_bytepoints"] + pontos_ganhos

                repositorio.registrar_gasto(cpf, categoria_escolhida, valor_saque)
                repositorio.salvar_conta(cpf, saldo=saldo, pontos_bytepoints=pontos_bytepoints)
                pilha_desfazer.append({"tipo": "saque", "valor": valor_saque})
                repositorio.registrar_extrato(cpf, "saque", f"Saque - {categoria_escolhida}", -valor_saque)
                print(f"Saque realizado! Saldo: R$ {saldo:.2f} | +{pontos_ganhos} BytePoints")
            else:
                print("Categoria inválida. Saque cancelado.")

    elif opcao == 3:
        dados_conta = repositorio.carregar_conta(cpf)
        print(f"Seu saldo é de: R$ {conta.mostrar_saldo(dados_conta['saldo']):.2f}")

    elif opcao == 4:
        nome_caixinha = input("Digite o nome da caixinha: ")
        caixinhas = repositorio.carregar_caixinhas(cpf)
        mensagem = cofrinhos.criar_cofrinho(caixinhas, nome_caixinha)
        repositorio.salvar_caixinhas(cpf, caixinhas)
        print(mensagem)

    elif opcao == 5:
        nome_caixinha = input("Digite o nome da caixinha: ")
        valor_guardar = float(input("Digite o valor a guardar: "))
        dados_conta = repositorio.carregar_conta(cpf)
        caixinhas = repositorio.carregar_caixinhas(cpf)
        saldo, mensagem = cofrinhos.guardar_no_cofrinho(
            dados_conta["saldo"], caixinhas, nome_caixinha, valor_guardar
        )
        repositorio.salvar_conta(cpf, saldo=saldo)
        repositorio.salvar_caixinhas(cpf, caixinhas)
        if saldo != dados_conta["saldo"]:
            repositorio.registrar_extrato(
                cpf, "cofrinho_guardar", f"Guardado na caixinha '{nome_caixinha}'", saldo - dados_conta["saldo"]
            )
        print(mensagem)

    elif opcao == 6:
        nome_caixinha = input("Digite o nome da caixinha: ")
        valor_resgatar = float(input("Digite o valor a resgatar: "))
        dados_conta = repositorio.carregar_conta(cpf)
        caixinhas = repositorio.carregar_caixinhas(cpf)
        saldo, mensagem = cofrinhos.resgatar_do_cofrinho(
            dados_conta["saldo"], caixinhas, nome_caixinha, valor_resgatar
        )
        repositorio.salvar_conta(cpf, saldo=saldo)
        repositorio.salvar_caixinhas(cpf, caixinhas)
        if saldo != dados_conta["saldo"]:
            repositorio.registrar_extrato(
                cpf, "cofrinho_resgatar", f"Resgatado da caixinha '{nome_caixinha}'", saldo - dados_conta["saldo"]
            )
        print(mensagem)

    elif opcao == 7:
        caixinhas = repositorio.carregar_caixinhas(cpf)
        print(cofrinhos.mostrar_cofrinhos(caixinhas))

    elif opcao == 8:
        caixinhas = repositorio.carregar_caixinhas(cpf)
        mensagem = cofrinhos.simular_rendimento(caixinhas)
        repositorio.salvar_caixinhas(cpf, caixinhas)
        print(mensagem)

    elif opcao == 9:
        historico_gastos = repositorio.carregar_historico_gastos(cpf)
        print(categorias.relatorio_categoria(historico_gastos))

    elif opcao == 10:
        valor_compra = float(input("Digite o valor da compra: "))
        estabelecimento = input("Digite o nome do estabelecimento: ")
        dados_conta = repositorio.carregar_conta(cpf)
        saldo_fatura_antes = dados_conta["saldo_fatura"]

        limite_disponivel, saldo_fatura, mensagem = cartao_credito.comprar_no_credito(
            dados_conta["limite_disponivel"], dados_conta["saldo_fatura"], valor_compra, estabelecimento
        )
        repositorio.salvar_conta(cpf, limite_disponivel=limite_disponivel, saldo_fatura=saldo_fatura)

        if saldo_fatura > saldo_fatura_antes:
            repositorio.registrar_compra_credito(cpf, estabelecimento, valor_compra)

        print(mensagem)

    elif opcao == 11:
        dados_conta = repositorio.carregar_conta(cpf)
        saldo, limite_disponivel, saldo_fatura, mensagem = cartao_credito.pagar_fatura(
            dados_conta["saldo"], dados_conta["limite_disponivel"], dados_conta["saldo_fatura"]
        )
        repositorio.salvar_conta(cpf, saldo=saldo, limite_disponivel=limite_disponivel, saldo_fatura=saldo_fatura)
        if saldo != dados_conta["saldo"]:
            repositorio.registrar_extrato(
                cpf, "fatura", "Pagamento de fatura do cartão", saldo - dados_conta["saldo"]
            )
        print(mensagem)

    elif opcao == 12:
        dados_conta = repositorio.carregar_conta(cpf)
        print(
            cartao_credito.mostrar_fatura(
                dados_conta["limite_credito"], dados_conta["limite_disponivel"], dados_conta["saldo_fatura"]
            )
        )

    elif opcao == 13:
        moeda = input("Digite a moeda (USD, EUR, BTC): ").upper()
        valor_brl = float(input("Digite o valor em R$ a converter: "))
        dados_conta = repositorio.carregar_conta(cpf)
        saldos_moedas = repositorio.carregar_saldos_moedas(cpf)
        saldo, mensagem = cambio.comprar_moeda_estrangeira(dados_conta["saldo"], saldos_moedas, moeda, valor_brl)
        repositorio.salvar_conta(cpf, saldo=saldo)
        repositorio.salvar_saldos_moedas(cpf, saldos_moedas)
        if saldo != dados_conta["saldo"]:
            repositorio.registrar_extrato(cpf, "cambio", f"Compra de {moeda}", saldo - dados_conta["saldo"])
        print(mensagem)

    elif opcao == 14:
        moeda = input("Digite a moeda (USD, EUR, BTC): ").upper()
        quantidade = float(input("Digite a quantidade a vender: "))
        dados_conta = repositorio.carregar_conta(cpf)
        saldos_moedas = repositorio.carregar_saldos_moedas(cpf)
        saldo, mensagem = cambio.vender_moeda_estrangeira(dados_conta["saldo"], saldos_moedas, moeda, quantidade)
        repositorio.salvar_conta(cpf, saldo=saldo)
        repositorio.salvar_saldos_moedas(cpf, saldos_moedas)
        if saldo != dados_conta["saldo"]:
            repositorio.registrar_extrato(cpf, "cambio", f"Venda de {moeda}", saldo - dados_conta["saldo"])
        print(mensagem)

    elif opcao == 15:
        saldos_moedas = repositorio.carregar_saldos_moedas(cpf)
        print(cambio.mostrar_carteira(saldos_moedas))

    elif opcao == 16:
        dados_conta = repositorio.carregar_conta(cpf)
        print(fidelidade.consultar_pontos(dados_conta["pontos_bytepoints"]))

    elif opcao == 17:
        pontos_resgatar = int(input("Digite a quantidade de pontos a resgatar: "))
        dados_conta = repositorio.carregar_conta(cpf)
        saldo, pontos_bytepoints, mensagem = fidelidade.resgatar_cashback(
            dados_conta["saldo"], dados_conta["pontos_bytepoints"], pontos_resgatar
        )
        repositorio.salvar_conta(cpf, saldo=saldo, pontos_bytepoints=pontos_bytepoints)
        if saldo != dados_conta["saldo"]:
            repositorio.registrar_extrato(cpf, "cashback", "Resgate de cashback", saldo - dados_conta["saldo"])
        print(mensagem)

    elif opcao == 18:
        valor_emprestimo = float(input("Digite o valor do empréstimo: "))
        numero_parcelas = int(input("Digite o número de parcelas: "))
        dados_conta = repositorio.carregar_conta(cpf)
        print(emprestimos.simular_emprestimo(dados_conta["saldo"], valor_emprestimo, numero_parcelas))

    elif opcao == 19:
        valor_emprestimo = float(input("Digite o valor do empréstimo: "))
        numero_parcelas = int(input("Digite o número de parcelas: "))
        dados_conta = repositorio.carregar_conta(cpf)
        parcelas_emprestimo = repositorio.carregar_parcelas(cpf)
        tamanho_antes = len(parcelas_emprestimo)

        saldo, divida_emprestimo, mensagem = emprestimos.contratar_emprestimo(
            dados_conta["saldo"],
            dados_conta["divida_emprestimo"],
            parcelas_emprestimo,
            valor_emprestimo,
            numero_parcelas,
        )
        repositorio.salvar_conta(cpf, saldo=saldo, divida_emprestimo=divida_emprestimo)

        novas_parcelas = parcelas_emprestimo[tamanho_antes:]
        if novas_parcelas:
            repositorio.adicionar_parcelas(cpf, novas_parcelas)
            repositorio.registrar_extrato(
                cpf, "emprestimo", f"Empréstimo contratado ({numero_parcelas}x)", saldo - dados_conta["saldo"]
            )

        print(mensagem)

    elif opcao == 20:
        dados_conta = repositorio.carregar_conta(cpf)
        parcelas_emprestimo = repositorio.carregar_parcelas(cpf)
        tamanho_antes = len(parcelas_emprestimo)

        saldo, divida_emprestimo, mensagem = emprestimos.pagar_parcela_emprestimo(
            dados_conta["saldo"], dados_conta["divida_emprestimo"], parcelas_emprestimo
        )
        repositorio.salvar_conta(cpf, saldo=saldo, divida_emprestimo=divida_emprestimo)

        if len(parcelas_emprestimo) < tamanho_antes:
            repositorio.remover_proxima_parcela(cpf)
            repositorio.registrar_extrato(
                cpf, "emprestimo", "Pagamento de parcela do empréstimo", saldo - dados_conta["saldo"]
            )

        print(mensagem)

    elif opcao == 21:
        dados_conta = repositorio.carregar_conta(cpf)
        parcelas_emprestimo = repositorio.carregar_parcelas(cpf)
        print(emprestimos.mostrar_emprestimo(dados_conta["divida_emprestimo"], parcelas_emprestimo))

    elif opcao == 22:
        cpf_destino_input = input("CPF de destino: ")
        valor_transferencia = float(input("Valor a transferir: "))
        cpf_destino = "".join(caractere for caractere in cpf_destino_input if caractere.isdigit())

        contas = repositorio.listar_contas()
        contas, sucesso, mensagem = pix.transferir_pix(contas, cpf, cpf_destino, valor_transferencia)

        if sucesso:
            for conta_atualizada in contas:
                if conta_atualizada["cpf"] in (cpf, cpf_destino):
                    repositorio.salvar_conta(conta_atualizada["cpf"], saldo=conta_atualizada["saldo"])

            pilha_desfazer.append({"tipo": "pix", "valor": valor_transferencia, "cpf_destino": cpf_destino})
            repositorio.registrar_extrato(cpf, "pix_enviado", f"PIX enviado para {cpf_destino}", -valor_transferencia)
            repositorio.registrar_extrato(
                cpf_destino, "pix_recebido", f"PIX recebido de {cpf}", valor_transferencia
            )

        print(mensagem)

    elif opcao == 23:
        contas = repositorio.listar_contas()
        print(pix.mostrar_contas(contas, cpf))

    elif opcao == 24:
        movimentacoes = repositorio.carregar_extrato(cpf)
        print(extrato.mostrar_extrato(movimentacoes))

    elif opcao == 25:
        dados_conta = repositorio.carregar_conta(cpf)
        saldo, estorno_destino, mensagem = estorno.desfazer_ultima_operacao(dados_conta["saldo"], pilha_desfazer)
        repositorio.salvar_conta(cpf, saldo=saldo)

        if estorno_destino:
            cpf_destino_estorno, valor_estornado = estorno_destino
            dados_destino = repositorio.carregar_conta(cpf_destino_estorno)
            repositorio.salvar_conta(cpf_destino_estorno, saldo=conta.saque(dados_destino["saldo"], valor_estornado))

        if "desfeito" in mensagem or "estornado" in mensagem:
            repositorio.registrar_extrato(cpf, "estorno", mensagem, saldo - dados_conta["saldo"])

        print(mensagem)

    elif opcao == 26:
        descricao_pagamento = input("Descrição do pagamento: ")
        valor_pagamento = float(input("Valor do pagamento: "))
        fila_pagamentos = repositorio.carregar_pagamentos_agendados(cpf)
        tamanho_antes = len(fila_pagamentos)

        mensagem = agendamentos.agendar_pagamento(fila_pagamentos, descricao_pagamento, valor_pagamento)

        if len(fila_pagamentos) > tamanho_antes:
            repositorio.adicionar_pagamento_agendado(cpf, descricao_pagamento, valor_pagamento)

        print(mensagem)

    elif opcao == 27:
        fila_pagamentos = repositorio.carregar_pagamentos_agendados(cpf)
        print(agendamentos.mostrar_pagamentos_agendados(fila_pagamentos))

    elif opcao == 28:
        dados_conta = repositorio.carregar_conta(cpf)
        fila_pagamentos = repositorio.carregar_pagamentos_agendados(cpf)
        tamanho_antes = len(fila_pagamentos)
        proximo_pagamento = fila_pagamentos[0] if fila_pagamentos else None

        saldo, mensagem = agendamentos.processar_proximo_pagamento(dados_conta["saldo"], fila_pagamentos)

        if len(fila_pagamentos) < tamanho_antes:
            repositorio.remover_proximo_pagamento_agendado(cpf)
            repositorio.salvar_conta(cpf, saldo=saldo)
            repositorio.registrar_extrato(
                cpf, "pagamento_agendado", proximo_pagamento["descricao"], -proximo_pagamento["valor"]
            )

        print(mensagem)

    elif opcao == 29:
        print("Programa encerrado.")
        break

    else:
        print("Opção inválida.")
