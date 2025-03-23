import pandas as pd
import matplotlib.pyplot as plt
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(script_dir, "..", "documentacao", "metricas_repositorio_clonado.csv")
df = pd.read_csv(csv_file_path)

def plot_metric_vs_independent(df, independent_var, metric_prefix, xlabel, title):
    # Define os nomes das colunas de interesse
    col_media   = f"{metric_prefix} Média"
    col_mediana = f"{metric_prefix} Mediana"
    col_desvio  = f"{metric_prefix} Desvio Padrão"
    
    # Converte a variável independente e as métricas para numérico
    x = pd.to_numeric(df[independent_var], errors='coerce')
    y_media = pd.to_numeric(df[col_media], errors='coerce')
    y_mediana = pd.to_numeric(df[col_mediana], errors='coerce')
    y_desvio = pd.to_numeric(df[col_desvio], errors='coerce')
    
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y_media, label=f"{metric_prefix} Média", marker='o')
    plt.scatter(x, y_mediana, label=f"{metric_prefix} Mediana", marker='s')
    plt.scatter(x, y_desvio, label=f"{metric_prefix} Desvio Padrão", marker='^')
    
    plt.xlabel(xlabel)
    plt.ylabel(metric_prefix)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    
    

def graphs():
    # RQ 01 - Popularidade
    indep_pop = "Número de Estrelas (Popularidade)"
    plot_metric_vs_independent(df, indep_pop, "CBO", indep_pop, "CBO vs Popularidade")
    plot_metric_vs_independent(df, indep_pop, "DIT", indep_pop, "DIT vs Popularidade")
    plot_metric_vs_independent(df, indep_pop, "LCOM", indep_pop, "LCOM vs Popularidade")

    # RQ 02 - Maturidade (convertendo idade de dias para anos)
    df["Idade (anos)"] = pd.to_numeric(df["Idade do Repositório (dias)"], errors='coerce') / 365.0
    indep_mat = "Idade (anos)"
    plot_metric_vs_independent(df, indep_mat, "CBO", indep_mat, "CBO vs Maturidade")
    plot_metric_vs_independent(df, indep_mat, "DIT", indep_mat, "DIT vs Maturidade")
    plot_metric_vs_independent(df, indep_mat, "LCOM", indep_mat, "LCOM vs Maturidade")

    # RQ 03 - Atividade
    indep_ati = "Número de Releases (Atividade)"
    plot_metric_vs_independent(df, indep_ati, "CBO", indep_ati, "CBO vs Atividade")
    plot_metric_vs_independent(df, indep_ati, "DIT", indep_ati, "DIT vs Atividade")
    plot_metric_vs_independent(df, indep_ati, "LCOM", indep_ati, "LCOM vs Atividade")

    # RQ 04 - Tamanho
    indep_tam = "Linhas de Código (Tamanho)"
    plot_metric_vs_independent(df, indep_tam, "CBO", indep_tam, "CBO vs Tamanho")
    plot_metric_vs_independent(df, indep_tam, "DIT", indep_tam, "DIT vs Tamanho")
    plot_metric_vs_independent(df, indep_tam, "LCOM", indep_tam, "LCOM vs Tamanho")

    plt.show()