import csv
from datetime import datetime

arquivos_de_dados = 'financas_igreja.csv'
campos = ['data', 'descricao', 'valor', 'tipo', 'categoria']

def carregar_dados():
    try:
        with open(arquivos_de_dados, mode='r', newline='', encoding='utf-8') as arquivo:
            leitor_csv = csv.DictReader(arquivo)
            lista_de_transacoes = list(leitor_csv)
        
        for transacao in lista_de_transacoes:
            transacao['valor'] = float(transacao['valor'])

        return lista_de_transacoes

    except FileNotFoundError:
        return []
    except Exception as e:
        print(f'Erro ao carregar o arquivo: {e}')
        return []

def salvar_dados(lista_de_transacoes):
    try:
        with open(arquivos_de_dados, mode='w', newline='', encoding='utf-8') as arquivo:
            escritor_csv = csv.DictWriter(arquivo, fieldnames=campos)
            escritor_csv.writeheader()
            escritor_csv.writerows(lista_de_transacoes)
    except Exception as e:
        print(f'Erro ao salvar dados: {e}')

def listar_transacoes(lista_de_transacoes):
    print("\n--- Lista de Transações ---")
    if not lista_de_transacoes:
        print("Nenhuma transação para listar.")
        return False

    for i, transacao in enumerate(lista_de_transacoes, start=1):
        print(f"[{i}] - {transacao['data']} - {transacao['descricao']:<25} | R$ {transacao['valor']:.2f}")
    
    return True

def adicionar_transacao(lista_de_transacoes):
    print('\n---Adicionar uma nova Transação---')
    print("(Digite 'cancelar' a qualquer momento para voltar ao menu)")
    
    while True:
        try:
            valor_str = input('Valor (R$): ').replace(',', '.')
            if valor_str.lower().strip() == 'cancelar':
                print('Operação cancelada.')
                return
            valor = float(valor_str)
            break
        except ValueError:
            print('❌ Erro: Por favor, digite um número válido.')

    while True:
        tipo_usuario = input("Digite o tipo ('entrada' ou 'saida'): ").lower().strip()
        if tipo_usuario == 'cancelar':
            print('Operação cancelada.')
            return
        if tipo_usuario in ['entrada', 'e', 'r', 'receita']:
            tipo_final = 'entrada'
            break
        elif tipo_usuario in ['saida', 's', 'd', 'despesa']:
            tipo_final = 'saida'
            break
        else:
            print('❌ Erro: Tipo inválido. Tente novamente.')

    data = datetime.now().strftime('%d/%m/%Y')
    descricao = input("Descrição da Transação: ")
    if descricao.lower().strip() == 'cancelar':
        print('Operação cancelada.')
        return
        
    categoria = input("Categoria: ")
    if categoria.lower().strip() == 'cancelar':
        print('Operação cancelada.')
        return
    
    nova_transacao = {
        'data': data,
        'descricao': descricao,
        'valor': valor,
        'tipo': tipo_final,
        'categoria': categoria,
    }

    lista_de_transacoes.append(nova_transacao)
    salvar_dados(lista_de_transacoes)
    print('\n✅ Transação adicionada e salva com sucesso !!')

def mostrar_relatorio_detalhado(lista_de_transacoes):
    print("\n--- Relatório Detalhado por Mês ---")

    while True:
        try:
            mes_data_str = input('Digite o mês que deseja ver (ou "cancelar"): ')
            if mes_data_str.lower().strip() == 'cancelar':
                print('Operação cancelada.')
                return 
            
            mes_data = int(mes_data_str)
            if 1 <= mes_data <= 12:
                mes_ajeitado = f'{mes_data:02d}'
                break
            else:
                print('❌ Erro: Esse número tem que ser entre 1 e 12.')
        except ValueError:
            print('❌ Erro: Por favor, digite apenas o número do mês.')

    while True:
        try:
            ano_data_str = input('Digite o ano (ou "cancelar"): ')
            if ano_data_str.lower().strip() == 'cancelar':
                print('Operação cancelada.')
                return
            ano_data = int(ano_data_str)
            if 2000 <= ano_data <= 2100:
                ano_ajeitado = str(ano_data)
                break
            else:
                print('❌ Erro: Digite um ano entre 2000 e 2100.')
        except ValueError:
            print('❌ Erro: Por favor, digite apenas números para o Ano.')

    transacoes_do_periodo = []
    for transacao in lista_de_transacoes:
        if transacao['data'][3:5] == mes_ajeitado and transacao['data'][6:10] == ano_ajeitado:
            transacoes_do_periodo.append(transacao)

    if not transacoes_do_periodo:
        print(f'\nNenhuma transação foi encontrada para o período de {mes_ajeitado}/{ano_ajeitado}.')
        return

    print(f'\n--- Lista de Transações de {mes_ajeitado}/{ano_ajeitado} ---')
    listar_transacoes(transacoes_do_periodo)

    total_entradas_periodo = 0.0
    total_saidas_periodo = 0.0

    for transacao in transacoes_do_periodo:
        if transacao['tipo'] == 'entrada':
            total_entradas_periodo += transacao['valor']
        elif transacao['tipo'] == 'saida':
            total_saidas_periodo += transacao['valor']

    saldo_periodo = total_entradas_periodo - total_saidas_periodo

    print("\n--- Resumo do Mês ---")
    print(f"Total de Entradas: R$ {total_entradas_periodo:.2f}")
    print(f"Total de Saídas:   R$ {total_saidas_periodo:.2f}")
    print("-----------------------")
    print(f"Saldo do Período:  R$ {saldo_periodo:.2f}")

