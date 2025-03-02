from github_api import fetch_repositories
from json_writer import save_json
from csv_writer import save_to_csv
from utils.file_utils import delete_old_files
from graphs import generate_graphs
from analyze_repositories import analyze_repositories


def main():
    print("Limpando arquivos antigos...")
    delete_old_files()

    print("Buscando repositórios...")
    repositories = fetch_repositories()

    print("Salvando JSON...")
    save_json(repositories)

    print("Salvando CSV...")
    save_to_csv(repositories)

    print("Processo concluído!")

    generate_graphs()

    analyze_repositories()

if __name__ == "__main__":
    main()
