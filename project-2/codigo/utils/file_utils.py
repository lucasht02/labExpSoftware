import os
from .constants import TODOS_REPOS_CSV, METRICAS_CSV

script_dir = os.path.dirname(os.path.abspath(__file__))
documentacao_dir = os.path.join(script_dir, "..", "..", "documentacao")

def delete_old_files():
    """Exclui os arquivos JSON e CSV se existirem antes de gerar novos."""
    for filename in [TODOS_REPOS_CSV, METRICAS_CSV]:
        file_path = os.path.join(documentacao_dir, filename)

        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Arquivo deletado: {file_path}")
        else:
            print(f"Arquivo não encontrado: {file_path}")

def has_java_files(repo_dir):
    """Verifica se o repositório contém arquivos .java"""
    for root, dirs, files in os.walk(repo_dir):
        for file in files:
            if file.endswith(".java"):
                return True
    return False
