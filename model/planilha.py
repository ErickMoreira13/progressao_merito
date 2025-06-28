import pandas as pd
from tkinter import Canvas, Frame, Tk, filedialog, messagebox
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
    janela.geometry("1000x500")

    frame = Frame(janela)
    frame.pack(fill='both', expand=True)

    canvas = Canvas(frame)
    canvas.pack(side='left', fill='both', expand=True)

    vsb = Scrollbar(frame, orient="vertical", command=canvas.yview)
    vsb.pack(side='right', fill='y')

    hsb = Scrollbar(janela, orient="horizontal", command=canvas.xview)
    hsb.pack(side='bottom', fill='x')

    canvas.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tabela_frame = Frame(canvas)
    canvas.create_window((0, 0), window=tabela_frame, anchor='nw')

    colunas = list(lista_resultados[0].keys())
    row_refs = {}
    selected_row = {"index": None}

    def selecionar_linha(idx):
        # Limpar linha anterior
        if selected_row["index"] is not None:
            for label in row_refs[selected_row["index"]]:
                label.config(bg=label.original_bg)

        # Marcar nova linha
        for label in row_refs[idx]:
            label.config(bg="#cce5ff")
        selected_row["index"] = idx

    # Cabeçalho
    for j, col in enumerate(colunas):
        lbl = Label(
            tabela_frame, text=col, bg="#cccccc",
            anchor='center', padx=10, pady=5,
            bd=1, relief="groove", highlightthickness=0
        )
        lbl.grid(row=0, column=j, sticky='nsew')

    # Dados + clique para seleção
    for i, item in enumerate(lista_resultados, start=1):
        row_labels = []
        for j, col in enumerate(colunas):
            valor = item[col]
            cor = "white"
            if col.upper() == "ESTÁ APTO PARA A PROGRESSÃO?":
                if str(valor).strip().lower() == "sim":
                    cor = "#42ff42"
                elif str(valor).strip().lower() in ("não", "nao"):
                    cor = "#ff4242"

            lbl = Label(
                tabela_frame, text=valor, bg=cor,
                anchor='center', padx=10, pady=5,
                bd=1, relief="groove", highlightthickness=0
            )
            lbl.original_bg = cor
            lbl.grid(row=i, column=j, sticky='nsew')

            # Ação de clique
            lbl.bind("<Button-1>", lambda e, idx=i: selecionar_linha(idx))
            row_labels.append(lbl)
        row_refs[i] = row_labels

    for j in range(len(colunas)):
        tabela_frame.grid_columnconfigure(j, weight=1)

    # Scroll com roda do mouse
    def on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", on_mousewheel)

    # Botões
    def salvar_xlsx():
        caminho = gerar_planilha_resposta(lista_resultados, caminho_original)
        messagebox.showinfo("Sucesso", f"Planilha salva em: {caminho}")

    def salvar_csv():
        caminho = salvar_como_csv(lista_resultados, caminho_original)
        messagebox.showinfo("Sucesso", f"Planilha CSV salva em: {caminho}")

    botoes_frame = Frame(janela)
    botoes_frame.pack(pady=10)

    Button(botoes_frame, text="Salvar como Excel", command=salvar_xlsx).grid(row=0, column=0, padx=5)
    Button(botoes_frame, text="Salvar como CSV", command=salvar_csv).grid(row=0, column=1, padx=5)
    Button(botoes_frame, text="Voltar à Tela Inicial", command=lambda: [janela.destroy(), voltar_callback(janela)]).grid(row=0, column=2, padx=5)

    tabela_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Para fechar a janela corretamente e manter a funcionalidade de voltar
    janela.protocol("WM_DELETE_WINDOW", lambda: [janela.destroy(), voltar_callback(janela)])