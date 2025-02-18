import csv
from utils.date_utils import calculate_days_since_update, calculate_repository_age
from utils.constants import CSV_FILENAME

def save_to_csv(repositories, filename=CSV_FILENAME):
    headers = [
        "Nome do Repositório",
        "Descrição",
        "URL",
        "Criado em",
        "Idade do Repositório (dias)",
        "Última Atualização",
        "Tempo desde última atualização (dias)",
        "Linguagem Principal",
        "Total PRs Mesclados",
        "Total de Releases",
        "Total de Issues",
        "Total de Issues Fechadas"
    ]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for repo in repositories:
            last_update = repo["pushedAt"]
            days_since_update = calculate_days_since_update(last_update)
            repository_age = calculate_repository_age(repo["createdAt"])

            writer.writerow([
                repo["name"],
                repo["description"] if repo["description"] else "Sem descrição",
                repo["url"],
                repo["createdAt"],
                repository_age,
                last_update,
                days_since_update,
                repo["primaryLanguage"]["name"] if repo["primaryLanguage"] else "N/A",
                repo["pullRequests"]["totalCount"],
                repo["releases"]["totalCount"],
                repo["issues"]["totalCount"],
                repo["closedIssues"]["totalCount"]
            ])

    print(f"Planilha gerada com sucesso: {filename}")
