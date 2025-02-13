import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

token = os.getenv('API_KEY')

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

query = """
query {
  search(query: "machine learning", type: REPOSITORY, first: 10) {
    edges {
      node {
        ... on Repository {
          name
          description
          url
        }
      }
    }
  }
}
"""

url = "https://api.github.com/graphql"

response = requests.post(url, json={'query': query}, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=2, ensure_ascii=False))
else:
    print(f"Falha na requisição: {response.status_code}")
    print(response.text)
