import git
import os
import random
import concurrent.futures

def get_unique_clone_dir(base_dir, repo_name):
    """
    Retorna um caminho único para clonar o repositório.
    Se já existir './base_dir/repo_name', adiciona um sufixo '_1', '_2', etc.
    """
    clone_dir = os.path.join(base_dir, repo_name)
    if not os.path.exists(clone_dir):
        return clone_dir

    counter = 1
    while True:
        new_clone_dir = f"{clone_dir}_{counter}"
        if not os.path.exists(new_clone_dir):
            return new_clone_dir
        counter += 1

def clone_repository(repo_url, clone_dir):
    """Clona o repositório no diretório especificado."""
    if not os.path.exists(clone_dir):
        os.makedirs(clone_dir)
    git.Repo.clone_from(repo_url, clone_dir)

def clone_repositories_parallel(repos, num_repos_to_clone=1, max_workers=5):
    """
    Clona até 'num_repos_to_clone' repositórios da lista fornecida em paralelo.
    """
    if not repos:
        print("Nenhum repositório encontrado.")
        return

    repos_to_clone = random.sample(repos, min(num_repos_to_clone, len(repos)))

    print("\nLista de repositórios escolhidos para clonagem:")
    for repo in repos_to_clone:
        print(f"- {repo['name']} ({repo['url']})")

    print("\nIniciando clonagem em paralelo...\n")

    base_clone_dir = "./repos"
    if not os.path.exists(base_clone_dir):
        os.makedirs(base_clone_dir)

    def clone_task(repo):
        repo_name = repo['name']
        repo_url = repo['url']
        # Gera um diretório único para clonar, mesmo se o nome se repetir.
        clone_dir = get_unique_clone_dir(base_clone_dir, repo_name)
        print(f"Clonando {repo_name} em {clone_dir}...")
        try:
            clone_repository(repo_url, clone_dir)
            return (repo_name, "Sucesso")
        except Exception as e:
            return (repo_name, f"Erro: {e}")

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(clone_task, repo) for repo in repos_to_clone]
        for future in concurrent.futures.as_completed(futures):
            repo_name, status = future.result()
            print(f"Resultado de {repo_name}: {status}")
            results.append((repo_name, status))
    return results