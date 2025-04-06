from src.services.repo_collector_service import get_top_repositories
from src.services.github_api_service import get_pull_requests
from src.services.export_service import exportar_prs_para_csv

def gerar_repos_txt():
    repos = get_top_repositories()
    with open("data/repos.txt", "w") as f:
        for repo in repos:
            f.write(repo + "\n")
    print(f"✅ {len(repos)} repositórios salvos.")

def processar_repos():
    with open("data/repos.txt") as f:
        repos = [line.strip() for line in f if line.strip()]

    for repo in repos:
        print(f"📦 Coletando PRs de {repo}")
        prs = get_pull_requests(repo)
        if prs:
            exportar_prs_para_csv(prs, append=True)
        else:
            print(f"⚠️ Nenhum PR válido encontrado para {repo}.")

if __name__ == "__main__":
    gerar_repos_txt()
    processar_repos()
