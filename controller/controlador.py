from model import calculadora
from model.servidorPublico import extrair_dados_servidores
from model.planilha import processar_planilha, selecionar_arquivo, mostrar_resultado_em_tabela
import pandas as pd

def formatar_data(data):
    return data.strftime("%d/%m/%Y")

class Controlador:
    def __init__(self, voltar_callback):
        self.voltar_callback = voltar_callback
        self.meses_intersticio = 12 
        self.nota_corte = 7.0 

    def acionar_leitura_planilha(self, caminho):
        if not caminho:
            print("Nenhum arquivo selecionado.")
            return

        try:
            dados = processar_planilha(caminho)
            dados_servidores = extrair_dados_servidores(dados)
        except Exception as e:
            print(f"Erro ao processar a planilha: {e}")
            return

        resultados = []
        for idx, linha in dados.iterrows():
            data_inicio = linha["INTERSTÍCIO INÍCIO"]
            nota = linha.get("NOTA", None)
            deducoes = linha.get("DEDUÇÕES LEGAIS AO EFETIVO EXERCÍCIO", 0)
            deducoes = 0 if pd.isna(deducoes) else int(deducoes)

            if pd.isna(data_inicio):
                continue

            resultado = calculadora.calcular_data_projetada(data_inicio, meses=self.meses_intersticio, dia_add=int(deducoes))

            resultado_apd = {
                "INTERSTÍCIO INÍCIO": formatar_data(data_inicio),
                "MESES PARA INTERSTÍCIO": self.meses_intersticio,
                "DATA PROGRESSÃO": formatar_data(resultado["data_final"]),
                "TEMPO EM EXERCÍCIO EM MESES": resultado["tempo_em_exercicio_em_meses"],
            }

            if self.meses_intersticio != 12:
                resultado_apd["SALDO"] = max(resultado["saldo"], 0)

            resultado_apd["NOTA"] = nota
            resultado_apd["ESTÁ APTO PARA A PROGRESSÃO?"] = "Sim" if nota >= self.nota_corte else "Não"
            resultado_apd["ALERTA DE PROGRESSÃO"] = resultado["alerta_progressao"]

            # Junta dados do servidor com os resultados da progressão
            resultado_completo = {**dados_servidores[idx], **resultado_apd}
            resultados.append(resultado_completo)

        mostrar_resultado_em_tabela(resultados, caminho, self.voltar_callback)

    def atualizar_configuracoes(self, meses, nota):
        self.meses_intersticio = meses
        self.nota_corte = nota
