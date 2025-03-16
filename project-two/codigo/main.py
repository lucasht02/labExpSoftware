from github_api import fetch_repositories
from clone_repositories import clone_repositories
from csv_writer import save_all_repositories_to_csv, save_cloned_repositories_metrics_to_csv
from utils.file_utils import delete_old_files

def main():
    print("Limpando arquivos antigos...")
    delete_old_files()

    print("Buscando repositórios...")
    repositories = fetch_repositories()

    print("Salvando todos os repositórios no CSV...")
    save_all_repositories_to_csv(repositories)

    print("Clonando repositórios...")
    clone_repositories(repositories, num_repos_to_clone=1)

    print("Salvando métricas dos repositórios clonados...")
    save_cloned_repositories_metrics_to_csv(repositories)

    print("Processo concluído!")

if __name__ == "__main__":
    main()