def excluir_dados(lista_de_transacoes):
    print('\n---Excluir uma Transação---')

    while True:
        try:
            mes_data_str = input('Digite o mês que deseja filtrar (ou "cancelar"): ')
            if mes_data_str.lower().strip() == 'cancelar':
                print('Operação cancelada.')
                return
            mes_data = int(mes_data_str)
            if 1 <= mes_data <= 12:
                mes_ajeitado = f'{mes_data:02d}'
                break
            else:
                print('❌ Erro: Esse número tem que ser entre 1 e 12.')
        except ValueError:
            print('❌ Erro: Por favor, digite apenas o número do mês.')

    while True:
        try:
            ano_data_str = input('Digite o ano (ou "cancelar"): ')
            if ano_data_str.lower().strip() == 'cancelar':
                print('Operação cancelada.')
                return
            ano_data = int(ano_data_str)
            if 2000 <= ano_data <= 2100:
                ano_ajeitado = str(ano_data)
                break
            else:
                print('❌ Erro: Digite um ano entre 2000 e 2100.')
        except ValueError:
            print('❌ Erro: Por favor, digite apenas números para o Ano.')

    transacoes_do_periodo = []
    for transacao in lista_de_transacoes:
        if transacao['data'][3:5] == mes_ajeitado and transacao['data'][6:10] == ano_ajeitado:
            transacoes_do_periodo.append(transacao)

    if not transacoes_do_periodo:
        print(f'\nNenhuma transação foi encontrada para o período de {mes_ajeitado}/{ano_ajeitado}.')
        return

    print("\nTransações encontradas para este período:")
    listar_transacoes(transacoes_do_periodo)

    while True:
        try:
            num_para_excluir_str = input('\nDigite o número da transação que deseja excluir (ou "cancelar"): ')
            if num_para_excluir_str.lower().strip() == 'cancelar':
                print("Operação cancelada.")
                return
            num_para_excluir = int(num_para_excluir_str)
            if 1 <= num_para_excluir <= len(transacoes_do_periodo):
                break
            else:
                print('❌ ERRO: Número inválido. Ele não está na lista.')
        except ValueError:
            print('❌ ERRO: Por favor, digite apenas um número.')
    
    indice_para_excluir = num_para_excluir - 1
    transacao_para_remover = transacoes_do_periodo[indice_para_excluir]
    lista_de_transacoes.remove(transacao_para_remover)
    salvar_dados(lista_de_transacoes)
    print(f"\n✅ A transação '{transacao_para_remover['descricao']}' foi removida com sucesso.")

