import csv
import os
import pandas as pd
import concurrent.futures
from utils.date_utils import calculate_days_since_update, calculate_repository_age, format_date_iso_to_dmy
from ck_analyzer import run_ck_analysis
from utils.constants import TODOS_REPOS_CSV, METRICAS_CSV

script_dir = os.path.dirname(os.path.abspath(__file__))
documentacao_dir = os.path.join(script_dir, "..", "documentacao")

def load_cloned_repositories_from_csv(csv_file_path):
    """
    Carrega os dados dos repositórios a partir de um arquivo CSV.
    O CSV deve conter pelo menos as colunas:
      - Nome do Repositório
      - Descrição
      - URL
      - Criado em (no formato ISO ou compatível)
      - Última Atualização (no formato ISO ou compatível)
      - Linguagem Principal
      - Número de Estrelas (Popularidade)
      - Número de Releases (Atividade)
    """
    repositories = []
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            repo = {
                "name": row["Nome do Repositório"],
                "description": row["Descrição"],
                "url": row["URL"],
                # Se as datas no CSV estiverem em um formato diferente do ISO, você poderá precisar ajustá-las
                "createdAt": row["Criado em"],
                "pushedAt": row["Última Atualização"],
                "primaryLanguage": {"name": row["Linguagem Principal"]} if row["Linguagem Principal"] else None,
                "stargazerCount": int(row["Número de Estrelas (Popularidade)"]) if row["Número de Estrelas (Popularidade)"] else 0,
                "releases": {"totalCount": int(row["Número de Releases (Atividade)"]) if row["Número de Releases (Atividade)"] else 0}
            }
            repositories.append(repo)
    return repositories

def get_cloned_repositories():
    """Retorna a lista de repositórios clonados na pasta ./repos/."""
    repos_dir = "./repos"
    if not os.path.exists(repos_dir):
        return []
    return [repo for repo in os.listdir(repos_dir) if os.path.isdir(os.path.join(repos_dir, repo))]

