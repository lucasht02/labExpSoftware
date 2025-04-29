import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr


df = pd.read_csv('../../data/prs_analise.csv')

df['total_changes'] = df['linhas_add'] + df['linhas_rem']

df['status'] = df['status'].str.lower()  # espera 'merged' e 'closed'

labels_A = {
    'arquivos':      'Número de arquivos (RQ01)',
    'total_changes': 'Total de linhas alteradas (RQ01)',
    'tempo_h':       'Tempo de análise em horas (RQ02)',
    'descricao_len': 'Tamanho da descrição em caracteres (RQ03)',
    'comentarios':   'Número de comentários (RQ04)',
    'participantes': 'Número de participantes (RQ04)'
}

# Seção A
for col, title in labels_A.items():
    med = df.groupby('status')[col].median().reindex(['merged','closed'])
    plt.figure(figsize=(6,4))
    bars = med.plot.bar(color=['#4C72B0','#55A868'])
    plt.title(f'Mediana de {title} por Status')
    plt.xlabel('Status do PR')
    plt.ylabel(f'Mediana de {title}')
    for p in bars.patches:
        bars.annotate(f'{p.get_height():.1f}',
                      (p.get_x()+p.get_width()/2, p.get_height()),
                      ha='center', va='bottom')
    plt.tight_layout()
    plt.show()

# Seção B
metrics_B = {
    'arquivos':      'Número de arquivos (RQ05)',
    'total_changes': 'Total de linhas alteradas (RQ05)',
    'tempo_h':       'Tempo de análise em horas (RQ06)',
    'descricao_len': 'Tamanho da descrição em caracteres (RQ07)',
    'comentarios':   'Número de comentários (RQ08)',
    'participantes': 'Número de participantes (RQ08)'
}

for col, title in metrics_B.items():
    x = df[col]
    y = df['reviews']

    rho, pval = spearmanr(x, y, nan_policy='omit')

    m, b = np.polyfit(x, y, 1)
    xx = np.linspace(x.min(), x.max(), 100)
    
    plt.figure(figsize=(6,6))
    plt.scatter(x, y, alpha=0.6)
    plt.plot(xx, m*xx + b, '--', linewidth=2)
    plt.title(f'{title} vs Número de Revisões\nSpearman ρ={rho:.2f} (p={pval:.3f})')
    plt.xlabel(title)
    plt.ylabel('Número de revisões')
    plt.tight_layout()
    plt.show()
