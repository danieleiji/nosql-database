## Configuração do Docker (Cassandra Local)

Para executar este projeto, é necessário ter uma instância do Apache Cassandra rodando. Você pode usar o Docker para configurar um container Cassandra localmente.

### 1. Instale o Docker

*   Certifique-se de ter o Docker instalado e em execução na sua máquina.
*   Você pode encontrar as instruções de instalação para o seu sistema operacional no site oficial do Docker:
    *   [COLE O LINK DE INSTALAÇÃO DO DOCKER AQUI]

### 2. Baixe a Imagem do Cassandra

*   Abra seu terminal ou prompt de comando e execute o seguinte comando para baixar a imagem oficial do Cassandra:

    ```bash
    docker pull cassandra:latest
    ```

### 3. Execute o Container Cassandra

*   Execute o seguinte comando para iniciar um container Cassandra. Este comando mapeia a porta padrão do Cassandra (9042) para a sua máquina local e nomeia o container como `my-cassandra` para facilitar o gerenciamento:

    ```bash
    docker run --name my-cassandra -p 9042:9042 -d cassandra:latest
    ```
    *   `--name my-cassandra`: Define um nome para o container.
    *   `-p 9042:9042`: Mapeia a porta 9042 do container para a porta 9042 da sua máquina host.
    *   `-d`: Executa o container em modo detached (em segundo plano).
    *   `cassandra:latest`: Especifica a imagem a ser usada.

### 4. Verifique se o Container está Rodando

*   Você pode verificar se o container está em execução com o comando:

    ```bash
    docker ps
    ```
    *   Você deve ver o container `my-cassandra` listado. Pode levar alguns instantes para o Cassandra iniciar completamente dentro do container.

### 5. Conectando os Scripts Python

*   Os scripts Python neste projeto (`Creationtable.py`, `inject.py`, `querys.py`) já estão configurados para se conectar ao Cassandra no endereço `127.0.0.1` na porta `9042`, que corresponde à configuração padrão do container Docker.

*   **Importante:** O keyspace `fei` precisa existir no Cassandra para que os scripts funcionem. O script `Creationtable.py` tentará se conectar a este keyspace e criar as tabelas dentro dele. Se o keyspace não existir, a conexão inicial pode falhar.

    Idealmente, o script `Creationtable.py` deve ser capaz de criar o keyspace se ele não existir (verifique o código do script para confirmar). No entanto, se você encontrar erros relacionados à ausência do keyspace após iniciar o container e antes de executar os scripts, pode ser necessário criá-lo manualmente:

    1.  Abra um terminal e conecte-se ao `cqlsh` dentro do container Docker (substitua `my-cassandra` pelo nome real do seu container, se for diferente):
        ```bash
        docker exec -it my-cassandra cqlsh
        ```
    2.  Dentro do `cqlsh`, execute o comando CQL para criar o keyspace:
        ```cql
        CREATE KEYSPACE fei WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
        ```
    3.  Verifique se o keyspace foi criado (opcional):
        ```cql
        DESCRIBE KEYSPACES;
        ```
        Você deve ver `fei` na lista.
    4.  Digite `exit;` e pressione Enter para sair do `cqlsh`.

    Após garantir que o keyspace `fei` existe, você pode executar os scripts Python conforme necessário.

### 6. Parando e Removendo o Container (Opcional)

*   Para parar o container:
    ```bash
    docker stop my-cassandra
    ```
*   Para remover o container (após parado):
    ```bash
    docker rm my-cassandra
    ```

Agora você pode seguir as instruções na seção "Execução" do seu README para criar as tabelas, inserir dados e executar as queries usando a instância local do Cassandra via Docker.
