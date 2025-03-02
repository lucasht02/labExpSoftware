import pandas as pd
from tabulate import tabulate


def rename_statistics(df):
    """Renomeia os rótulos das estatísticas para melhor interpretação e formata os números."""
    df = df.rename(index={
        "count": "Total de Repositórios",
        "mean": "Média",
        "std": "Desvio Padrão",
        "min": "Valor Mínimo",
        "25%": "1º Quartil (25%)",
        "50%": "Mediana (50%)",
        "75%": "3º Quartil (75%)",
        "max": "Valor Máximo"
    })

    # Formatar os números: inteiros sem casas decimais, decimais com 2 casas
    df = df.applymap(lambda x: f"{x:.2f}" if isinstance(x, float) else int(x) if isinstance(x, (
            int, float)) and x.is_integer() else x)

    return df


def generate_explanations(statistics, rq_description):
    """Gera explicações automáticas para as estatísticas descritivas."""
    explanations = {
        "Total de Repositórios": f"Foram analisados {int(statistics['count'])} repositórios.",
        "Média": f"Em média, cada repositório tem {statistics['mean']:.2f} {rq_description}.",
        "Desvio Padrão": f"Indica alta variação entre os repositórios; alguns têm muitos {rq_description}, outros poucos.",
        "Valor Mínimo": f"O repositório com menor {rq_description} tem {int(statistics['min'])}.",
        "1º Quartil (25%)": f"25% dos repositórios possuem menos de {int(statistics['25%'])} {rq_description}.",
        "Mediana (50%)": f"Metade dos repositórios tem menos de {int(statistics['50%'])} {rq_description}, a outra metade tem mais.",
        "3º Quartil (75%)": f"25% dos repositórios mais populares têm mais de {int(statistics['75%'])} {rq_description}.",
        "Valor Máximo": f"O repositório mais ativo tem {int(statistics['max'])} {rq_description}."
    }

    return pd.DataFrame(list(explanations.items()), columns=["Estatística", "Significado"])


def analyze_repositories(csv_file="repositorios.csv", output_file="estatisticas.md"):
    """Analisa as estatísticas dos repositórios e gera um relatório com explicações automáticas."""
    df = pd.read_csv(csv_file)

    # Criar a métrica "Razão Issues Fechadas (%)"
    df["Razão Issues Fechadas (%)"] = (df["Total de Issues Fechadas"] / df["Total de Issues"]) * 100
    df_filtrado = df[df["Total de Issues"] > 0]  # Evita divisão por zero

    # Análises Estatísticas para cada RQ
    rq_data = {
        "RQ 01: Sistemas populares são maduros/antigos?": ("Idade do Repositório (dias)", "dias de existência"),
        "RQ 02: Sistemas populares recebem muita contribuição externa?": ("Total PRs Mesclados", "PRs mesclados"),
        "RQ 03: Sistemas populares lançam releases com frequência?": ("Total de Releases", "releases"),
        "RQ 04: Sistemas populares são atualizados com frequência?": ("Tempo desde última atualização (dias)", "dias desde a última atualização"),
    }

    # Criar relatório Markdown
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Relatório de Estatísticas dos Repositórios\n\n")

        for rq, (coluna, descricao) in rq_data.items():
            estatisticas = rename_statistics(df[coluna].describe().to_frame())
            explicacoes = generate_explanations(df[coluna].describe(), descricao)

            f.write(f"## {rq}\n")
            f.write(tabulate(estatisticas, headers="keys", tablefmt="github"))
            f.write("\n\n**Explicação:**\n\n")
            f.write(tabulate(explicacoes, headers="keys", tablefmt="github"))
            f.write("\n\n")

        # RQ 05: Sistemas populares são escritos nas linguagens mais populares?
        f.write("## RQ 05: Sistemas populares são escritos nas linguagens mais populares?\n")
        linguagens = df['Linguagem Principal'].value_counts().reset_index()
        linguagens.columns = ["Linguagem", "Número de Repositórios"]
        f.write(tabulate(linguagens, headers="keys", tablefmt="github"))
        f.write("\n\n")

        # RQ 06: Sistemas populares possuem um alto percentual de Issues Fechadas?
        f.write("## RQ 06: Sistemas Populares possuem um alto percentual de Issues Fechadas?\n")
        media_issues_fechadas = df_filtrado["Razão Issues Fechadas (%)"].mean()
        comparacao_issues = pd.DataFrame({
            "Métrica": ["Média de Issues Fechadas (%)"],
            "Valor": [round(media_issues_fechadas, 2)]
        })
        f.write(tabulate(comparacao_issues, headers="keys", tablefmt="github"))
        f.write("\n")

    # Exibir os resultados no terminal
    print("\n===== Relatório gerado com sucesso: estatisticas.md =====\n")
