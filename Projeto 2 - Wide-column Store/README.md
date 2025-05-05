## Configuração do Ambiente

Para executar este projeto, você precisará configurar o Python e o Cassandra.

### 1. Configuração do Python

*   **Instale o Python:** Este projeto requer **Python 3.7.9 ou inferior**. Versões mais recentes podem não ser compatíveis com a dependência `cassandra-driver`.
    *   Você pode baixar o Python 3.7.9 para Windows aqui: <mcurl name="Python 3.7.9 Download" url="https://www.python.org/downloads/release/python-379/"></mcurl>
    *   Durante a instalação, certifique-se de marcar a opção "Add Python 3.7 to PATH".

*   **Crie e Ative um Ambiente Virtual (Recomendado):**
    *   Abra seu terminal ou prompt de comando na pasta do projeto.
    *   Execute os seguintes comandos:
        ```bash
        # Cria um ambiente virtual chamado 'venv'
        python -m venv venv

        # Ativa o ambiente virtual (Windows)
        .\venv\Scripts\activate

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
    *   Certifique-se de ter o Docker instalado e em execução na sua máquina.
    *   Instruções de instalação: <mcurl name="Docker Official Website" url="https://docs.docker.com/get-docker/"></mcurl>

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

*   **Criação do Keyspace (Importante):** O keyspace `fei` precisa existir no Cassandra. O script <mcfile name="Creationtable.py" path="f:\Github\nosql-database\Projeto 2 - Wide-column Store\Creationtable.py"></mcfile> tentará se conectar a ele. Se não existir, crie-o manualmente:
    1.  Conecte-se ao `cqlsh` dentro do container: `docker exec -it my-cassandra cqlsh`
    2.  Execute o comando CQL: `CREATE KEYSPACE fei WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};`
    3.  Digite `exit;` para sair do `cqlsh`.

## Execução dos Scripts Python

Com o ambiente Python configurado, o ambiente virtual ativado e o container Cassandra rodando com o keyspace `fei` criado, execute os scripts na seguinte ordem:

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

4.  **(Opcional) Executar Queries:**
    *   Se você tiver um script `querys.py` (não listado nos arquivos fornecidos, mas mencionado no README original), execute-o para testar consultas:
      ```bash
      python querys.py
      ```

## Parando e Removendo o Container (Opcional)

*   Para parar o container Cassandra:
    ```bash
    docker stop my-cassandra
    ```
*   Para remover o container (após parado):
    ```bash
    docker rm my-cassandra
    ```