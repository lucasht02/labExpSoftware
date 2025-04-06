# Laboratório 2

Este projeto tem como objetivo realizar consultas à API GraphQL do GitHub para buscar informações detalhadas de 1000 repositórios java populares. As informações coletadas servirão para responder a um conjunto de questões de pesquisa (RQs) relacionadas a características dos repositórios buscados.

## 🌟 Funcionalidades

- Coleta automática dos 1.000 repositórios Java mais populares do GitHub via GraphQL.

- Clonagem automatizada dos repositórios selecionados.

- Extração de métricas de qualidade de código via CK (Coupling between Objects, DIT, LCOM, LOC, Comentários).

- Armazenamento das informações coletadas em formato CSV para análise posterior.

- Visualização e análise estatística dos resultados.

## 📜 Índice

1. [Sobre o Projeto](#sobre-o-projeto)
2. [Ferramentas Utilizadas](#ferramentas-utilizadas)
3. [Como Executar o Projeto](#como-executar-o-projeto)
4. [Estrutura do Projeto](#estrutura-do-projeto)
5. [Exemplo de Saída](#exemplo-de-saída)
6. [Referências](#referências)

## 📝 Sobre o Projeto

O objetivo é realizar consultas GraphQL para obter métricas de qualidade de código dos 1.000 repositórios Java mais populares do GitHub, correlacionando essas métricas com características do seu processo de desenvolvimento. O projeto busca responder às seguintes questões de pesquisa (RQs):

- **RQ 01**: Qual a relação entre a popularidade dos repositórios e suas características de qualidade?
- **RQ 02**: Qual a relação entre a maturidade dos repositórios e suas características de qualidade?
- **RQ 03**: Qual a relação entre a atividade dos repositórios e suas características de qualidade?
- **RQ 04**: Qual a relação entre o tamanho dos repositórios e suas características de qualidade?

## 🛠 Ferramentas Utilizadas

- **Python 3.13**: Linguagem de programação principal.
- **Requests**: Biblioteca para fazer requisições HTTP.
- **CSV**: Biblioteca para geração de planilhas.
- **JSON**: Para salvar dados estruturados.
- **dotenv**: Gerenciar variáveis de ambiente.
- **GitHub GraphQL API**: Para consultas avançadas de repositórios.
- **Pandas**: Para manipulação e análise de dados.
- **CK**: Ferramenta de análise estática para extração de métricas de qualidade do código.

## 🚀 Como Executar o Projeto

1. **Instalar Dependências**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Configurar variáveis de ambiente**:
    - Criar um arquivo `.env` com sua chave de API do GitHub:

    ```bash
    API_KEY=seu_token_github
    ```
    ```bash
    CK_PATH=caminho_do_arquivo_jar_do_CK
    ```
3. **Executar o `Script` principal**:
    ```bash
    python main.py
    ```

## 🏗 Estrutura do Projeto

- `main.py`: Script principal que executa o processo de busca e salvamento.
- `github_api.py`: Realiza as consultas GraphQL e faz chamadas a API do GitHub.
- `csv_writer.py`: Gera o arquivo CSV com as informações dos repositórios.
- `clone_repositories.py`: Clona os repositórios selecionados.
- `config.py`: Configurações de URL e autenticação.
- `query.graphql`: Arquivo com a query GraphQL utilizada para as consultas.
- `ck_analyzer`: Executa o CK e coleta métricas de qualidade do código.
- `requirements.txt`: Lista de dependências do projeto.

## 📊 Exemplo de Saída

Após a execução, os seguintes arquivos serão gerados:

- `todos_repositorios.csv`: Contém as informações de todos os 1000 repositórios.
- `metricas_repositorio_clonado.csv`: Contém uma planilha com os dados estruturados, incluindo:
  - Nome do repositório
  - Descrição
  - URL
  - Data de criação e última atualização
  - Linguagem principal
  - Total de releases
  - CBO (Coupling Between Objects)
  - DIT (Depth Inheritance Tree)
  - LCOM (Lack of Cohesion of Methods)
  - LOC (Linhas de Código)
  - Linhas de Comentário

## Autores

- Lucas Cabral Soares
- Lucas Hemétrio
- Maria Eduarda Amaral Muniz



