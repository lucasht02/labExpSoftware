import requests
import time
from config import URL, HEADERS, PAGE_SIZE, MAX_REPOSITORIES

def load_query(filename="query.graphql"):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

def fetch_repositories():
    repositories = []
    has_next_page = True
    cursor = None
    query = load_query()

    while has_next_page and len(repositories) < MAX_REPOSITORIES:
        variables = {
            "queryString": "stars:>1 sort:stars-desc",
            "pageSize": PAGE_SIZE,
            "cursor": cursor
        }

        response = requests.post(URL, json={'query': query, 'variables': variables}, headers=HEADERS)

        if response.status_code == 200:
            result = response.json()
            if 'errors' in result:
                print("Erros na query:", result['errors'])
                break

            search_data = result['data']['search']
            for edge in search_data['edges']:
                repositories.append(edge['node'])
                if len(repositories) >= MAX_REPOSITORIES:
                    break

            has_next_page = search_data['pageInfo']['hasNextPage']
            cursor = search_data['pageInfo']['endCursor']

            time.sleep(1)
        else:
            print(f"Falha na requisição: {response.status_code}")
            print(response.text)
            break

    return repositories
