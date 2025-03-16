import csv
import os
from utils.date_utils import calculate_days_since_update, calculate_repository_age, format_date_iso_to_dmy
from ck_analyzer import run_ck_analysis  # Importa a função que executa o CK
from utils.constants import TODOS_REPOS_CSV, METRICAS_CSV  # Adicionei constantes para os dois CSVs

script_dir = os.path.dirname(os.path.abspath(__file__))
documentacao_dir = os.path.join(script_dir, "..", "documentacao")


def get_cloned_repositories():
    """Retorna a lista de repositórios que foram clonados na pasta ./repos/"""
    repos_dir = "./repos"
    if not os.path.exists(repos_dir):
        return []
    return [repo for repo in os.listdir(repos_dir) if os.path.isdir(os.path.join(repos_dir, repo))]


def save_all_repositories_to_csv(repositories):
    """
    Salva um CSV com os dados de TODOS os repositórios retornados pela API do GitHub.
    Este CSV NÃO contém métricas do CK, apenas as informações básicas.
    """
    file_path = os.path.join(documentacao_dir, TODOS_REPOS_CSV)
    headers = [
        "Nome do Repositório",
        "Descrição",
        "URL",
        "Criado em",
        "Última Atualização",
        "Linguagem Principal",
        "Número de Estrelas (Popularidade)",
        "Número de Releases (Atividade)"
    ]

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for repo in repositories:
            writer.writerow([
                repo["name"],
                repo["description"] if repo["description"] else "Sem descrição",
                repo["url"],
                format_date_iso_to_dmy(repo["createdAt"]),
                format_date_iso_to_dmy(repo["pushedAt"]),
                repo["primaryLanguage"]["name"] if repo["primaryLanguage"] else "N/A",
                repo["stargazerCount"],
                repo.get("releasesCount", "N/A")
            ])

    print(f"Planilha com todos os repositórios gerada: {file_path}")


def save_cloned_repositories_metrics_to_csv(repositories):
    """
    Salva um CSV com as métricas detalhadas apenas dos repositórios que foram clonados
    e analisados pelo CK.
    """
    file_path = os.path.join(documentacao_dir, METRICAS_CSV)
    headers = [
        "Nome do Repositório",
        "Descrição",
        "URL",
        "Criado em",
        "Idade do Repositório (dias)",
        "Última Atualização",
        "Tempo desde última atualização (dias)",
        "Linguagem Principal",
        "CBO (Coupling between Objects)",
        "DIT (Depth Inheritance Tree)",
        "LCOM (Lack of Cohesion of Methods)",
        "Número de Estrelas (Popularidade)",
        "Linhas de Código (Tamanho)",
        "Linhas de Comentários (Tamanho)",
        "Número de Releases (Atividade)"
    ]

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        cloned_repos = get_cloned_repositories()

        for repo in repositories:
            if repo['name'] not in cloned_repos:
                continue

            created_at_dmy = format_date_iso_to_dmy(repo["createdAt"])
            last_update_dmy = format_date_iso_to_dmy(repo["pushedAt"])

            days_since_update = calculate_days_since_update(last_update_dmy)
            repository_age = calculate_repository_age(created_at_dmy)

            repo_directory = f"./repos/{repo['name']}"
            ck_output = run_ck_analysis(repo_directory)

            cbo, dit, lcom = extract_metrics_from_ck_output(ck_output)

            stars = repo["stargazerCount"]
            loc = repo.get("loc", "N/A")
            comment_lines = repo.get("commentLines", "N/A")
            releases = repo.get("releasesCount", "N/A")

            writer.writerow([
                repo["name"],
                repo["description"] if repo["description"] else "Sem descrição",
                repo["url"],
                created_at_dmy,
                repository_age,
                last_update_dmy,
                days_since_update,
                repo["primaryLanguage"]["name"] if repo["primaryLanguage"] else "N/A",
                cbo,
                dit,
                lcom,
                stars,
                loc,
                comment_lines,
                releases
            ])

    print(f"Planilha com métricas dos repositórios clonados gerada: {file_path}")


def extract_metrics_from_ck_output(ck_output):
    """Extrai as métricas CBO, DIT e LCOM da saída do CK"""
    cbo = "N/A"
    dit = "N/A"
    lcom = "N/A"

    if ck_output:
        lines = ck_output.splitlines()
        for line in lines:
            parts = line.split(",")
            if len(parts) >= 4:
                cbo = parts[1].strip()
                dit = parts[2].strip()
                lcom = parts[3].strip()
                break

    return cbo, dit, lcom
