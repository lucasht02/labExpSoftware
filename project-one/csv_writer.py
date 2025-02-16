import csv

def save_to_csv(repositories, filename="repositorios.csv"):
    headers = [
        "Nome do Repositório",
        "Descrição",
        "URL",
        "Criado em",
        "Última Atualização",
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
            writer.writerow([
                repo["name"],
                repo["description"] if repo["description"] else "Sem descrição",
                repo["url"],
                repo["createdAt"][:10],
                repo["updatedAt"][:10],
                repo["primaryLanguage"]["name"] if repo["primaryLanguage"] else "N/A",
                repo["pullRequests"]["totalCount"],
                repo["releases"]["totalCount"],
                repo["issues"]["totalCount"],
                repo["closedIssues"]["totalCount"]
            ])

    print(f"Planilha gerada com sucesso: {filename}")
