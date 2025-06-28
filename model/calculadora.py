from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def calcular_data_projetada(data_base: datetime, meses: int, saldo: int = 0, dia_add: int = 0):
    # Aplica o saldo nos meses
    meses_corrigidos = meses - saldo

    # Calcula a nova data
    nova_data = data_base + relativedelta(months=meses_corrigidos) + timedelta(days=dia_add)

    # Primeiro dia do ano da nova data
    inicio_ano = datetime(nova_data.year, 1, 1)

    # Tempo efetivo de exercício até 01/01
    tempo_exercicio = relativedelta(inicio_ano, data_base)
    tempo_exercicio_str = f"{tempo_exercicio.years} anos, {tempo_exercicio.months} meses, {tempo_exercicio.days} dias"

    # Saldo de meses desde 01/01 até nova data
    diferenca = relativedelta(nova_data, inicio_ano)
    saldo_meses = diferenca.years * 12 + diferenca.months
    saldo_dias = diferenca.days

    saldo_formatado = f"{saldo_meses} meses"
    if saldo_dias:
        saldo_formatado += f" e {saldo_dias} dias"

    # Tempo de exercício em meses
    tempo_exercicio_em_meses = tempo_exercicio.years * 12 + tempo_exercicio.months

    # Geração do alerta de progressão
    alerta = gerar_alerta_progressao(nova_data)

    resultado = {
        "data_final": nova_data,
        "tempo_em_exercicio_em_meses": tempo_exercicio_em_meses,
        "alerta_progressao": alerta
    }

    # Se meses for diferente de 12, adiciona o campo "saldo"
    if meses != 12:
        resultado["saldo"] = tempo_exercicio_em_meses - 12

    return resultado

def gerar_alerta_progressao(data_projetada: datetime):
    hoje = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    if data_projetada >= hoje:
        diff = relativedelta(data_projetada, hoje)
        diferenca_meses = diff.years * 12 + diff.months + (1 if diff.days > 0 else 0)
        if diferenca_meses > 3:
            return ""
        else:
            dias = (data_projetada - hoje).days
            if dias == 1:
                return "Falta 1 dia para a progressão"
            else:
                return f"Faltam {dias} dias para a progressão"
    else:
        dias_passados = (hoje - data_projetada).days
        if dias_passados == 1:
            return "Data da progressão passou 1 dia"
        else:
            return f"Data da progressão passou {dias_passados} dias"