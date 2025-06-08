
# 1. Introdução

A crescente adoção de APIs na arquitetura de sistemas modernos exige decisões criteriosas quanto ao modelo de comunicação utilizado. Dentre as abordagens predominantes, destaca-se o REST (Representational State Transfer), amplamente difundido por sua simplicidade e aderência ao protocolo HTTP. Contudo, alternativas mais recentes, como o GraphQL, têm ganhado espaço por oferecer maior flexibilidade nas consultas e reduzir o *overfetching* e *underfetching* de dados.

GraphQL, desenvolvido pelo Facebook, permite que os clientes especifiquem exatamente quais dados desejam receber, potencialmente otimizando o desempenho da aplicação. Em contrapartida, REST expõe múltiplos endpoints fixos, o que pode resultar em múltiplas requisições ou carregamento de dados desnecessários. Apesar das promessas de eficiência, os benefícios práticos do GraphQL em relação ao REST ainda carecem de validação empírica, especialmente sob condições controladas e reprodutíveis.

Este trabalho propõe a realização de um experimento controlado com o objetivo de responder às seguintes perguntas de pesquisa:

- **RQ1:** Respostas às consultas GraphQL são mais rápidas que respostas às consultas REST?
- **RQ2:** Respostas às consultas GraphQL têm tamanho menor que respostas às consultas REST?

A fim de obter evidências quantitativas, serão analisadas métricas como tempo de resposta e tamanho da resposta em diferentes tipos de API construídas sobre a mesma base de dados. O presente relatório apresenta, nas seções a seguir, o desenho experimental adotado, bem como os procedimentos de preparação, execução e análise estatística dos resultados.

# 2. Desenho do Experimento

## 2.1 Formulação das Hipóteses

Com base nas perguntas de pesquisa apresentadas, as hipóteses estatísticas foram formuladas da seguinte forma:

**Hipóteses para RQ1 (tempo de resposta):**

- **H₀ (Hipótese Nula):** Não há diferença significativa no tempo médio de resposta entre APIs REST e APIs GraphQL.
- **H₁ (Hipótese Alternativa):** APIs GraphQL apresentam tempo médio de resposta inferior ao das APIs REST.

**Hipóteses para RQ2 (tamanho da resposta):**

- **H₀₂:** Não há diferença significativa no tamanho médio das respostas entre APIs REST e GraphQL.
- **H₁₂:** As respostas de APIs GraphQL possuem tamanho médio inferior ao das respostas REST.

## 2.2 Variáveis do Experimento

**Variáveis Independentes:**

- Tipo de API utilizada (REST ou GraphQL).

**Variáveis Dependentes:**

- Tempo de resposta (em milissegundos).
- Tamanho da resposta (em bytes).

## 2.3 Tratamentos

O experimento contará com dois tratamentos distintos, aplicados sobre a API pública do GitHub, que oferece suporte tanto ao modelo REST quanto ao modelo GraphQL.

