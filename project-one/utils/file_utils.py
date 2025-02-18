import os
from .constants import JSON_FILENAME, CSV_FILENAME

def delete_old_files():
    """Exclui os arquivos JSON e CSV se existirem antes de gerar novos."""
    for filename in [JSON_FILENAME, CSV_FILENAME]:
        if os.path.exists(filename):
            os.remove(filename)
            print(f"Arquivo deletado: {filename}")
        else:
            print(f"Arquivo não encontrado: {filename}")