def save_all_repositories_to_csv(repositories):
    """
    Salva um CSV com os dados de TODOS os repositórios retornados pela API do GitHub.
    Este CSV NÃO contém as métricas do CK, apenas informações básicas.
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
                repo["releases"]["totalCount"]
            ])

    print(f"Planilha com todos os repositórios gerada: {file_path}")

def extract_metrics_from_ck_output():
    """
    Extrai as métricas (CBO, DIT, LCOM, LOC e linhas de comentários) do arquivo 'class.csv'
    gerado pelo CK na pasta atual.
    Para CBO, DIT e LCOM, calcula média, mediana e desvio padrão.
    """
    # Valores padrões caso não seja possível extrair
    cbo_mean = cbo_median = cbo_std = "N/A"
    dit_mean = dit_median = dit_std = "N/A"
    lcom_mean = lcom_median = lcom_std = "N/A"
    loc = "N/A"
    comment_lines = "N/A"

    if os.path.exists("class.csv"):
        try:
            df_class = pd.read_csv("class.csv")

            if not df_class.empty:
                if "cbo" in df_class.columns:
                    cbo_mean = round(df_class["cbo"].mean(), 2)
                    cbo_median = round(df_class["cbo"].median(), 2)
                    cbo_std = round(df_class["cbo"].std(), 2)
                if "dit" in df_class.columns:
                    dit_mean = round(df_class["dit"].mean(), 2)
                    dit_median = round(df_class["dit"].median(), 2)
                    dit_std = round(df_class["dit"].std(), 2)
                if "lcom" in df_class.columns:
                    lcom_mean = round(df_class["lcom"].mean(), 2)
                    lcom_median = round(df_class["lcom"].median(), 2)
                    lcom_std = round(df_class["lcom"].std(), 2)
                if "loc" in df_class.columns:
                    loc = int(df_class["loc"].sum())
                if "logStatementsQty" in df_class.columns:
                    comment_lines = int(df_class["logStatementsQty"].sum())
        except Exception as e:
            print(f"Erro ao processar class.csv: {e}")

    return (cbo_mean, cbo_median, cbo_std,
            dit_mean, dit_median, dit_std,
            lcom_mean, lcom_median, lcom_std,
            loc, comment_lines)

def process_repo(repo):
    """
    Processa um repositório: calcula as datas, executa a análise CK e extrai as métricas.
    Para isolar a análise, muda o diretório atual para o do repositório e depois restaura.
    Retorna uma lista com os dados a serem escritos na planilha.
    """
    # Formata as datas
    created_at_dmy = repo["createdAt"]
    last_update_dmy = repo["pushedAt"]
    days_since_update = calculate_days_since_update(last_update_dmy)
    repository_age = calculate_repository_age(created_at_dmy)
    
    repo_dir = os.path.join("repos", repo["name"])
    original_dir = os.getcwd()
    
    try:
        # Muda para o diretório do repositório para que o CK escreva o class.csv nele
        os.chdir(repo_dir)
        run_ck_analysis(".")
        (cbo_mean, cbo_median, cbo_std,
         dit_mean, dit_median, dit_std,
         lcom_mean, lcom_median, lcom_std,
         loc, comment_lines) = extract_metrics_from_ck_output()
    except Exception as e:
        print(f"Erro ao analisar {repo['name']}: {e}")
        cbo_mean = cbo_median = cbo_std = "Erro"
        dit_mean = dit_median = dit_std = "Erro"
        lcom_mean = lcom_median = lcom_std = "Erro"
        loc = comment_lines = "Erro"
    finally:
        os.chdir(original_dir)
    
    stars = repo["stargazerCount"]
    releases = repo["releases"]["totalCount"]
    primary_language = repo["primaryLanguage"]["name"] if repo["primaryLanguage"] else "N/A"
    
    return [
        repo["name"],
        repo["description"] if repo["description"] else "Sem descrição",
        repo["url"],
        created_at_dmy,
        repository_age,
        last_update_dmy,
        days_since_update,
        primary_language,
        cbo_mean,
        cbo_median,
        cbo_std,
        dit_mean,
        dit_median,
        dit_std,
        lcom_mean,
        lcom_median,
        lcom_std,
        stars,
        loc,
        comment_lines,
        releases
    ]

def repo_is_cloned(repo_name, cloned_folders):
    """
    Retorna True se houver uma pasta em cloned_folders cujo nome seja exatamente
    repo_name ou que comece com 'repo_name_'.
    """
    return any(folder == repo_name or folder.startswith(f"{repo_name}_") for folder in cloned_folders)

def save_cloned_repositories_metrics_to_csv_parallel(max_workers=5):
    """
    Salva um CSV com as métricas detalhadas apenas dos repositórios que foram clonados
    e analisados pelo CK.
    A análise de cada repositório é realizada em paralelo.
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
        "CBO Média",
        "CBO Mediana",
        "CBO Desvio Padrão",
        "DIT Média",
        "DIT Mediana",
        "DIT Desvio Padrão",
        "LCOM Média",
        "LCOM Mediana",
        "LCOM Desvio Padrão",
        "Número de Estrelas (Popularidade)",
        "Linhas de Código (Tamanho)",
        "Linhas de Comentários (Tamanho)",
        "Número de Releases (Atividade)"
    ]

    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(script_dir, "..", "documentacao", "todos_repositorios.csv")

    repositories = load_cloned_repositories_from_csv(csv_file_path)
    cloned_repos = get_cloned_repositories()

    repos_to_analyze = [repo for repo in repositories if repo_is_cloned(repo["name"], cloned_repos)]

    # Abre o arquivo CSV e escreve o cabeçalho
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        # Cria o executor para processar os repositórios em paralelo
        with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(process_repo, repo): repo for repo in repos_to_analyze}
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    writer.writerow(result)
                    f.flush()  # Garante que os dados sejam escritos imediatamente
                    print(f"Análise concluída para: {result[0]}")
                except Exception as e:
                    print(f"Erro ao processar o repositório: {e}")

    print(f"Planilha com métricas dos repositórios clonados gerada: {file_path}")