- **Tratamento A – REST:** Utilização da [GitHub REST API v3](https://docs.github.com/en/rest), onde cada recurso (usuários, repositórios, issues, etc.) é acessado por meio de endpoints separados, como `GET /users/{username}` ou `GET /repos/{owner}/{repo}/issues`.

- **Tratamento B – GraphQL:** Utilização da [GitHub GraphQL API v4](https://docs.github.com/en/graphql), na qual uma única chamada pode buscar múltiplas entidades e atributos em uma estrutura personalizada, reduzindo o número de requisições e a quantidade de dados retornados.

As duas interfaces expõem essencialmente os mesmos dados e funcionalidades, mas diferem na forma como as consultas são realizadas e estruturadas.

## 2.4 Objetos Experimentais

Os objetos experimentais consistem em **consultas reais sobre repositórios públicos no GitHub**, realizadas tanto pela API REST quanto pela API GraphQL. A escolha pelo GitHub justifica-se por sua relevância no ecossistema de desenvolvimento de software e pela disponibilidade pública e gratuita de acesso às suas APIs.

Foram definidas três categorias principais de consulta:

- **Consulta de usuário:** buscar nome, bio, localização e seguidores de um usuário.
- **Consulta de repositório:** buscar nome, descrição, número de estrelas, forks e linguagem principal.
- **Consulta de issues:** listar as últimas 10 issues de um repositório com título e estado.

**Exemplo de equivalência entre REST e GraphQL:**

REST:
```
GET /users/octocat  
GET /repos/octocat/Hello-World  
GET /repos/octocat/Hello-World/issues  
```

GraphQL:
```graphql
{
  user(login: "octocat") {
    name
    bio
    location
    followers {
      totalCount
    }
  }
  repository(owner: "octocat", name: "Hello-World") {
    name
    description
    stargazerCount
    forkCount
    primaryLanguage {
      name
    }
    issues(first: 10) {
      nodes {
        title
        state
      }
    }
  }
}
```

As consultas foram cuidadosamente definidas para refletir operações comuns em aplicações que consomem dados do GitHub, garantindo paridade entre os dois modelos e mantendo o foco na análise das métricas de tempo de resposta e tamanho da resposta.

## 2.5 Tipo de Projeto Experimental

Trata-se de um **experimento controlado com medidas repetidas**, permitindo que cada tratamento (REST ou GraphQL) seja avaliado múltiplas vezes sob as mesmas condições. Essa abordagem possibilita uma análise comparativa direta entre os dois modelos.

## 2.6 Quantidade de Medições

Serão executadas **30 requisições para cada tipo de consulta** em ambas as APIs, totalizando 60 medições por métrica (tempo e tamanho da resposta). As medições serão feitas por scripts automatizados em Python, utilizando a biblioteca `requests` para simular os acessos e registrar os resultados.

## 2.7 Ameaças à Validade

Foram identificadas as seguintes ameaças à validade do experimento:

- **Validade Interna:** Diferenças na lógica de implementação entre as APIs podem enviesar os resultados.  
  *Mitigação:* reutilização de componentes de backend e banco de dados em ambas as abordagens.

- **Validade Externa:** Os resultados obtidos em ambiente controlado podem não refletir contextos reais em produção.  
  *Mitigação:* simulação de cargas realistas.

- **Validade de Construção:** Ferramentas de medição podem introduzir imprecisões.  
  *Mitigação:* uso de medições repetidas e ferramentas precisas.

- **Validade Estatística:** Tamanho da amostra pode não ser suficiente para detectar pequenas diferenças.  
  *Mitigação:* aplicação de testes estatísticos apropriados como o *t de Student* para amostras emparelhadas.

# 3. Preparação do Experimento

Com o desenho experimental definido, esta etapa tem como objetivo estruturar o ambiente necessário para a aplicação dos tratamentos REST e GraphQL sobre a API pública do GitHub. A preparação abrange desde a definição das consultas até o desenvolvimento dos scripts de automação responsáveis pela coleta dos dados.

## 3.1 Seleção e Estruturação das Consultas

Foram definidas três categorias de consultas equivalentes para REST e GraphQL:

1. **Consulta de usuário:** obtém nome, bio, localização e número de seguidores de um usuário.
2. **Consulta de repositório:** retorna nome, descrição, número de estrelas, forks e linguagem principal.
3. **Consulta de issues:** recupera as 10 issues mais recentes de um repositório com seus respectivos títulos e estados.

As consultas foram definidas com base na documentação oficial das APIs:

- [GitHub REST API v3](https://docs.github.com/en/rest)
- [GitHub GraphQL API v4](https://docs.github.com/en/graphql)

Essa equivalência garante isonomia nos dados retornados, permitindo que as diferenças observadas estejam associadas ao modelo de API e não à natureza da consulta.

## 3.2 Ambiente de Execução

As medições foram realizadas em ambiente local com as seguintes especificações:

- **Sistema Operacional:** Ubuntu 22.04 LTS
- **Processador:** Intel Core i5, 2.5GHz
- **Memória RAM:** 8GB
- **Python:** versão 3.10
- **Bibliotecas:** `requests`, `time`, `json`, `pandas`, `dotenv`

A execução foi feita em uma rede estável e sem interferência de proxy, VPN ou firewall, garantindo consistência nas medições. A autenticação foi realizada por meio de tokens pessoais (PATs), exigidos pela API do GitHub, com permissão de acesso apenas a dados públicos.

## 3.3 Scripts de Medição

Foi desenvolvido um script Python genérico que realiza o seguinte fluxo:

1. Carrega os parâmetros de autenticação via variável de ambiente.
2. Realiza 30 requisições para cada tipo de consulta, alternando entre REST e GraphQL.
3. Para cada requisição, registra:
   - Tempo total de resposta (em milissegundos)
   - Tamanho da resposta (em bytes)
   - Timestamp e tipo da API
4. Salva os dados em arquivos `.csv` separados por abordagem (REST e GraphQL)

Trechos do script:

```python
# REST
start = time.time()
response = requests.get(rest_url, headers=headers)
elapsed_time = (time.time() - start) * 1000  # em ms
size = len(response.content)

# GraphQL
query = { "query": "{ ... }" }
start = time.time()
response = requests.post(graphql_url, json=query, headers=headers)
elapsed_time = (time.time() - start) * 1000
size = len(response.content)
```

O espaçamento entre requisições foi de 1 segundo, visando evitar bloqueio por *rate limiting* e reduzir viés por aquecimento de cache.

## 3.4 Persistência dos Resultados

Todos os dados coletados foram armazenados em arquivos `CSV` com os seguintes campos:

- `api_type` (REST ou GraphQL)
- `query_type` (user, repo, issues)
- `response_time_ms`
- `response_size_bytes`
- `timestamp`

Esses dados serão posteriormente analisados com auxílio da biblioteca `pandas` e visualizados com `seaborn` ou `matplotlib`.

## 3.5 Reprodutibilidade

O projeto foi versionado em repositório Git contendo:

- Scripts Python de coleta
- Arquivo `.env.example` com estrutura de token
- Documentação do experimento
- Resultados parciais em `.csv`

Com isso, qualquer desenvolvedor pode replicar o experimento executando os scripts em um ambiente controlado com seu próprio token de acesso.
