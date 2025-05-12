## 1. Pré-requisitos e Instalação

### Python e Faker

*   **Python:** Certifique-se de ter o Python 3.7 ou superior instalado. Você pode baixá-lo em [python.org](https://www.python.org/downloads/).
*   **Faker:** Esta biblioteca é usada para gerar dados fictícios. Instale-a usando pip:
    ```bash
    pip install Faker
    ```

### Neo4j Desktop

*   Baixe e instale o Neo4j Desktop a partir do [site oficial do Neo4j](https://neo4j.com/download/).
*   Siga as instruções de instalação para o seu sistema operacional.

---

## 2. Estrutura do Projeto

O projeto consiste nos seguintes arquivos:

*   `Gerador.py`: Script Python responsável por gerar os dados e os arquivos Cypher.
*   `nodes.cypher`: Arquivo Cypher gerado contendo os comandos para criar os nós, constraints e índices no Neo4j.
*   `relationships.cypher`: Arquivo Cypher gerado contendo os comandos para criar os relacionamentos entre os nós.
*   `queries.cypher`: Arquivo Cypher gerado contendo exemplos de consultas para interagir com os dados no Neo4j.

---

## 3. Modelo de Dados

O modelo de dados define as entidades (nós) e como elas se conectam (relacionamentos) no grafo.

### Nós

*   `Aluno`: Representa um estudante.
    *   Propriedades: `id_aluno` (inteiro, único), `nome_aluno` (string)
*   `Professor`: Representa um docente.
    *   Propriedades: `id_professor` (inteiro, único), `nome_professor` (string)
*   `Disciplina`: Representa uma matéria ou curso.
    *   Propriedades: `codigo_disciplina` (string, único, ex: "DISC001"), `nome_disciplina` (string)
*   `Departamento`: Representa uma unidade administrativa da instituição.
    *   Propriedades: `id_departamento` (inteiro, único), `nome_departamento` (string)
*   `MatrizCurricular`: Representa a estrutura de um curso com suas disciplinas obrigatórias.
    *   Propriedades: `id_matriz` (inteiro, único), `nome_matriz` (string)
*   `TCC`: Representa um Trabalho de Conclusão de Curso.
    *   Propriedades: `id_tcc` (inteiro, único), `titulo_tcc` (string)

### Relacionamentos

*   `(:Aluno)-[:CURSOU {semestre: int, ano: int, nota_final: float}]->(:Disciplina)`
    *   Indica que um aluno cursou uma disciplina, com informações sobre semestre, ano e nota.
*   `(:Professor)-[:MINISTROU {semestre: int, ano: int}]->(:Disciplina)`
    *   Indica que um professor ministrou uma disciplina em um determinado semestre e ano.
*   `(:MatrizCurricular)-[:CONTEM_DISCIPLINA]->(:Disciplina)`
    *   Indica que uma disciplina faz parte de uma matriz curricular.
*   `(:Aluno)-[:FORMADO_EM {semestre_formacao: int, ano_formacao: int}]->(:MatrizCurricular)`
    *   Indica que um aluno concluiu todas as disciplinas de uma matriz curricular e se formou.
*   `(:Professor)-[:CHEFE_DE]->(:Departamento)`
    *   Indica que um professor é o chefe de um departamento.
*   `(:Aluno)-[:PARTICIPA_DE]->(:TCC)`
    *   Indica que um aluno faz parte de um grupo de TCC.
*   `(:Professor)-[:ORIENTA]->(:TCC)`
    *   Indica que um professor orienta um TCC.

---

## 4. Geração dos Dados

Para gerar os arquivos Cypher (`nodes.cypher`, `relationships.cypher`, `queries.cypher`), execute o script Python:

1.  Abra um terminal ou prompt de comando.
2.  Navegue até o diretório onde você salvou o arquivo `Gerador.py`.
3.  Execute o script:
    ```bash
    python Gerador.py
    ```
4.  Após a execução, os três arquivos `.cypher` serão criados no mesmo diretório.

---

## 5. Carregando os Dados no Neo4j Desktop

Siga estes passos para importar os dados gerados para o seu banco de dados Neo4j usando o Neo4j Desktop:

1.  **Abra o Neo4j Desktop.**
2.  **Crie um Novo Projeto (se ainda não tiver um):**
    *   Clique em "New" (Novo) ou no ícone `+` para adicionar um projeto.
    *   Dê um nome ao seu projeto (ex: "DadosAcademicosProjeto") e clique em "Create" (Criar).
3.  **Adicione um Banco de Dados ao Projeto:**
    *   Dentro do seu projeto, clique em "Add" (Adicionar) -> "Local DBMS" (Banco de Dados Local).
    *   Dê um nome para o seu banco de dados (ex: "academic_db").
    *   Defina uma senha para o banco de dados (lembre-se dela!).
    *   Clique em "Create" (Criar).
4.  **Inicie o Banco de Dados:**
    *   Localize o banco de dados que você acabou de criar na lista de DBMSs do seu projeto.
    *   Clique no botão "Start" (Iniciar) ao lado dele. Aguarde até que o status mude para "Active" (Ativo), indicado por um ponto verde.
5.  **Abra o Neo4j Browser:**
    *   Com o banco de dados ativo, clique no botão "Open" (Abrir) ao lado dele. Isso abrirá o Neo4j Browser em seu navegador web padrão.
    *   Você pode ser solicitado a se conectar. O usuário padrão é `neo4j` e a senha é a que você definiu ao criar o DBMS.
6.  **Execute o arquivo `nodes.cypher` (Criação de Nós e Estrutura):**
    *   **Atenção:** O arquivo `nodes.cypher` contém o comando `MATCH (n) DETACH DELETE n;` no início. **Este comando APAGARÁ TODOS OS DADOS existentes no banco de dados selecionado.** Se for um banco de dados de teste, isso é desejável para uma importação limpa. Caso contrário, comente ou remova essa linha do arquivo `nodes.cypher` antes de prosseguir.
    *   Abra o arquivo `nodes.cypher` (gerado pelo script Python) em um editor de texto.
    *   Copie **todo** o conteúdo do arquivo.
    *   No Neo4j Browser, cole o conteúdo copiado na barra de consulta no topo da tela (onde diz "$").
    *   Clique no ícone de "Play" (um triângulo apontando para a direita) ou pressione `Ctrl+Enter` (Windows/Linux) ou `Cmd+Enter` (Mac) para executar os comandos.
    *   Aguarde a conclusão. Você deverá ver uma mensagem indicando o sucesso da operação.
7.  **Execute o arquivo `relationships.cypher` (Criação de Relacionamentos):**
    *   Agora, abra o arquivo `relationships.cypher` em um editor de texto.
    *   Copie **todo** o conteúdo do arquivo.
    *   No Neo4j Browser, substitua o conteúdo anterior na barra de consulta pelo conteúdo do `relationships.cypher`.
    *   Clique no ícone de "Play" ou pressione `Ctrl+Enter` / `Cmd+Enter` para executar os comandos.
    *   Aguarde a conclusão.

Seus dados agora estão carregados no Neo4j!

---

## 6. Executando Consultas (Queries)

O arquivo `queries.cypher` contém exemplos de consultas para explorar os dados. Veja como usá-las:

1.  **Abra o Neo4j Browser** (se ainda não estiver aberto e conectado ao seu banco de dados).
2.  **Abra o arquivo `queries.cypher`** em um editor de texto.
3.  **Copie uma Query:**
    *   Selecione e copie uma das queries do arquivo. Por exemplo, para ver o histórico de um aluno:
      ```cypher
      // 1. Histórico escolar do aluno ID <ID_EXEMPLO>
      MATCH (a:Aluno {id_aluno: <ID_EXEMPLO>})-[r:CURSOU]->(d:Disciplina)
      RETURN d.codigo_disciplina, d.nome_disciplina, r.semestre, r.ano, r.nota_final ORDER BY r.ano, r.semestre;
      ```
      *Nota: O arquivo `queries.cypher` gerado pelo script Python tentará preencher `<ID_EXEMPLO>` com um ID de aluno real dos dados gerados. Você pode usar esse ID ou escolher outro.*
4.  **Cole e Execute no Neo4j Browser:**
    *   Cole a query copiada na barra de consulta do Neo4j Browser.
    *   Se a query usar um placeholder como `<ID_EXEMPLO>`, substitua-o por um ID válido de um aluno existente no seu banco.
    *   Clique no ícone de "Play" ou pressione `Ctrl+Enter` / `Cmd+Enter`.
5.  **Analise os Resultados:**
    *   Os resultados da sua consulta serão exibidos abaixo da barra de consulta, geralmente em formato de tabela ou visualização de grafo.

**Importante:** Os IDs (`38`, `6`, etc.) e os valores de semestre/ano nas queries de exemplo abaixo são baseados nos exemplos do arquivo `queries.cypher`. **Verifique se esses IDs e valores específicos existem e retornam resultados significativos nos seus dados gerados antes de executar as consultas.** Você pode encontrar IDs válidos executando consultas como `MATCH (a:Aluno) RETURN a.id_aluno LIMIT 5;` ou `MATCH (p:Professor) RETURN p.id_professor LIMIT 5;` no Neo4j Browser para listar alguns IDs existentes.

**Exemplos de Queries (do arquivo `queries.cypher`):**

*   **Histórico escolar de um aluno:**
    ```cypher
    // O arquivo queries.cypher usa o ID 38 como exemplo
    MATCH (a:Aluno {id_aluno: 38})-[r:CURSOU]->(d:Disciplina)
    RETURN d.codigo_disciplina, d.nome_disciplina, r.semestre, r.ano, r.nota_final ORDER BY r.ano, r.semestre;
    ```
*   **Disciplinas ministradas por um professor:**
    ```cypher
    // O arquivo queries.cypher usa o ID 6 como exemplo
    MATCH (p:Professor {id_professor: 6})-[r:MINISTROU]->(d:Disciplina)
    RETURN d.nome_disciplina, r.semestre, r.ano ORDER BY r.ano,     r.semestre;
    ```
*   **Alunos formados em um semestre/ano específico:**
    ```cypher
    // O arquivo queries.cypher usa 1/2023, um período para o qual o Gerador.py tenta criar dados.
    MATCH (a:Aluno)-[f:FORMADO_EM {semestre_formacao: 1, ano_formacao: 2023}]->(m:MatrizCurricular)
    RETURN a.id_aluno, a.nome_aluno, m.nome_matriz ORDER BY a.nome_aluno;
    // Para testar outros anos/semestres, você pode verificar quais foram gerados:
    // MATCH ()-[f:FORMADO_EM]->() RETURN DISTINCT f.ano_formacao, f.semestre_formacao ORDER BY f.ano_formacao, f.semestre_formacao;
    ```
*   **Professores chefes de departamento:**
    ```cypher
    MATCH (p:Professor)-[:CHEFE_DE]->(d:Departamento)
    RETURN p.id_professor, p.nome_professor, d.nome_departamento ORDER BY d.nome_departamento;
    ```
*   **Grupos de TCC e orientadores:**
    ```cypher
    MATCH (al:Aluno)-[:PARTICIPA_DE]->(tcc:TCC)<-[:ORIENTA]-(prof:Professor)
    RETURN tcc.id_tcc, tcc.titulo_tcc, prof.nome_professor AS orientador, collect({id: al.id_aluno, nome: al.nome_aluno}) AS grupo_alunos
    ORDER BY tcc.id_tcc;
    ```

