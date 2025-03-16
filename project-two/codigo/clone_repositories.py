import git
import os
import random


def clone_repository(repo_url, clone_dir):
    """Clona o repositório no diretório especificado"""
    if not os.path.exists(clone_dir):
        os.makedirs(clone_dir)
    git.Repo.clone_from(repo_url, clone_dir)


def clone_repositories(repos, num_repos_to_clone=1):
    """Clona até 'num_repos_to_clone' repositórios diferentes da lista fornecida"""

    if not repos:
        print("Nenhum repositório encontrado.")
        return

    repos_to_clone = random.sample(repos, min(num_repos_to_clone, len(repos)))

    print("\nLista de repositórios escolhidos para clonagem:")
    for repo in repos_to_clone:
        print(f"- {repo['name']} ({repo['url']})")

    print("\nIniciando clonagem...\n")

    for repo in repos_to_clone:
        repo_name = repo['name']
        repo_url = repo['url']
        clone_dir = f'./repos/{repo_name}'

        print(f"Clonando {repo_name}...")
        clone_repository(repo_url, clone_dir)
