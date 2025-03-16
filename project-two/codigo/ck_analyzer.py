import os
import subprocess

def run_ck_analysis(repo_dir):
    """Executa o CK para gerar as métricas do código"""
    ck_jar_path = os.getenv('CK_PATH')
    result = subprocess.run(
        ['java', '-jar', ck_jar_path, repo_dir],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if result.stderr:
        print(f"Erro ao rodar o CK: {result.stderr.decode()}")
    return result.stdout.decode()