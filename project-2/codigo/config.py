import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('API_KEY')

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

URL = "https://api.github.com/graphql"
PAGE_SIZE = 25
MAX_REPOSITORIES = 1000
