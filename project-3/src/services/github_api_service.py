import random
import time
import requests
from src.constants.config_constant import HEADERS, PAGE_SIZE
from src.constants.url_constant import URL_GRAPHQL
from src.constants.limits_constant import MAX_PRS_PER_REPO, REQUEST_TIMEOUT, MIN_PRS
from src.services.utils_service import horas_entre_datas

def executar_query(query, variables=None, retries=5, delay=5, timeout=REQUEST_TIMEOUT):
    attempt = 0
    while attempt < retries:
        try:
            response = requests.post(
                URL_GRAPHQL,
                json={"query": query, "variables": variables or {}},
                headers=HEADERS,
                timeout=timeout
            )
            if response.status_code == 200:
                return response.json()
            elif response.status_code in (502, 503, 504):
                print(f"⚠️ Tentativa {attempt+1} falhou com status {response.status_code}. Retentando em {delay} segundos...")
            else:
                raise Exception(f"Erro GraphQL: {response.status_code}, {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Tentativa {attempt+1} falhou com exceção: {str(e)}. Retentando...")
        attempt += 1
        time.sleep(min(delay * (2 ** attempt), 60) + random.uniform(0, 2))  # Retry exponencial
    raise Exception(f"Erro GraphQL: Falha na conexão após {retries} tentativas.")


def get_pull_requests(repo_full_name, page_size=PAGE_SIZE):
    owner, name = repo_full_name.split('/')
    query = """
    query($owner: String!, $name: String!, $first: Int!, $after: String) {
      repository(owner: $owner, name: $name) {
        pullRequests(first: $first, after: $after, states: [MERGED, CLOSED], orderBy: {field: CREATED_AT, direction: DESC}) {
          pageInfo {
            hasNextPage
            endCursor
          }
          nodes {
            number
            createdAt
            closedAt
            mergedAt
            bodyText
            additions
            deletions
            changedFiles
            comments { totalCount }
            reviews { totalCount }
            participants { totalCount }
          }
        }
      }
    }
    """
    results = []
    after_cursor = None

    while True:
        variables = {
            "owner": owner,
            "name": name,
            "first": page_size,
            "after": after_cursor
        }

        try:
            data = executar_query(query, variables)
        except Exception as e:
            print(f"⚠️ Erro ao buscar PRs de {repo_full_name}: {e}")
            break

        pr_data = data.get("data", {}).get("repository", {}).get("pullRequests")
        if pr_data is None:
            print(f"⚠️ Dados inválidos para {repo_full_name}.")
            break

        for pr in pr_data["nodes"]:
            end = pr["mergedAt"] or pr["closedAt"]
            tempo_aberto_horas = horas_entre_datas(pr["createdAt"], end)
            if pr["reviews"]["totalCount"] >= 1 and tempo_aberto_horas >= 1:
                results.append({
                    "repo": repo_full_name,
                    "numero": pr["number"],
                    "arquivos": pr["changedFiles"],
                    "linhas_add": pr["additions"],
                    "linhas_rem": pr["deletions"],
                    "tempo_h": round(tempo_aberto_horas, 2),
                    "descricao_len": len(pr["bodyText"]),
                    "comentarios": pr["comments"]["totalCount"],
                    "participantes": pr["participants"]["totalCount"],
                    "status": "merged" if pr["mergedAt"] else "closed",
                    "reviews": pr["reviews"]["totalCount"]
                })
                if len(results) >= MAX_PRS_PER_REPO:
                    return results

        if not pr_data["pageInfo"]["hasNextPage"]:
            break

        after_cursor = pr_data["pageInfo"]["endCursor"]

    if len(results) < MIN_PRS:
        print(f"⚠️ Apenas {len(results)} PRs válidos encontrados para {repo_full_name}, mínimo era 100.")
        return []
    
    return results






