from src.services.repo_collector_service import get_top_repositories
from src.services.github_api_service import get_pull_requests
from src.services.export_service import exportar_prs_para_csv
from src.constants.limits_constant import MAX_REPOS
import os
import time

def processar_200_populares_com_prs_validos():
    os.makedirs("data", exist_ok=True)

    csv_path = "data/pull_requests.csv"
    if os.path.exists(csv_path):
        os.remove(csv_path)
        print("🧹 Arquivo pull_requests.csv antigo removido.")

    pagina = 1
    repos_validos = 0
    repos_checados_total = 0

    while repos_validos < MAX_REPOS:
        print(f"\n🔎 Buscando página {pagina} de repositórios populares...")
        candidatos = get_top_repositories(pagina=pagina)

        if not candidatos:
            print("⚠️ Nenhum repositório retornado nesta página.")
            break

        for repo in candidatos:
            repos_checados_total += 1
            if repos_validos >= MAX_REPOS:
                break

            print(f"📦 Verificando {repo}...")
            try:
                prs = get_pull_requests(repo)
                if len(prs) >= 100:
                    exportar_prs_para_csv(prs, append=True)
                    repos_validos += 1
                    print(f"✅ {repo} adicionado ({repos_validos}/{MAX_REPOS})")
                else:
                    print(f"⏭️ {repo} ignorado (apenas {len(prs)} PRs válidos)")
            except Exception as e:
                print(f"❌ Erro ao processar {repo}: {e}")

            time.sleep(2)

        pagina += 1

    print(f"\n🏁 Finalizado! {repos_validos} repositórios válidos salvos, após checar {repos_checados_total} repositórios populares.")

if __name__ == "__main__":
    processar_200_populares_com_prs_validos()
