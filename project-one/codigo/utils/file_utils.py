import os
from .constants import JSON_FILENAME, CSV_FILENAME

script_dir = os.path.dirname(os.path.abspath(__file__))
documentacao_dir = os.path.join(script_dir, "..", "..", "documentacao")

def delete_old_files():
    """Exclui os arquivos JSON e CSV se existirem antes de gerar novos."""
    for filename in [JSON_FILENAME, CSV_FILENAME]:
        file_path = os.path.join(documentacao_dir, filename)

        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Arquivo deletado: {file_path}")
        else:
            print(f"Arquivo não encontrado: {file_path}")
