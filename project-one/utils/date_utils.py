from datetime import datetime

def format_date_iso_to_dmy(date_iso):
    """Converte uma data no formato ISO (YYYY-MM-DD) para d-m-y."""
    return datetime.strptime(date_iso[:10], "%Y-%m-%d").strftime("%d-%m-%Y")

def calculate_days_since_update(last_update_dmy):
    """Calcula quantos dias se passaram desde a última atualização."""
    data_atual = datetime.utcnow().date()
    data_ultima_atualizacao = datetime.strptime(last_update_dmy, "%d-%m-%Y").date()
    return (data_atual - data_ultima_atualizacao).days

def calculate_repository_age(created_at_dmy):
    """Calcula a idade do repositório (dias desde a criação)."""
    data_atual = datetime.utcnow().date()
    data_criacao = datetime.strptime(created_at_dmy, "%d-%m-%Y").date()
    return (data_atual - data_criacao).days