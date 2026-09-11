def deposito(saldo, valor_deposito):
    return saldo + valor_deposito


def saque(saldo, valor_saque):
    return saldo - valor_saque


def mostrar_saldo(saldo):
    return saldo


saldo = 0

while True:

    print("\n===== BANCO =====")
    print("1 - Depósito")
    print("2 - Saque")
    print("3 - Saldo")
    print("4 - Sair")

    opcao = int(input("Escolha uma opção: "))

    if opcao == 1:
        valor_deposito = float(input("Digite o valor do depósito: "))

        if valor_deposito > 0:
            saldo = deposito(saldo, valor_deposito)
            print(f"Depósito realizado! Saldo: R$ {saldo:.2f}")
        else:
            print("Valor de depósito inválido.")

    elif opcao == 2:
        valor_saque = float(input("Digite o valor do saque: "))

        if valor_saque <= 0:
            print("Valor de saque inválido.")

        elif valor_saque > saldo:
            print("Saldo insuficiente.")

        else:
            saldo = saque(saldo, valor_saque)
            print(f"Saque realizado! Saldo: R$ {saldo:.2f}")

    elif opcao == 3:
        print(f"Seu saldo é de: R$ {mostrar_saldo(saldo):.2f}")

    elif opcao == 4:
        print("Programa encerrado.")
        break

    else:
        print("Opção inválida.")
