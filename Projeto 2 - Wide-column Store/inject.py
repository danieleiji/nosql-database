from cassandra.cluster import Cluster
import os

# Função para obter uma sessão de conexão com o Cassandra
def get_cassandra_session():
    # Configura a conexão com o cluster Cassandra local
    cluster = Cluster(['127.0.0.1'])
    # Conecta ao keyspace 'fei'
    session = cluster.connect('fei')
    return session

# Função para ler arquivos .cql e executar os comandos INSERT
def execute_inserts_from_files(file_names):
    # Obtém a sessão do Cassandra
    session = get_cassandra_session()
    # Itera sobre a lista de nomes de arquivos fornecida
    for file_name in file_names:
        # Verifica se o arquivo existe
        if os.path.exists(file_name):
            print(f"Lendo o arquivo: {file_name}")
            try:
                # Tenta ler o arquivo com encoding UTF-8
                with open(file_name, 'r', encoding="utf-8") as file:
                    # Separa os comandos pelo caractere ';'
                    commands = file.read().split(';')
            except Exception as e:
                # Se falhar, tenta com o encoding padrão do sistema
                print(f"Erro ao abrir com UTF-8: {e}")
                try:
                    print("Tentando abrir com encoding padrão do sistema...")
                    with open(file_name, 'r') as file:
                        commands = file.read().split(';')
                except Exception as e2:
                    # Se falhar novamente, reporta o erro e continua para o próximo arquivo
                    print(f"Erro ao abrir o arquivo: {file_name}\nErro: {e2}")
                    continue

            # Itera sobre os comandos lidos do arquivo
            for command in commands:
                # Remove espaços em branco extras
                command = command.strip()
                # Verifica se o comando é um INSERT (ignorando maiúsculas/minúsculas)
                if command.upper().startswith("INSERT"):
                    try:
                        # Executa o comando INSERT (adicionando o ';' de volta)
                        session.execute(command + ";")
                        # print("Comando executado com sucesso:", command) # Descomente para debug detalhado
                    except Exception as e:
                        # Reporta erro na execução do comando específico
                        print(f"Erro ao executar o comando: {command}\nErro: {e}")
        else:
            # Reporta se um arquivo da lista não foi encontrado
            print(f"Arquivo {file_name} não encontrado.")

# Lista dos arquivos .cql a serem processados
file_names = [
    "1alunos_formados.cql",
    "1alunos.cql",
    "1departamentos.cql",
    "1grupo_proj.cql",
    "1professores.cql"
]

# Bloco principal que executa ao rodar o script
# Chama a função para executar os inserts dos arquivos listados
execute_inserts_from_files(file_names)
print("Injeção de dados concluída.") # Mensagem de conclusão
