import csv
from datetime import datetime

def save_to_csv(repositories, filename="repositorios.csv"):
    headers = [
        "Nome do Repositório",
        "Descrição",
        "URL",
        "Criado em",
        "Última Atualização",
        "Tempo até Última Atualização (dias)",
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
            ultima_atualizacao_iso = repo["pushedAt"]
            data_ultima_atualizacao = datetime.strptime(ultima_atualizacao_iso, "%d-%m-%Y").date()
            data_atual = datetime.utcnow().date()
            tempo_ate_atualizacao = (data_atual - data_ultima_atualizacao).days

            criado_em = repo["createdAt"]

            writer.writerow([
                repo["name"],
                repo["description"] if repo["description"] else "Sem descrição",
                repo["url"],
                criado_em,
                ultima_atualizacao_iso,
                tempo_ate_atualizacao,
                repo["primaryLanguage"]["name"] if repo["primaryLanguage"] else "N/A",
                repo["pullRequests"]["totalCount"],
                repo["releases"]["totalCount"],
                repo["issues"]["totalCount"],
                repo["closedIssues"]["totalCount"]
            ])

    print(f"Planilha gerada com sucesso: {filename}")
