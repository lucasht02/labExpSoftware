import os # Usado para acessar variáveis de ambiente do sistema
from dotenv import load_dotenv # Carrega automaticamente as variáveis definidas no arquivo .env

# Carrega as variáveis do .env para o ambiente, tornando-as acessíveis via os.getenv da ln 8.
load_dotenv()

# Lê a variável API_KEY do .env (que deve conter seu token GitHub) e armazena na variável TOKEN
TOKEN = os.getenv('API_KEY')


# Define os headers HTTP que serão usados nas requisições à API GraphQL do GitHub
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json" # informa que o corpo da requisição estará em JSON.
}

PAGE_SIZE = 10
MAX_REPOSITORIES = 1000