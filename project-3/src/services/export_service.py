import csv
import os

def exportar_prs_para_csv(prs, filename="data/pull_requests.csv", append=False):
    os.makedirs("data", exist_ok=True)
    mode = "a" if append else "w"
    write_header = not os.path.exists(filename) or not append

    with open(filename, mode=mode, newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=prs[0].keys())
        if write_header:
            writer.writeheader()
        writer.writerows(prs)

    print(f"✅ {len(prs)} PRs adicionados em {filename}")

