import pandas as pd
from tkinter import Tk, filedialog, messagebox
import unicodedata
import os
from tkinter import Toplevel, Button, ttk, Label, Scrollbar

def selecionar_arquivo():
    Tk().withdraw()
    caminho = filedialog.askopenfilename(
        title="Selecione a planilha",
        filetypes=[("Planilhas Excel ou CSV", "*.xlsx *.csv")]
    )
    return caminho

def normalizar_coluna(col):
    col = unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('ASCII')
    return col.strip().upper()

def processar_planilha(caminho_arquivo):
    if caminho_arquivo.endswith(".csv"):
        dados = pd.read_csv(caminho_arquivo, dayfirst=True)
    else:
        dados = pd.read_excel(caminho_arquivo, header=2)

    print("Colunas reais:", dados.columns.tolist())

    dados.columns = [col.strip().upper() for col in dados.columns]

    colunas_obrigatorias = {"NOME SERVIDOR", "INTERSTÍCIO INÍCIO"}
    if not colunas_obrigatorias.issubset(dados.columns):
        raise ValueError("A planilha deve conter ao menos as colunas obrigatórias: 'NOME SERVIDOR' e 'INTERSTÍCIO INÍCIO'")

    dados["INTERSTÍCIO INÍCIO"] = pd.to_datetime(dados["INTERSTÍCIO INÍCIO"], dayfirst=True, errors='coerce')

    return dados

def gerar_planilha_resposta(lista_resultados, caminho_original):
    df_resultado = pd.DataFrame(lista_resultados)
    novo_nome = os.path.splitext(caminho_original)[0] + "_resultado.xlsx"
    df_resultado.to_excel(novo_nome, index=False)
    return novo_nome

def salvar_como_csv(lista_resultados, caminho_original):
    df_resultado = pd.DataFrame(lista_resultados)
    novo_nome = os.path.splitext(caminho_original)[0] + "_resultado.csv"
    df_resultado.to_csv(novo_nome, index=False, sep=';', encoding='utf-8-sig')
    return novo_nome

def mostrar_resultado_em_tabela(lista_resultados, caminho_original, voltar_callback):
    janela = Toplevel()
    janela.title("Resultado da Análise")
    janela.geometry("900x500")

    frame = ttk.Frame(janela)
    frame.pack(fill='both', expand=True)

    colunas = list(lista_resultados[0].keys())

    # Criando a barra de rolagem vertical
    scroll_vertical = Scrollbar(frame, orient="vertical")
    scroll_vertical.pack(side='right', fill='y')

    # Criando a barra de rolagem horizontal
    scroll_horizontal = Scrollbar(frame, orient="horizontal")
    scroll_horizontal.pack(side='bottom', fill='x')

    # Criando a Treeview (tabela)
    tree = ttk.Treeview(frame, columns=colunas, show='headings', yscrollcommand=scroll_vertical.set, xscrollcommand=scroll_horizontal.set)

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, anchor='center')

    for item in lista_resultados:
        valores = [item[col] for col in colunas]
        tree.insert('', 'end', values=valores)

    tree.pack(fill='both', expand=True)

    # Associando as barras de rolagem
    scroll_vertical.config(command=tree.yview)
    scroll_horizontal.config(command=tree.xview)

    def salvar_xlsx():
        caminho = gerar_planilha_resposta(lista_resultados, caminho_original)
        messagebox.showinfo("Sucesso", f"Planilha salva em: {caminho}")

    def salvar_csv():
        caminho = salvar_como_csv(lista_resultados, caminho_original)
        messagebox.showinfo("Sucesso", f"Planilha CSV salva em: {caminho}")

    botoes_frame = ttk.Frame(janela)
    botoes_frame.pack(pady=10)

    btn_xlsx = Button(botoes_frame, text="Salvar como Excel", command=salvar_xlsx)
    btn_xlsx.grid(row=0, column=0, padx=5)

    btn_csv = Button(botoes_frame, text="Salvar como CSV", command=salvar_csv)
    btn_csv.grid(row=0, column=1, padx=5)

    btn_voltar = Button(botoes_frame, text="Voltar à Tela Inicial", command=lambda: [janela.destroy(), voltar_callback(janela)])
    btn_voltar.grid(row=0, column=2, padx=5)
    
    # Para fechar a janela corretamente e manter a funcionalidade de voltar
    janela.protocol("WM_DELETE_WINDOW", lambda: [janela.destroy(), voltar_callback(janela)])


