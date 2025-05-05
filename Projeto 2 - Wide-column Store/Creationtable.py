from cassandra.cluster import Cluster

def get_cassandra_session():
    # Configuração para conectar ao Cassandra local via Docker
    # Substitua '127.0.0.1' se o seu container Cassandra estiver exposto em outro IP/hostname
    cluster = Cluster(['127.0.0.1'])
    # Mantém a conexão ao keyspace 'fei'
    session = cluster.connect('fei')
    return session

def create_tables(session):

    session.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id_aluno int PRIMARY KEY,
            nome text,
            -- id_curso int,       // Removido
            -- id_disciplina int,  // Removido
            disciplinas_concluidas map<text, frozen<tuple<int, int, float>>>
        )
    """)
    session.execute("""
        CREATE TABLE IF NOT EXISTS professor (
            id_professor int PRIMARY KEY,
            nome text,
            id_departamento int,
            disciplinas_ministradas map<text, frozen<tuple<int, int>>>
        )
    """)
    session.execute("""
        CREATE TABLE IF NOT EXISTS departamento (
            id_departamento int PRIMARY KEY,
            nome text,
            id_chefe_departamento int,
            disciplinas set<text>
        )
    """)
    session.execute("""
        CREATE TABLE IF NOT EXISTS alunos_formado (
            ano int,
            semestre int,
            id_aluno int,
            nome text,
            PRIMARY KEY ((ano, semestre), id_aluno)
        ) WITH CLUSTERING ORDER BY (id_aluno ASC)
    """)
    session.execute("""
        CREATE TABLE IF NOT EXISTS grupo_proj (
            id_grupo int PRIMARY KEY,
            id_professor int,
            membros list<int>
        )
    """)

if __name__ == "__main__":
    session = get_cassandra_session()
    create_tables(session)
    print("Tables created or updated successfully!")
    session.cluster.shutdown()
