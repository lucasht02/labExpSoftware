import pandas as pd
import matplotlib.pyplot as plt

def generate_graphs():

    df = pd.read_csv("repositorios.csv")

    #RQ 1
    plt.figure(figsize=(10, 6))
    plt.hist(df['Idade do Repositório (dias)'], bins=30, edgecolor='black')
    plt.title('Distribuição da Idade dos Repositórios')
    plt.xlabel('Idade (dias)')
    plt.ylabel('Número de Repositórios')


    #RQ 2
    plt.figure(figsize=(10, 6))
    plt.hist(df['Total PRs Mesclados'], bins=30, edgecolor='black')
    plt.title('Distribuição dos Pull Requests Aceitos')
    plt.xlabel('Total de Pull Requests Aceitos')
    plt.ylabel('Número de Repositórios')

    #RQ 3
    plt.figure(figsize=(10, 6))
    plt.hist(df['Total de Releases'], bins=30, edgecolor='black')
    plt.title('Distribuição dos Releases')
    plt.xlabel('Total de Releases')
    plt.ylabel('Número de Repositórios')

    #RQ 4
    plt.figure(figsize=(10, 6))
    plt.hist(df['Tempo desde última atualização (dias)'], bins=30, edgecolor='black')
    plt.title('Tempo desde a Última Atualização')
    plt.xlabel('Dias')
    plt.ylabel('Número de Repositórios')

    #RQ 5
    language_counts = df['Linguagem Principal'].value_counts()

    plt.figure(figsize=(12, 7))
    plt.bar(language_counts.index, language_counts.values, color='blue')
    plt.title('Contagem por Linguagem Primária')
    plt.xlabel('Linguagem')
    plt.ylabel('Número de Repositórios')
    plt.xticks(rotation=90)
    plt.tight_layout()

    #RQ 6
    avg_pr_by_language = df.groupby('Linguagem Principal')['Total PRs Mesclados'].mean()

    plt.figure(figsize=(12, 7))
    plt.bar(avg_pr_by_language.index, avg_pr_by_language.values, color='green')
    plt.title('Média de Pull Requests Aceitos por Linguagem')
    plt.xlabel('Linguagem')
    plt.ylabel('Média de Pull Requests Aceitos')
    plt.xticks(rotation=90)


    plt.tight_layout()
    plt.show()