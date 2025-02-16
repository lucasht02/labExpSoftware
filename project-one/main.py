from github_api import fetch_repositories
from json_writer import save_json
from csv_writer import save_to_csv

def main():
    print("Buscando repositórios...")
    repositories = fetch_repositories()

    print("Salvando JSON...")
    save_json(repositories)

    print("Salvando CSV...")
    save_to_csv(repositories)

    print("Processo concluído!")

if __name__ == "__main__":
    main()
