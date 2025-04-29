import os 
from dotenv import load_dotenv 

load_dotenv()

TOKEN = os.getenv('API_KEY')

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json" 
}

PAGE_SIZE = 10
MAX_REPOSITORIES = 1000