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

---

## Integrantes

*   Daniel Eiji Osato Yoshida - RA: 22.121.131-1

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

Para gerar os arquivos Cypher (`nodes.cypher`, `relationships.cypher`), execute o script Python:

1.  Abra um terminal ou prompt de comando.
2.  Navegue até o diretório onde você salvou o arquivo `Gerador.py`.
3.  Execute o script:
    ```bash
    python Gerador.py
    ```
4.  Após a execução, os arquivos `nodes.cypher` e `relationships.cypher` serão criados no mesmo diretório.

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

Você pode executar consultas Cypher diretamente no Neo4j Browser para explorar os dados carregados.
Esta seção também apresenta as 5 consultas solicitadas no item 4 dos critérios de avaliação do projeto, demonstrando como validar diferentes aspectos do modelo de dados e dos relacionamentos criados. Estas consultas servem para validar a estrutura e os dados inseridos, conforme solicitado no item 5 da entrega (descrição de como validar as queries).

1.  **Abra o Neo4j Browser** (se ainda não estiver aberto e conectado ao seu banco de dados).
2.  **Escreva ou Cole uma Query:**
    *   Você pode escrever suas próprias consultas Cypher ou colar os exemplos abaixo.
3.  **Execute no Neo4j Browser:**
    *   Cole a query na barra de consulta do Neo4j Browser.
    *   Se a query usar um placeholder como `<ID_ALUNO>`, `<ID_PROFESSOR>`, `<ANO>`, ou `<SEMESTRE>`, substitua-o por um valor válido existente no seu banco de dados.
    *   Clique no ícone de "Play" (um triângulo apontando para a direita) ou pressione `Ctrl+Enter` (Windows/Linux) ou `Cmd+Enter` (Mac).
4.  **Analise os Resultados:**
    *   Os resultados da sua consulta serão exibidos abaixo da barra de consulta.

**Importante:** Ao testar consultas com IDs específicos (ex: `id_aluno: 1`), verifique se esses IDs existem nos seus dados gerados. Você pode encontrar IDs válidos executando consultas como `MATCH (a:Aluno) RETURN a.id_aluno, a.nome_aluno LIMIT 5;` ou `MATCH (p:Professor) RETURN p.id_professor, p.nome_professor LIMIT 5;` no Neo4j Browser. Para a consulta de formados, use a query de verificação para saber quais anos/semestres têm dados.

**Consultas de Validação (Item 4 da Entrega):**

*   **1. Histórico escolar de um aluno (substitua `<ID_ALUNO>` por um ID real):**
    ```cypher
    // Exemplo: Para o aluno com id_aluno = 1
    MATCH (a:Aluno {id_aluno: 1})-[r:CURSOU]->(d:Disciplina)
    RETURN d.codigo_disciplina AS CodigoDisciplina,
           d.nome_disciplina AS NomeDisciplina,
           r.semestre AS SemestreCursado,
           r.ano AS AnoCursado,
           r.nota_final AS NotaFinal
    ORDER BY r.ano, r.semestre;
    ```

*   **2. Histórico de disciplinas ministradas por um professor (substitua `<ID_PROFESSOR>` por um ID real):**
    ```cypher
    // Exemplo: Para o professor com id_professor = 1
    MATCH (p:Professor {id_professor: 1})-[r:MINISTROU]->(d:Disciplina)
    RETURN d.codigo_disciplina AS CodigoDisciplina,
           d.nome_disciplina AS NomeDisciplina,
           r.semestre AS SemestreMinistrado,
           r.ano AS AnoMinistrado
    ORDER BY r.ano, r.semestre;
    ```

*   **3. Listar alunos que concluíram um determinado semestre de um ano com todas as notas acima de 4.0 (substitua `<ANO>` e `<SEMESTRE>`):**
    ```cypher
    // Esta consulta identifica alunos que, em um semestre e ano específicos,
    // obtiveram nota superior a 4.0 em TODAS as disciplinas cursadas naquele período.
    // Altere os valores de semestre_desejado e ano_desejado conforme sua necessidade.
    WITH 1 AS semestre_desejado, 2023 AS ano_desejado

    MATCH (aluno:Aluno)-[r:CURSOU]->(disciplina:Disciplina)
    WHERE r.semestre = semestre_desejado AND r.ano = ano_desejado

    WITH aluno, semestre_desejado, ano_desejado, collect(r.nota_final) AS notas_do_semestre_especifico
    WHERE size(notas_do_semestre_especifico) > 0 // Garante que o aluno cursou algo no período
      AND none(nota IN notas_do_semestre_especifico WHERE nota <= 4.0) // Nenhuma nota menor ou igual a 4.0

    RETURN aluno.id_aluno AS IDAluno,
           aluno.nome_aluno AS NomeAluno,
           semestre_desejado,
           ano_desejado,
           notas_do_semestre_especifico AS NotasNoSemestreAno
    ORDER BY NomeAluno;

    // Para verificar QUAIS anos/semestres possuem dados de alunos cursando disciplinas:
    // MATCH (a:Aluno)-[r:CURSOU]->(d:Disciplina)
    // RETURN DISTINCT r.ano AS AnoCursado, r.semestre AS SemestreCursado
    // ORDER BY AnoCursado, SemestreCursado;
    ```

*   **4. Listar todos os professores que são chefes de departamento, junto com o nome do departamento:**
    ```cypher
    MATCH (p:Professor)-[:CHEFE_DE]->(d:Departamento)
    RETURN p.id_professor AS IDProfessor,
           p.nome_professor AS NomeProfessor,
           d.nome_departamento AS NomeDepartamento
    ORDER BY NomeDepartamento, NomeProfessor;
    ```

*   **5. Saber quais alunos formaram um grupo de TCC e qual professor foi o orientador:**
    ```cypher
    MATCH (aluno:Aluno)-[:PARTICIPA_DE]->(tcc:TCC)<-[:ORIENTA]-(professor:Professor)
    RETURN tcc.id_tcc AS ID_TCC,
           tcc.titulo_tcc AS TituloTCC,
           professor.nome_professor AS NomeOrientador,
           collect({id_aluno: aluno.id_aluno, nome_aluno: aluno.nome_aluno}) AS GrupoAlunos
    ORDER BY ID_TCC, NomeOrientador;
    ```

---

