import json
from utils.date_utils import format_date_iso_to_dmy, calculate_days_since_update, calculate_repository_age
from utils.constants import JSON_FILENAME

def process_repositories(repositories):
    """Formata as datas e adiciona métricas antes de salvar no JSON."""
    for repo in repositories:
        repo["createdAt"] = format_date_iso_to_dmy(repo["createdAt"])
        repo["pushedAt"] = format_date_iso_to_dmy(repo["pushedAt"])
        repo["daysSinceUpdate"] = calculate_days_since_update(repo["pushedAt"])
        repo["repositoryAge"] = calculate_repository_age(repo["createdAt"])
    return repositories

def save_json(repositories, filename=JSON_FILENAME):
    """Salva os repositórios formatados em JSON."""
    repositories = process_repositories(repositories)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(repositories, f, indent=2, ensure_ascii=False)

    print(f"JSON gerado com sucesso: {filename}")