def editar_transacao(lista_de_transacoes):
    print('\n---Editar Transação---')

    while True:
        try:
            mes_data_str = input('Digite o mês que deseja filtrar (ou "cancelar"): ')
            if mes_data_str.lower().strip() == 'cancelar':
                print('Operação cancelada.')
                return
            mes_data = int(mes_data_str)
            if 1 <= mes_data <= 12:
                mes_ajeitado = f'{mes_data:02d}'
                break
            else:
                print('❌ Erro: Esse número tem que ser entre 1 e 12.')
        except ValueError:
            print('❌ Erro: Por favor, digite apenas o número do mês.')

    while True:
        try:
            ano_data_str = input('Digite o ano (ou "cancelar"): ')
            if ano_data_str.lower().strip() == 'cancelar':
                print("Operação cancelada.")
                return
            ano_data = int(ano_data_str)
            if 2000 <= ano_data <= 2100:
                ano_ajeitado = str(ano_data)
                break
            else:
                print('❌ Erro: Digite um ano entre 2000 e 2100.')
        except ValueError:
            print('❌ Erro: Por favor, digite apenas números para o Ano.')

    transacoes_do_periodo = []
    for transacao in lista_de_transacoes:
        if transacao['data'][3:5] == mes_ajeitado and transacao['data'][6:10] == ano_ajeitado:
            transacoes_do_periodo.append(transacao)

    if not transacoes_do_periodo:
        print(f'\nNenhuma transação foi encontrada para o período de {mes_ajeitado}/{ano_ajeitado}.')
        return

    print("\nTransações encontradas para este período:")
    listar_transacoes(transacoes_do_periodo)

    while True:
        try:
            num_para_editar_str = input('\nDigite o número da transação que deseja editar (ou "cancelar"): ')
            if num_para_editar_str.lower().strip() == 'cancelar':
                print("Operação cancelada.")
                return
            num_para_editar = int(num_para_editar_str)
            if 1 <= num_para_editar <= len(transacoes_do_periodo):
                break
            else:
                print('❌ ERRO: Número inválido. Ele não está na lista.')
        except ValueError:
            print('❌ ERRO: Por favor, digite apenas um número.')
    
    indice_para_editar = num_para_editar - 1
    transacao_para_editar = transacoes_do_periodo[indice_para_editar]
    
    print('\nVocê selecionou a seguinte transação para editar:')
    print(transacao_para_editar)
    
    print('\nO que você deseja editar?')
    print("[1] Descrição")
    print("[2] Valor")
    print("[3] Tipo (entrada/saida)")
    print("[4] Categoria")
    print("[5] Cancelar Edição")

    escolha_campo = input('Escolha o campo: ')

    campo_foi_alterado = False

    if escolha_campo == '1':
        nova_descricao = input("Digite a nova descrição: ")
        if nova_descricao.lower().strip() != 'cancelar':
            transacao_para_editar['descricao'] = nova_descricao
            campo_foi_alterado = True
    elif escolha_campo == '2':
        while True:
            try:
                novo_valor_str = input('Digite o novo valor (R$): ').replace(',', '.')
                if novo_valor_str.lower().strip() == 'cancelar':
                    break
                novo_valor = float(novo_valor_str)
                transacao_para_editar['valor'] = novo_valor
                campo_foi_alterado = True
                break
            except ValueError:
                print("❌ Erro: Valor inválido.")
    elif escolha_campo == '3':
        while True:
            novo_tipo = input("Digite o novo tipo ('entrada' ou 'saida'): ").lower().strip()
            if novo_tipo == 'cancelar':
                break
            if novo_tipo in ['entrada', 'saida']:
                transacao_para_editar['tipo'] = novo_tipo
                campo_foi_alterado = True
                break
            else:
                print("❌ Erro: Tipo inválido.")
    elif escolha_campo == '4':
        nova_categoria = input('Digite uma nova categoria: ')
        if nova_categoria.lower().strip() != 'cancelar':
            transacao_para_editar['categoria'] = nova_categoria
            campo_foi_alterado = True
    elif escolha_campo == '5':
        print("\nEdição cancelada.")
    else:
        print("\nOpção inválida.")

    if campo_foi_alterado:
        salvar_dados(lista_de_transacoes)
        print("\n✅ Transação editada e salva com sucesso!")

def main():
    transacoes = carregar_dados()

    while True:
        print('\n====Sistema de Finanças da Igreja====')
        print('''OPÇÕES:
[1] Adicionar Transação
[2] Ver Relatório e Saldo do Mês
[3] Excluir Transação
[4] Editar Transação
[5] Sair do Programa''')
        print('-=-=-=-=-=-' * 5)

        escolha_do_usuario = input('Escolha uma opção: ')

        if escolha_do_usuario == '1':
            adicionar_transacao(transacoes)
        elif escolha_do_usuario == '2':
            mostrar_relatorio_detalhado(transacoes)
        elif escolha_do_usuario == '3':
            excluir_dados(transacoes)
        elif escolha_do_usuario == '4':
            editar_transacao(transacoes)
        elif escolha_do_usuario == '5':
            print('Fim do Programa!!')
            break
        else:
            print('\nOpção inválida. Tente novamente.')

if __name__ == "__main__":
    main()