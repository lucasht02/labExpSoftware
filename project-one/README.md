# Laboratório 1

Este projeto tem como objetivo realizar consultas à API GraphQL do GitHub para buscar informações detalhadas de 1000 repositórios populares. As informações coletadas servirão para responder a um conjunto de questões de pesquisa (RQs) relacionadas a características dos repositórios buscados.

## 🌟 Funcionalidades

- Realiza consultas GraphQL para buscar informações de repositórios do GitHub.
- Salva os dados obtidos em formato JSON e CSV.
- Automatiza o processo de requisição para múltiplas páginas de resultados.
- Utiliza variáveis de ambiente para autenticação segura.

## 📜 Índice

1. [Sobre o Projeto](#sobre-o-projeto)
2. [Ferramentas Utilizadas](#ferramentas-utilizadas)
3. [Como Executar o Projeto](#como-executar-o-projeto)
4. [Estrutura do Projeto](#estrutura-do-projeto)
5. [Exemplo de Saída](#exemplo-de-saída)
6. [Referências](#referências)

## 📝 Sobre o Projeto

O propósito deste projeto é realizar consultas GraphQL para obter dados e métricas de 1000 repositórios populares do GitHub, com o objetivo de responder às seguintes questões de pesquisa (RQs):

- **RQ 01**: Sistemas populares são maduros/antigos?
  - **Métrica**: Idade do repositório (calculado a partir da data de sua criação).
- **RQ 02**: Sistemas populares recebem muita contribuição externa?
  - **Métrica**: Total de pull requests aceitas.
- **RQ 03**: Sistemas populares lançam releases com frequência?
  - **Métrica**: Total de releases.
- **RQ 04**: Sistemas populares são atualizados com frequência?
  - **Métrica**: Tempo até a última atualização (calculado a partir da data de última atualização).
- **RQ 05**: Sistemas populares são escritos nas linguagens mais populares?
  - **Métrica**: Linguagem primária de cada um desses repositórios.
- **RQ 06**: Sistemas populares possuem um alto percentual de issues fechadas?
  - **Métrica**: Razão entre número de issues fechadas pelo total de issues.

## 🛠 Ferramentas Utilizadas

- **Python 3.13**: Linguagem de programação principal.
- **Requests**: Biblioteca para fazer requisições HTTP.
- **CSV**: Biblioteca para geração de planilhas.
- **JSON**: Para salvar dados estruturados.
- **dotenv**: Gerenciar variáveis de ambiente.
- **GitHub GraphQL API**: Para consultas avançadas de repositórios.

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
3. **Executar o `Script` principal**:
    ```bash
    python main.py
    ```

## 🏗 Estrutura do Projeto

- `main.py`: Script principal que executa o processo de busca e salvamento.
- `github_api.py`: Realiza as consultas GraphQL e faz chamadas a API do GitHub.
- `csv_writer.py`: Gera o arquivo CSV com as informações dos repositórios.
- `json_writer.py`: Gera o JSON com as informações dos repositórios.
- `config.py`: Configurações de URL e autenticação.
- `query.graphql`: Arquivo com a query GraphQL utilizada para as consultas.
- `requirements.txt`: Lista de dependências do projeto.

## 📊 Exemplo de Saída

Após a execução, os seguintes arquivos serão gerados:

- `repositorios.json`: Contém as informações completas dos repositórios em formato JSON.
- `repositorios.csv`: Contém uma planilha com os dados estruturados, incluindo:
  - Nome do repositório
  - Descrição
  - URL
  - Data de criação e última atualização
  - Linguagem principal
  - Total de PRs mesclados
  - Total de releases
  - Total de issues e issues fechadas

## Autores

- Lucas Cabral Soares
- Lucas Hemétrio
- Maria Eduarda Amaral Muniz



