import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import unicodedata
import os

def selecionar_arquivo():
    Tk().withdraw()
    caminho = askopenfilename(
        title="Selecione a planilha",
        filetypes=[("Planilhas Excel ou CSV", "*.xlsx *.csv")]
    )
    return caminho

def normalizar_coluna(col):
    # Remove acentos e transforma em maiúsculas sem espaços extras
    col = unicodedata.normalize('NFKD', col).encode('ASCII', 'ignore').decode('ASCII')
    return col.strip().upper()

def processar_planilha(caminho_arquivo):
    if caminho_arquivo.endswith(".csv"):
        dados = pd.read_csv(caminho_arquivo, dayfirst=True)
    else:
        # Usa a terceira linha (índice 2) como cabeçalho
        dados = pd.read_excel(caminho_arquivo, header=2)

    print("Colunas reais:", dados.columns.tolist())

    # Normaliza e mapeia colunas
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