# Projeto 1 - Document Store (Banco de Dados NoSQL)

Este projeto demonstra a modelagem e consulta de dados acadêmicos utilizando MongoDB como um banco de dados orientado a documentos. Ele inclui scripts para gerar dados fictícios, inseri-los no banco e realizar consultas específicas.

## Integrante

*   Daniel Eiji Osato Yoshida - RA: 22.121.131-1

## Dependências

### Python

*   **pymongo:** Driver oficial do MongoDB para Python.
*   **Faker:** Biblioteca para gerar dados fictícios.

Você pode instalar as dependências Python usando pip:

```bash
pip install pymongo faker
```

**Nota sobre a Criação das Coleções:**

Este projeto não inclui scripts `.js` separados especificamente para a criação das coleções (`db.createCollection(...)`). O MongoDB cria coleções (e o próprio banco de dados `feidb`, se ele não existir) automaticamente na primeira vez que um documento é inserido nelas. O script `insert.py`, ao ser executado, realiza essa primeira inserção para cada tipo de dado (alunos, professores, etc.), garantindo assim que todas as coleções necessárias sejam criadas implicitamente no banco `feidb`. Como alternativa, o comando `use feidb` no `mongosh` cria o banco de dados, mas as coleções ainda serão criadas na primeira inserção pelo `insert.py`.

### MongoDB

*   É necessário ter uma instância do MongoDB em execução (localmente ou em um servidor). A URI de conexão padrão nos scripts é `mongodb://localhost:27017/`.
*   Os scripts `insert.py` e `query.py` esperam que exista um banco de dados chamado `feidb`. O script `insert.py` criará as coleções dentro deste banco de dados se elas não existirem. Você pode criar o banco de dados manualmente no `mongosh` com o comando `use feidb` antes de executar os scripts, ou deixar que a primeira inserção o crie.

## Instruções Passo a Passo

1.  **Gerar Dados Fictícios:**
    Execute o script <mcfile name="Gerador.py" path="f:\Github\nosql-database\Projeto 1 - Document Store\Gerador.py"></mcfile> para criar os arquivos JSON com dados simulados de alunos, professores, cursos, etc.
    ```bash
    python Gerador.py
    ```
    Isso criará/sobrescreverá os seguintes arquivos JSON no diretório:
    *   `alunos.json`
    *   `professores.json`
    *   `cursos.json`
    *   `departamentos.json`
    *   `disciplinas.json`
    *   `grupos_tcc.json`

2.  **Inserir Dados no MongoDB:**
    Execute o script <mcfile name="insert.py" path="f:\Github\nosql-database\Projeto 1 - Document Store\insert.py"></mcfile> para ler os arquivos JSON gerados e inseri-los nas coleções correspondentes no banco de dados `feidb`.
    *   **Atenção:** Por padrão, o script `insert.py` (com `LIMPAR_COLECOES_ANTES = True`) limpará as coleções antes de inserir novos dados.
    ```bash
    python insert.py
    
    ```
3.  **Executar Consultas (Queries):**
    Existem duas maneiras principais de executar as consultas predefinidas no banco `feidb`:

    *   **Método 1: Usando o Shell Embutido do MongoDB Compass**
        Esta é uma forma direta de testar as consultas JavaScript.
        1.  Abra o **MongoDB Compass** e conecte-se à sua instância MongoDB.
        2.  No painel esquerdo, selecione ou crie o banco de dados `feidb`.
        3.  Clique na aba `_MongoSH` para abrir o shell embutido.
        4.  Abra o arquivo `.js` da consulta desejada (por exemplo, `Query_1_Historico_aluno.js`) em um editor de texto.
        5.  **Importante:** Muitas consultas requerem um ID específico (como `aluno_id`). Verifique o código no arquivo `.js` e, se necessário, **edite o valor do ID diretamente no código** antes de copiar.
        6.  **Copie todo o conteúdo** do arquivo `.js` editado.
        7.  **Cole o código copiado** diretamente no prompt do `_MongoSH` dentro do Compass e pressione Enter para executar a consulta. Os resultados aparecerão na janela do shell.

    *   **Método 2: Usando o Script Python Interativo (`query.py`) (Recomendado para Facilidade)**
        Para uma experiência mais **simples e guiada**, sem precisar editar arquivos `.js` manualmente, utilize o script Python. Ele apresenta um menu para selecionar a consulta e solicita os IDs necessários interativamente.
        1.  No seu terminal, navegue até o diretório do projeto.
        2.  Execute o script:
            ```bash
            python query.py
            ```
        3.  Siga as instruções apresentadas no menu para escolher a consulta e fornecer os dados solicitados (como IDs ou semestres). Os resultados serão impressos diretamente no terminal.

    *   **Método 2: Usando o Script Python Interativo (`query.py`) (Recomendado para facilidade)**
        Para uma experiência mais **simples e guiada**, você pode usar o script Python fornecido. Ele apresenta um menu para selecionar a consulta e solicita os IDs necessários interativamente.
        1.  No seu terminal, execute o script:
            ```bash
            python query.py
            ```
        2.  Siga as instruções apresentadas no menu para escolher e executar a consulta desejada.

