## Configuração do Ambiente

Para executar este projeto, você precisará configurar o Python e o Cassandra.

### 1. Configuração do Python

*   **Instale o Python:** Este projeto requer **Python 3.7.9 ou inferior**. Versões mais recentes podem não ser compatíveis com a dependência `cassandra-driver`.
    *   Você pode baixar o Python 3.7.9 para Windows aqui: <mcurl name="Python 3.7.9 Download" url="https://www.python.org/downloads/release/python-379/"></mcurl>
    *   Durante a instalação, certifique-se de marcar a opção "Add Python 3.7 to PATH".

*   **Verifique a Versão do Python:** Abra seu terminal e execute:
    ```bash
    python --version
    ```
    *   Se a versão exibida for 3.7.9 ou inferior, você pode prosseguir.
    *   Se for uma versão diferente, você precisará usar o caminho completo para o executável do Python 3.7.9 ou um alias (como `py -3.7`) nos comandos a seguir. Exemplo: `C:\path\to\python3.7.9\python.exe -m venv venv` ou `py -3.7 -m venv venv`.

*   **Crie e Ative um Ambiente Virtual (Recomendado):**
    *   Abra seu terminal ou prompt de comando na pasta do projeto.
    *   Execute os seguintes comandos (substitua `python` se necessário, conforme a verificação de versão acima):
        ```bash
        # Cria um ambiente virtual chamado 'venv'
        python -m venv venv

        # Ativa o ambiente virtual (Windows PowerShell/Terminal Integrado)
        .\venv\Scripts\activate

        # Ativa o ambiente virtual (Windows CMD)
        # venv\Scripts\activate.bat

        # Ativa o ambiente virtual (Linux/macOS)
        # source venv/bin/activate
        ```

*   **Instale as Dependências:** Com o ambiente virtual ativado, instale as bibliotecas Python necessárias:
    ```bash
    pip install -r requirements.txt
    ```
    *   Isso instalará as bibliotecas listadas no arquivo <mcfile name="requirements.txt" path="f:\Github\nosql-database\Projeto 2 - Wide-column Store\requirements.txt"></mcfile> (`cassandra-driver` e `Faker`).

### 2. Configuração do Docker (Cassandra Local)

Para executar este projeto, é necessário ter uma instância do Apache Cassandra rodando. Você pode usar o Docker para configurar um container Cassandra localmente.

*   **Instale o Docker:**
    *   Certifique-se de ter o Docker Desktop instalado e em execução na sua máquina.
    *   Instruções de instalação e download: <mcurl name="Docker Official Website" url="https://docs.docker.com/get-docker/"></mcurl>
    *   *Observação:* Os comandos Docker a seguir podem ser executados no PowerShell, mas é recomendável usar o terminal integrado da sua IDE (que geralmente usa PowerShell por padrão no Windows).

*   **Baixe a Imagem do Cassandra:**
    ```bash
    docker pull cassandra:latest
    ```

*   **Execute o Container Cassandra:**
    ```bash
    docker run --name my-cassandra -p 9042:9042 -d cassandra:latest
    ```
    *   `--name my-cassandra`: Define um nome para o container.
    *   `-p 9042:9042`: Mapeia a porta 9042 do container para a porta 9042 da sua máquina host.
    *   `-d`: Executa o container em modo detached (em segundo plano).
    *   `cassandra:latest`: Especifica a imagem a ser usada.

*   **Verifique se o Container está Rodando:**
    ```bash
    docker ps
    ```
    *   Você deve ver o container `my-cassandra` listado. Pode levar alguns instantes para o Cassandra iniciar completamente.

*   **Criação do Keyspace (Importante):** O keyspace `fei` precisa existir no Cassandra. O script <mcfile name="Creationtable.py" path="f:\Github\nosql-database\Projeto 2 - Wide-column Store\Creationtable.py"></mcfile> tentará se conectar a ele. Se não existir, crie-o manualmente usando os comandos abaixo no seu terminal:

    1.  Conecte-se ao `cqlsh` dentro do container:
        ```bash
        docker exec -it my-cassandra cqlsh
        ```
    2.  Dentro do `cqlsh` (o prompt mudará para `cqlsh>`), execute o comando para criar o keyspace:
        ```cql
        CREATE KEYSPACE fei WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
        ```
    3.  Digite `exit;` e pressione Enter para sair do `cqlsh`.

## Execução dos Scripts Python

Com o ambiente Python configurado, o ambiente virtual ativado e o container Cassandra rodando com o keyspace `fei` criado, execute os scripts na seguinte ordem no seu terminal (com o ambiente virtual ativado):

1.  **Criar as Tabelas:**
    ```bash
    python Creationtable.py
    ```
    *   Este script se conecta ao Cassandra e cria as tabelas necessárias no keyspace `fei`.

