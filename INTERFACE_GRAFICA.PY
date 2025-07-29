import PySimpleGUI as sg
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
        sg.popup_error(f'Erro ao carregar o arquivo: {e}')
        return []

def salvar_dados(lista_de_transacoes):
    try:
        with open(arquivos_de_dados, mode='w', newline='', encoding='utf-8') as arquivo:
            escritor_csv = csv.DictWriter(arquivo, fieldnames=campos)
            escritor_csv.writeheader()
            escritor_csv.writerows(lista_de_transacoes)
    except Exception as e:
        sg.popup_error(f'Erro ao salvar dados: {e}')

def abrir_janela_adicionar():
    layout_adicionar = [
        [sg.Text("Descrição:", size=(10,1)), sg.InputText(key='-DESCRICAO-')],
        [sg.Text("Valor (R$):", size=(10,1)), sg.InputText(key='-VALOR-')],
        [sg.Text("Tipo:", size=(10,1)), sg.Combo(['entrada', 'saida'], default_value='saida', key='-TIPO-')],
        [sg.Text("Categoria:", size=(10,1)), sg.InputText(key='-CATEGORIA-')],
        [sg.Button("Salvar"), sg.Button("Cancelar")]
    ]
    janela_adicionar = sg.Window("Adicionar Nova Transação", layout_adicionar, modal=True)
    nova_transacao = None
    while True:
        event, values = janela_adicionar.read()
        if event == sg.WIN_CLOSED or event == "Cancelar":
            break
        if event == "Salvar":
            try:
                valor = float(values['-VALOR-'].replace(',', '.'))
                if not values['-DESCRICAO-'] or not values['-TIPO-'] or not values['-CATEGORIA-']:
                    sg.popup_error("Erro: Todos os campos devem ser preenchidos.")
                    continue
                nova_transacao = {
                    'data': datetime.now().strftime('%d/%m/%Y'),
                    'descricao': values['-DESCRICAO-'],
                    'valor': valor,
                    'tipo': values['-TIPO-'],
                    'categoria': values['-CATEGORIA-']
                }
                break
            except ValueError:
                sg.popup_error("Erro: O valor deve ser um número.")
    janela_adicionar.close()
    return nova_transacao

def abrir_janela_editar(transacao_para_editar):
    layout_editar = [
        [sg.Text("Descrição:", size=(10,1)), sg.InputText(default_text=transacao_para_editar['descricao'], key='-DESCRICAO-')],
        [sg.Text("Valor (R$):", size=(10,1)), sg.InputText(default_text=transacao_para_editar['valor'], key='-VALOR-')],
        [sg.Text("Tipo:", size=(10,1)), sg.Combo(['entrada', 'saida'], default_value=transacao_para_editar['tipo'], key='-TIPO-')],
        [sg.Text("Categoria:", size=(10,1)), sg.InputText(default_text=transacao_para_editar['categoria'], key='-CATEGORIA-')],
        [sg.Button("Salvar Alterações"), sg.Button("Cancelar")]
    ]
    janela_editar = sg.Window("Editar Transação", layout_editar, modal=True)
    dados_atualizados = None
    while True:
        event, values = janela_editar.read()
        if event == sg.WIN_CLOSED or event == 'Cancelar':
            break
        if event == 'Salvar Alterações':
            try:
                valor = float(values['-VALOR-'].replace(',', '.'))
                dados_atualizados = {
                    'data': transacao_para_editar['data'],
                    'descricao': values['-DESCRICAO-'],
                    'valor': valor,
                    'tipo': values['-TIPO-'],
                    'categoria': values['-CATEGORIA-']
                }
                break
            except ValueError:
                sg.popup_error("Erro: O valor deve ser um número.")
    janela_editar.close()
    return dados_atualizados

