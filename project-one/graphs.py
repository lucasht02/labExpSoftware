import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def generate_graphs():
    df = pd.read_csv("repositorios.csv")

    # RQ 1: Idade dos Repositórios
    plt.figure(figsize=(10, 6))
    plt.hist(df['Idade do Repositório (dias)'], bins=30, edgecolor='black', alpha=0.7, color='dodgerblue')
    plt.axvline(df['Idade do Repositório (dias)'].mean(), color='red', linestyle='dashed', linewidth=2, label='Média')
    plt.axvline(df['Idade do Repositório (dias)'].median(), color='green', linestyle='dashed', linewidth=2, label='Mediana')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.title('Distribuição da Idade dos Repositórios')
    plt.xlabel('Idade (dias)')
    plt.ylabel('Número de Repositórios')
    plt.legend()

    # RQ 2: Total de Pull Requests Aceitos
    plt.figure(figsize=(10, 6))
    plt.hist(df['Total PRs Mesclados'], bins=30, edgecolor='black', alpha=0.7, color='orange')
    plt.axvline(df['Total PRs Mesclados'].mean(), color='red', linestyle='dashed', linewidth=2, label='Média')
    plt.axvline(df['Total PRs Mesclados'].median(), color='green', linestyle='dashed', linewidth=2, label='Mediana')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.title('Distribuição dos Pull Requests Aceitos')
    plt.xlabel('Total de Pull Requests Aceitos')
    plt.ylabel('Número de Repositórios')
    plt.legend()

    # RQ 3: Total de Releases
    plt.figure(figsize=(10, 6))
    plt.hist(df['Total de Releases'], bins=30, edgecolor='black', alpha=0.7, color='seagreen')
    plt.axvline(df['Total de Releases'].mean(), color='red', linestyle='dashed', linewidth=2, label='Média')
    plt.axvline(df['Total de Releases'].median(), color='green', linestyle='dashed', linewidth=2, label='Mediana')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.title('Distribuição dos Releases')
    plt.xlabel('Total de Releases')
    plt.ylabel('Número de Repositórios')
    plt.legend()

    # RQ 4: Tempo desde a Última Atualização
    plt.figure(figsize=(10, 6))
    plt.hist(df['Tempo desde última atualização (dias)'], bins=30, edgecolor='black', alpha=0.7, color='purple')
    plt.axvline(df['Tempo desde última atualização (dias)'].mean(), color='red', linestyle='dashed', linewidth=2, label='Média')
    plt.axvline(df['Tempo desde última atualização (dias)'].median(), color='green', linestyle='dashed', linewidth=2, label='Mediana')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.title('Tempo desde a Última Atualização')
    plt.xlabel('Dias')
    plt.ylabel('Número de Repositórios')
    plt.legend()

    # RQ 5: Contagem de Repositórios por Linguagem Principal
    language_counts = df['Linguagem Principal'].value_counts()

    plt.figure(figsize=(12, 7))
    bars = plt.bar(language_counts.index, language_counts.values, color='royalblue')
    plt.title('Contagem por Linguagem Primária')
    plt.xlabel('Linguagem')
    plt.ylabel('Número de Repositórios')
    plt.xticks(rotation=90)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Adicionando rótulos nas barras
    for bar in bars:
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{int(bar.get_height())}",
                 ha='center', va='bottom', fontsize=9, color='black')

    plt.tight_layout()

    # RQ 6: Distribuição da Razão de Issues Fechadas
    df = df[df["Total de Issues"] > 0]  # Evita divisão por zero
    df["Razão Issues Fechadas (%)"] = (df["Total de Issues Fechadas"] / df["Total de Issues"]) * 100

    plt.figure(figsize=(10, 6))
    plt.hist(df['Razão Issues Fechadas (%)'], bins=30, edgecolor='black', alpha=0.7, color='darkviolet')
    plt.axvline(df['Razão Issues Fechadas (%)'].mean(), color='red', linestyle='dashed', linewidth=2, label='Média')
    plt.axvline(df['Razão Issues Fechadas (%)'].median(), color='green', linestyle='dashed', linewidth=2, label='Mediana')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.title('Distribuição da Razão de Issues Fechadas')
    plt.xlabel('Razão de Issues Fechadas (%)')
    plt.ylabel('Número de Repositórios')
    plt.legend()

    plt.tight_layout()
    plt.show()