2.  **Gerar Dados Fictícios:**
    ```bash
    python gerador.py
    ```
    *   Este script usa a biblioteca Faker para gerar dados fictícios e salva os comandos `INSERT` em arquivos `.cql` (por exemplo, <mcfile name="1alunos.cql" path="f:\Github\nosql-database\Projeto 2 - Wide-column Store\1alunos.cql"></mcfile>, <mcfile name="1professores.cql" path="f:\Github\nosql-database\Projeto 2 - Wide-column Store\1professores.cql"></mcfile>, etc.).

3.  **Injetar Dados no Cassandra:**
    ```bash
    python inject.py
    ```
    *   Este script lê os arquivos `.cql` gerados e executa os comandos `INSERT` para popular as tabelas no Cassandra.

## Executando Consultas CQL (Exemplos)

Após popular o banco de dados, você pode executar consultas diretamente no Cassandra usando `cqlsh`.

1.  **Conecte-se ao `cqlsh`:** Abra seu terminal e conecte-se ao container Docker:
    ```bash
    docker exec -it my-cassandra cqlsh
    ```

2.  **Use o Keyspace Correto:** Dentro do `cqlsh` (o prompt mudará para `cqlsh>`), selecione o keyspace onde as tabelas foram criadas:
    ```cql
    USE fei;
    ```

3.  **Execute as Consultas:** Agora você pode executar as consultas CQL. Abaixo estão exemplos baseados nas funcionalidades solicitadas (lembre-se de substituir os IDs de exemplo pelos IDs reais gerados ou que você deseja consultar):

    *   **1. Histórico escolar de um aluno:** Retorna o mapa de disciplinas concluídas, com semestre, ano e nota.
        ```cql
        -- Substitua 1 pelo ID do aluno desejado
        SELECT disciplinas_concluidas FROM alunos WHERE id_aluno = 1;
        ```

    *   **2. Histórico de disciplinas ministradas por um professor:** Retorna o mapa de disciplinas ministradas, com semestre e ano.
        ```cql
        -- Substitua 3 pelo ID do professor desejado
        SELECT disciplinas_ministradas FROM professor WHERE id_professor = 3;
        ```

    *   **3. Listar alunos formados em um semestre/ano:** Retorna o ID e nome dos alunos formados no período especificado.
        ```cql
        -- Substitua 2023 e 2 pelo ano e semestre desejados
        SELECT id_aluno, nome FROM alunos_formado WHERE ano = 2023 AND semestre = 2;
        ```

    *   **4. Listar professores chefes de departamento:** Esta consulta requer duas etapas no CQL puro para obter o nome do professor e o nome do departamento que ele chefia.
        *   **Etapa A:** Obtenha os IDs dos chefes e os nomes dos departamentos.
            ```cql
            SELECT id_chefe_departamento, nome FROM departamento;
            ```
        *   **Etapa B:** Para cada `id_chefe_departamento` retornado na Etapa A, busque o nome do professor correspondente. (Você pode fazer isso individualmente ou buscar todos os professores e filtrar na sua aplicação).
            ```cql
            -- Exemplo: Se a Etapa A retornou um chefe com ID 5
            SELECT nome FROM professor WHERE id_professor = 5;
            -- Ou para buscar vários chefes (ex: IDs 1, 5, 8)
            -- SELECT id_professor, nome FROM professor WHERE id_professor IN (1, 5, 8);
            ```

    *   **5. Membros e orientador de um grupo de TCC:** Similar à consulta 4, requer múltiplas etapas para obter todos os nomes.
        *   **Etapa A:** Obtenha o ID do professor orientador e a lista de IDs dos membros do grupo.
            ```cql
            -- Substitua 2 pelo ID do grupo desejado
            SELECT id_professor, membros FROM grupo_proj WHERE id_grupo = 2;
            ```
        *   **Etapa B:** Busque o nome do professor orientador usando o `id_professor` da Etapa A.
            ```cql
            -- Exemplo: Se id_professor for 4
            SELECT nome FROM professor WHERE id_professor = 4;
            ```
        *   **Etapa C:** Busque os nomes dos alunos membros usando a lista `membros` da Etapa A.
            ```cql
            -- Exemplo: Se membros for [10, 15, 22]
            SELECT id_aluno, nome FROM alunos WHERE id_aluno IN (10, 15, 22);
            ```

4.  **Sair do `cqlsh`:** Quando terminar, digite `exit;` e pressione Enter.

## Parando e Removendo o Container (Opcional)

*   Para parar o container Cassandra:
    ```bash
    docker stop my-cassandra
    ```
*   Para remover o container (após parado):
    ```bash
    docker rm my-cassandra
    ```