def main():
    sg.theme('DarkBlue3')

    layout_login = [
        [sg.VPush()],
        [sg.Column([
            [sg.Text("Sistema Financeiro da Igreja", font=("Helvetica", 22), justification='center')],
            [sg.Text("Por favor, faça o login para continuar", font=("Helvetica", 12), justification='center', pad=((0,0), (0, 20)))],
            [sg.HSeparator()],
            [sg.Text("Usuário:", size=(8, 1), font=("Helvetica", 11)), sg.InputText(key='-USUARIO-')],
            [sg.Text("Senha:", size=(8, 1), font=("Helvetica", 11)), sg.InputText(key='-SENHA-', password_char='*')],
            [sg.Button("Login", font=("Helvetica", 11)), sg.Button("Sair", font=("Helvetica", 11))]
        ], element_justification='center')],
        [sg.VPush()]
    ]
    
    transacoes = carregar_dados()
    dados_para_tabela = []
    for t in transacoes:
        dados_para_tabela.append([t['data'], t['descricao'], t['valor'], t['tipo'], t['categoria']])
    cabecalhos = ['Data', 'Descrição', 'Valor', 'Tipo', 'Categoria']

    layout_principal = [
        [sg.Text("Painel de Controle Financeiro", font=("Helvetica", 18), pad=((0,0), (0, 15)), justification='center', expand_x=True)],
        [sg.Text("Buscar por Descrição:", font=("Helvetica", 11)), 
         sg.InputText(key='-BUSCA-', size=(30, 1)), 
         sg.Button("Buscar", font=("Helvetica", 10)), 
         sg.Button("Limpar Busca", font=("Helvetica", 10))],
        [sg.Table(values=dados_para_tabela, headings=cabecalhos,
                  auto_size_columns=False, col_widths=[10, 35, 10, 10, 15],
                  justification='left', num_rows=20, key='-TABELA-',
                  pad=((0,0), (10, 10)), expand_x=True, expand_y=True)],
        [sg.Column([
            [sg.Button("Adicionar", font=("Helvetica", 12), size=(10, 1)), 
             sg.Button("Editar", font=("Helvetica", 12), size=(10, 1)), 
             sg.Button("Excluir", font=("Helvetica", 12), size=(10, 1)), 
             sg.Button("Sair do App", key='-SAIR_PRINCIPAL-', font=("Helvetica", 12), size=(10, 1))]
        ], element_justification='center', expand_x=True)]
    ]

    layout_mestre = [
        [sg.Column(layout_login, key='-PAINEL_LOGIN-', element_justification='center', expand_x=True, expand_y=True)],
        [sg.Column(layout_principal, visible=False, key='-PAINEL_PRINCIPAL-', expand_x=True, expand_y=True)]
    ]

    janela = sg.Window("Sistema Financeiro da Igreja", layout_mestre, finalize=True, resizable=True)
    janela.Maximize()

    dados_exibidos = list(transacoes)

    def atualizar_tabela(lista_de_dicionarios):
        dados_atualizados = []
        for t in lista_de_dicionarios:
            dados_atualizados.append([t['data'], t['descricao'], t['valor'], t['tipo'], t['categoria']])
        janela['-TABELA-'].update(values=dados_atualizados)

    while True:
        event, values = janela.read()

        if event == sg.WIN_CLOSED or event == "Sair" or event == '-SAIR_PRINCIPAL-':
            break
        
        if event == 'Login':
            usuario_correto = 'pedro'
            senha_correta = '1234'
            
            if values['-USUARIO-'] == usuario_correto and values['-SENHA-'] == senha_correta:
                sg.popup("Login realizado com sucesso!")
                janela['-PAINEL_LOGIN-'].update(visible=False)
                janela['-PAINEL_PRINCIPAL-'].update(visible=True)
            else:
                sg.popup_error('Usuário ou Senha incorretos.')

        if event == "Adicionar":
            nova_transacao = abrir_janela_adicionar()
            if nova_transacao:
                transacoes.append(nova_transacao)
                salvar_dados(transacoes)
                dados_exibidos = list(transacoes)
                atualizar_tabela(dados_exibidos)
                janela['-BUSCA-'].update('')
                sg.popup("Transação adicionada com sucesso!")

        elif event == "Excluir":
            if not values['-TABELA-']:
                sg.popup_error('Por favor, selecione uma transação na tabela para excluir.')
                continue
            
            resposta = sg.popup_yes_no("Tem certeza que deseja excluir a transação selecionada?", title="Confirmar Exclusão")
            
            if resposta == 'Yes':
                indice_selecionado = values['-TABELA-'][0]
                transacao_para_remover = dados_exibidos[indice_selecionado]
                transacoes.remove(transacao_para_remover)
                salvar_dados(transacoes)
                dados_exibidos = list(transacoes)
                atualizar_tabela(dados_exibidos)
                janela['-BUSCA-'].update('')
                sg.popup(f"A transação '{transacao_para_remover['descricao']}' foi excluída com sucesso!")
        
        elif event == "Editar":
            if not values['-TABELA-']:
                sg.popup_error("Por favor, selecione uma transação na tabela para editar.")
                continue

            indice_selecionado = values['-TABELA-'][0]
            transacao_para_editar = dados_exibidos[indice_selecionado]
            indice_real = transacoes.index(transacao_para_editar)
            
            dados_atualizados = abrir_janela_editar(transacao_para_editar)
            
            if dados_atualizados:
                transacoes[indice_real] = dados_atualizados
                salvar_dados(transacoes)
                dados_exibidos = list(transacoes)
                atualizar_tabela(dados_exibidos)
                janela['-BUSCA-'].update('')
                sg.popup("Transação editada com sucesso!")
        
        elif event == "Buscar":
            termo_busca = values['-BUSCA-'].lower()
            if termo_busca:
                resultados_busca = []
                for transacao in transacoes:
                    if termo_busca in transacao['descricao'].lower():
                        resultados_busca.append(transacao)
                dados_exibidos = resultados_busca
                atualizar_tabela(dados_exibidos)
        
        elif event == "Limpar Busca":
            dados_exibidos = list(transacoes)
            atualizar_tabela(dados_exibidos)
            janela['-BUSCA-'].update('')
    
    janela.close()

if __name__ == "__main__":
    main()