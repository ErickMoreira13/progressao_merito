from model import calculadora
from model.planilha import processar_planilha, selecionar_arquivo, mostrar_resultado_em_tabela
import pandas as pd

def formatar_data(data):
    return data.strftime("%d/%m/%Y")

class Controlador:
    def __init__(self, voltar_callback):
        self.voltar_callback = voltar_callback

    def acionar_leitura_planilha(self, meses_intersticio=18):
        caminho = selecionar_arquivo()
        if not caminho:
            print("Nenhum arquivo selecionado.")
            return

        try:
            dados = processar_planilha(caminho)
        except Exception as e:
            print(f"Erro ao processar a planilha: {e}")
            return

        resultados = []

        for _, linha in dados.iterrows():
            nome = linha["NOME SERVIDOR"]
            data_inicio = linha["INTERSTÍCIO INÍCIO"]

            if pd.isna(data_inicio):
                continue

            resultado = calculadora.calcular_data_projetada(data_inicio, meses=meses_intersticio)

            resultados.append({
                "NOME SERVIDOR": nome,
                "INTERSTÍCIO INÍCIO": formatar_data(data_inicio),
                "MESES USADOS": meses_intersticio,
                "DATA PROJETADA": formatar_data(resultado["data_final"]),
                "SALDO NO ANO NOVO": resultado["saldo_no_ano_novo"],
                "TEMPO EFETIVO ATÉ 01/01": resultado["tempo_efetivo_ate_ano_novo"],
                "TEMPO EM EXERCÍCIO EM MESES": resultado["tempo_em_exercicio_em_meses"]
            })

        mostrar_resultado_em_tabela(resultados, caminho, self.voltar_callback)