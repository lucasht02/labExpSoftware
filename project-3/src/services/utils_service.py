from datetime import datetime

def horas_entre_datas(inicio: str, fim: str) -> float:
    fmt = "%Y-%m-%dT%H:%M:%SZ"
    delta = datetime.strptime(fim, fmt) - datetime.strptime(inicio, fmt)
    return delta.total_seconds() / 3600
