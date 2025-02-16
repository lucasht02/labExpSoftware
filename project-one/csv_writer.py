import csv
from date_utils import calculate_days_since_update

def save_to_csv(repositories, filename="repositorios.csv"):
    headers = [
        "Nome do Repositório",
        "Descrição",
        "URL",
        "Criado em",
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
            ultima_atualizacao = repo["pushedAt"]
            tempo_ate_atualizacao = calculate_days_since_update(ultima_atualizacao)

            writer.writerow([
                repo["name"],
                repo["description"] if repo["description"] else "Sem descrição",
                repo["url"],
                repo["createdAt"],
                ultima_atualizacao,
                tempo_ate_atualizacao,
                repo["primaryLanguage"]["name"] if repo["primaryLanguage"] else "N/A",
                repo["pullRequests"]["totalCount"],
                repo["releases"]["totalCount"],
                repo["issues"]["totalCount"],
                repo["closedIssues"]["totalCount"]
            ])

    print(f"Planilha gerada com sucesso: {filename}")