## Descrição das Coleções do Banco de Dados `feidb`

O banco de dados `feidb` contém as seguintes coleções:

1.  **`departamentos`**: Armazena informações sobre os departamentos acadêmicos.
    *   `_id`: Identificador único do departamento.
    *   `nome`: Nome do departamento.
    *   `codigo_dept`: Código único do departamento (ex: "INF", "MAT").
    *   `chefe_id`: Referência (`_id`) ao professor que chefia o departamento (da coleção `professores`).

2.  **`cursos`**: Armazena informações sobre os cursos de graduação.
    *   `_id`: Identificador único do curso.
    *   `nome`: Nome do curso (ex: "Graduação em Engenharia de Software").
    *   `departamento_id`: Referência (`_id`) ao departamento que oferece o curso (da coleção `departamentos`).
    *   `disciplinas_ids`: Lista de referências (`_id`) às disciplinas que compõem o curso (da coleção `disciplinas`).

3.  **`disciplinas`**: Armazena informações sobre as disciplinas.
    *   `_id`: Identificador único da disciplina.
    *   `codigo`: Código único da disciplina (ex: "INF101").
    *   `nome`: Nome da disciplina (ex: "Algoritmos e Estruturas de Dados").

4.  **`professores`**: Armazena informações sobre os professores.
    *   `_id`: Identificador único do professor.
    *   `nome`: Nome do professor.
    *   `departamento_id`: Referência (`_id`) ao departamento ao qual o professor pertence (da coleção `departamentos`).
    *   `eh_chefe`: Booleano indicando se o professor é chefe do seu departamento.
    *   `disciplinas_ministradas`: Lista de documentos embutidos, cada um representando uma oferta de disciplina:
        *   `disciplina_id`: Referência (`_id`) à disciplina ministrada (da coleção `disciplinas`).
        *   `semestre`: Semestre em que a disciplina foi ministrada (formato "AAAA.S").
        *   `ano`: Ano em que a disciplina foi ministrada.

5.  **`alunos`**: Armazena informações sobre os alunos.
    *   `_id`: Identificador único do aluno.
    *   `nome`: Nome do aluno.
    *   `curso_id`: Referência (`_id`) ao curso em que o aluno está matriculado (da coleção `cursos`).
    *   `historico`: Lista de documentos embutidos, representando o histórico acadêmico do aluno:
        *   `codigo`: Código da disciplina cursada.
        *   `nome`: Nome da disciplina cursada.
        *   `semestre`: Semestre em que a disciplina foi cursada.
        *   `ano`: Ano em que a disciplina foi cursada.
        *   `nota_final`: Nota obtida pelo aluno.
        *   `status`: Situação do aluno na disciplina ("Aprovado", "Reprovado").
    *   `graduado`: Booleano indicando se o aluno já se graduou.
    *   `semestre_graduacao`: Semestre em que o aluno se graduou (formato "AAAA.S"), se aplicável.

6.  **`grupos_tcc`**: Armazena informações sobre os grupos de Trabalho de Conclusão de Curso (TCC).
    *   `_id`: Identificador único do grupo de TCC.
    *   `orientador_id`: Referência (`_id`) ao professor orientador (da coleção `professores`).
    *   `alunos_ids`: Lista de referências (`_id`) aos alunos que compõem o grupo (da coleção `alunos`).
    *   `semestre`: Semestre de realização do TCC (formato "AAAA.S").

## Queries Implementadas

As seguintes consultas estão disponíveis:

1.  **Histórico Escolar de um Aluno:** Dado o ID de um aluno, retorna seu nome e o histórico de disciplinas cursadas (código, nome, semestre, nota, status).
    *   Implementação:https://github.com/danieleiji/nosql-database/blob/main/Projeto%201%20-%20Document%20Store/Query_1_Historico_aluno
2.  **Histórico de Disciplinas Ministradas por um Professor:** Dado o ID de um professor, retorna seu nome e as disciplinas que ele ministrou (código, nome, semestre).
    *   Implementação:https://github.com/danieleiji/nosql-database/blob/main/Projeto%201%20-%20Document%20Store/Query_2_Hist%C3%B3rico_Ministrado_Prof

3.  **Listar Alunos Graduados:** Dado um semestre/ano (formato "AAAA.S"), lista os alunos (ID e nome) que se graduaram nesse período.
    *   Implementação: https://github.com/danieleiji/nosql-database/blob/main/Projeto%201%20-%20Document%20Store/Query_3_Lista_aluno

4.  **Listar Professores Chefes de Departamento:** Lista todos os professores que são chefes de departamento, juntamente com o nome e código do departamento que chefiam.
    *   Implementação: https://github.com/danieleiji/nosql-database/blob/main/Projeto%201%20-%20Document%20Store/Query_4_Professor_chefe_departamento
    *   
5.  **Detalhes de um Grupo de TCC:** Dado o ID de um grupo de TCC, retorna o semestre, o nome do orientador e a lista de nomes dos alunos participantes.
    *   Implementação: https://github.com/danieleiji/nosql-database/blob/main/Projeto%201%20-%20Document%20Store/Query_5_Grupo_TCC
```
