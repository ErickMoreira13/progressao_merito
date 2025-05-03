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

    return {
        "data_final": nova_data,
        "saldo_no_ano_novo": saldo_formatado,
        "tempo_efetivo_ate_ano_novo": tempo_exercicio_str,
        "tempo_em_exercicio_em_meses": tempo_exercicio_em_meses
    }