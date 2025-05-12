from cassandra.cluster import Cluster

# Função para obter uma sessão de conexão com o Cassandra
def get_cassandra_session():
    # Configura a conexão com o cluster Cassandra local
    cluster = Cluster(['127.0.0.1'])
    # Conecta ao keyspace 'fei'
    session = cluster.connect('fei')
    return session

# Função para criar as tabelas no keyspace 'fei'
def create_tables(session):

    # Cria a tabela 'alunos' se ela não existir
    session.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id_aluno int PRIMARY KEY,
            nome text,
            disciplinas_concluidas map<text, frozen<tuple<int, int, float>>>
        )
    """)
    # Cria a tabela 'professor' se ela não existir
    session.execute("""
        CREATE TABLE IF NOT EXISTS professor (
            id_professor int PRIMARY KEY,
            nome text,
            id_departamento int,
            disciplinas_ministradas map<text, frozen<tuple<int, int>>>
        )
    """)
    # Cria a tabela 'departamento' se ela não existir
    session.execute("""
        CREATE TABLE IF NOT EXISTS departamento (
            id_departamento int PRIMARY KEY,
            nome text,
            id_chefe_departamento int,
            disciplinas set<text>
        )
    """)
    # Cria a tabela 'alunos_formado' se ela não existir
    session.execute("""
        CREATE TABLE IF NOT EXISTS alunos_formado (
            ano int,
            semestre int,
            id_aluno int,
            nome text,
            PRIMARY KEY ((ano, semestre), id_aluno)
        ) WITH CLUSTERING ORDER BY (id_aluno ASC)
    """)
    # Cria a tabela 'grupo_proj' se ela não existir
    session.execute("""
        CREATE TABLE IF NOT EXISTS grupo_proj (
            id_grupo int PRIMARY KEY,
            id_professor int,
            membros list<int>
        )
    """)

# Bloco principal que executa ao rodar o script
if __name__ == "__main__":
    # Obtém a sessão do Cassandra
    session = get_cassandra_session()
    # Chama a função para criar as tabelas
    create_tables(session)
    print("Tabelas Criada com Sucesso!")
    # Fecha a conexão com o cluster
    session.cluster.shutdown()
