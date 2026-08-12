from datetime import datetime, time

JORNADA_DIARIA = 8 * 60
TOLERANCIA = 10

def calcular_minutos(hora_inicio:time,
                     hora_fim:time) -> int:
    inicio = datetime.combine(datetime.today(),
                              hora_inicio)
    fim = datetime.combine(datetime.today(), hora_fim)

    diferenca = fim - inicio

    return int(diferenca.total_seconds() / 60)

def calcular_horas_trabalhadas(entrada: time,
                               saida_almoco: time,
                               volta_almoco: time,
                               saida: time):
    periodo_manha = calcular_minutos(entrada, saida_almoco)
    periodo_tarde = calcular_minutos(volta_almoco, saida)

    total_minutos = periodo_manha + periodo_tarde

    diferenca = total_minutos - JORNADA_DIARIA

    if abs(diferenca) <= TOLERANCIA:
        diferenca = 0

    horas = total_minutos //60
    minutos = total_minutos % 60

    return {"total_minutos": total_minutos,
            "horas_trabalhadas": f"{horas:02d}:{minutos:02d}",
            "diferenca_minutos": diferenca}

  