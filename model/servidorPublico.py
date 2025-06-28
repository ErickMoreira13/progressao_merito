import pandas as pd

def extrair_dados_servidores(dados: pd.DataFrame):
    # Garante que as colunas estejam em maiúsculo sem acentos e espaços
    colunas = list(dados.columns)

    try:
        inicio = colunas.index("NOME SERVIDOR")
        fim = colunas.index("ATIVIDADE FUNÇÃO")
    except ValueError as e:
        raise ValueError("As colunas 'NOME SERVIDOR' e 'ATIVIDADE FUNÇÃO' devem existir na planilha.") from e

    colunas_servidor = colunas[inicio:fim+1]
    dados_servidores = dados[colunas_servidor].copy()

    # Converte DataFrame em lista de dicionários
    return dados_servidores.to_dict(orient="records")
