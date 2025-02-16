import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('API_KEY')

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

url = "https://api.github.com/graphql"

repositories = []
has_next_page = True
cursor = None
page_size = 25  

while has_next_page and len(repositories) < 100:
    query = """
    query ($queryString: String!, $pageSize: Int!, $cursor: String) {
      search(query: $queryString, type: REPOSITORY, first: $pageSize, after: $cursor) {
        pageInfo {
          hasNextPage
          endCursor
        }
        edges {
          node {
            ... on Repository {
              name
              description
              url
              createdAt
              updatedAt
              primaryLanguage {
                name
              }
              pullRequests(states: MERGED) {
                totalCount
              }
              releases {
                totalCount
              }
              issues {
                totalCount
              }
              closedIssues: issues(states: CLOSED) {
                totalCount
              }
            }
          }
        }
      }
    }
    """
    
    variables = {
        "queryString": "stars:>1 sort:stars-desc",
        "pageSize": page_size,
        "cursor": cursor
    }
    
    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        if 'errors' in result:
            print("Erros na query:", result['errors'])
            break
        
        search_data = result['data']['search']
        for edge in search_data['edges']:
            repositories.append(edge['node'])
            if len(repositories) >= 100:
                break
        
        has_next_page = search_data['pageInfo']['hasNextPage']
        cursor = search_data['pageInfo']['endCursor']
        
        
        time.sleep(1)
    else:
        print(f"Falha na requisição: {response.status_code}")
        print(response.text)
        break

print(json.dumps(repositories, indent=2, ensure_ascii=False))
