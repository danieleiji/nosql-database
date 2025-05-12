import random
from faker import Faker

# Inicializa o Faker para gerar dados em português do Brasil
fake = Faker('pt_BR')

# Lista de disciplinas disponíveis
disciplinas = ["Cálculo I", "Álgebra Linear", "Complexidade de Algoritmo", "Computação Grafica", "CC6240", "Compilador",
                "Banco de Dados", "Redes de Computadores","Software orientado a objetos","Sistemas Operacionais"]

# Contadores globais para gerar IDs sequenciais
aluno_counter = 1
professor_counter = 1
departamento_counter = 1
grupo_counter = 1

# Listas globais para armazenar os IDs gerados e garantir referências válidas
departamentos_ids = []
alunos_ids = []
professor_ids = []

# Função principal para gerar os comandos INSERT para todas as tabelas
def generate_insert_statements(num_alunos=75, num_professores=20, num_departamentos=10, num_alunos_formados=40, num_grupos=15):
    global aluno_counter, professor_counter, departamento_counter, grupo_counter

    # Listas para armazenar os comandos INSERT gerados
    alunos_inserts = []
    professores_inserts = []
    departamentos_inserts = []
    alunos_formados_inserts = []
    grupo_proj_inserts = []

    # --- Geração de Departamentos ---
    for _ in range(num_departamentos):
        id_departamento = departamento_counter
        departamentos_ids.append(id_departamento)
        nome_departamento = fake.company()
        num_disciplinas_dept = random.randint(1, 3)
        departamento_disciplinas = random.sample(disciplinas, num_disciplinas_dept)
        disciplinas_str = ', '.join([f"'{d}'" for d in departamento_disciplinas])
        departamentos_inserts.append(
            (id_departamento, nome_departamento, disciplinas_str)
        )
        departamento_counter += 1

    # --- Geração de Professores ---
    for _ in range(num_professores):
        id_professor = professor_counter
        professor_ids.append(id_professor)
        nome = fake.name()
        id_departamento = random.choice(departamentos_ids)
        disciplinas_ministradas = {}
        num_disciplinas_ministradas = random.randint(1, 4)
        disciplinas_selecionadas = random.sample(disciplinas, num_disciplinas_ministradas)
        for disciplina in disciplinas_selecionadas:
            semestre = random.randint(1, 2)
            ano = random.randint(2018, 2024)
            disciplinas_ministradas[disciplina] = (semestre, ano)

        disciplinas_ministradas_str = '{' + ', '.join([f"'{k}': ({v[0]}, {v[1]})" for k, v in disciplinas_ministradas.items()]) + '}'

        professores_inserts.append(
            f"INSERT INTO professor (id_professor, nome, id_departamento, disciplinas_ministradas) "
            f"VALUES ({id_professor}, '{nome}', {id_departamento}, {disciplinas_ministradas_str});"
        )
        professor_counter += 1

    # --- Atualização de Departamentos com Chefes ---
    final_departamentos_inserts = []
    temp_professor_ids = professor_ids[:] # Copia para manipulação
    for id_dept, nome_dept, disciplinas_str_dept in departamentos_inserts:
        if temp_professor_ids:
            id_chefe = random.choice(temp_professor_ids)
            temp_professor_ids.remove(id_chefe)
        elif professor_ids:
             id_chefe = random.choice(professor_ids)
        else:
            id_chefe = 0

        final_departamentos_inserts.append(
            f"INSERT INTO departamento (id_departamento, nome, id_chefe_departamento, disciplinas) "
            f"VALUES ({id_dept}, '{nome_dept}', {id_chefe}, {{ {disciplinas_str_dept} }});"
        )

    # --- Geração de Alunos ---
    for _ in range(num_alunos):
        id_aluno = aluno_counter
        alunos_ids.append(id_aluno)
        nome = fake.name()

        disciplinas_concluidas = {}
        num_disciplinas_concluidas = random.randint(1, len(disciplinas))
        disciplinas_selecionadas = random.sample(disciplinas, num_disciplinas_concluidas)
        for disciplina in disciplinas_selecionadas:
            semestre = random.randint(1, 8)
            ano = random.randint(2018, 2024)
            nota = round(random.uniform(0, 10), 2)
            disciplinas_concluidas[disciplina] = (semestre, ano, nota)

        disciplinas_concluidas_str = '{' + ', '.join([f"'{k}': ({v[0]}, {v[1]}, {v[2]})" for k, v in disciplinas_concluidas.items()]) + '}'

        alunos_inserts.append(
            f"INSERT INTO alunos (id_aluno, nome, disciplinas_concluidas) VALUES ({id_aluno}, '{nome}', {disciplinas_concluidas_str});"
        )
        aluno_counter += 1

    # --- Geração de Alunos Formados ---
    # Seleciona aleatoriamente alunos da lista de alunos existentes
    alunos_formados_sample = random.sample(alunos_ids, min(num_alunos_formados, len(alunos_ids)))
    for id_aluno_formado in alunos_formados_sample:
        ano = random.randint(2020, 2024)
        semestre = random.randint(1, 2)
        nome_formado = fake.name()
        alunos_formados_inserts.append(
            f"INSERT INTO alunos_formado (ano, semestre, id_aluno, nome) VALUES ({ano}, {semestre}, {id_aluno_formado}, '{nome_formado}');"
        )

    # --- Geração de Grupos de Projeto ---
    # Garante que existam professores e alunos suficientes
    if professor_ids and len(alunos_ids) >= 2:
        for _ in range(num_grupos):
            id_grupo = grupo_counter
            id_professor_grupo = random.choice(professor_ids)
            num_membros = random.randint(2, min(5, len(alunos_ids)))
            membros_ids = random.sample(alunos_ids, num_membros)
            membros_str = '[' + ', '.join(map(str, membros_ids)) + ']'

            grupo_proj_inserts.append(
                f"INSERT INTO grupo_proj (id_grupo, id_professor, membros) VALUES ({id_grupo}, {id_professor_grupo}, {membros_str});"
            )
            grupo_counter += 1

    # Retorna todas as listas de comandos INSERT
    return (
        alunos_inserts,
        professores_inserts,
        final_departamentos_inserts, # Usa a lista atualizada com chefes
        alunos_formados_inserts,
        grupo_proj_inserts,
    )

# Função para salvar os comandos INSERT gerados em arquivos .cql separados
def save_to_cql_files(alunos, professores, departamentos, formados, grupos):
    # Função auxiliar para escrever em um arquivo
    def write_to_file(filename, queries):
        with open(filename, 'w', encoding='utf-8') as f:
            for query in queries:
                f.write(query + '\n')

    # Salva cada tipo de insert em seu respectivo arquivo
    write_to_file('1alunos.cql', alunos)
    write_to_file('1professores.cql', professores)
    write_to_file('1departamentos.cql', departamentos)
    write_to_file('1alunos_formados.cql', formados)
    write_to_file('1grupo_proj.cql', grupos)

# Bloco principal que executa ao rodar o script
# Gera os dados chamando a função principal
alunos, professores, departamentos, formados, grupos = generate_insert_statements()
# Salva os dados gerados nos arquivos .cql
save_to_cql_files(alunos, professores, departamentos, formados, grupos)
print("Files CQL foram gerados com sucesso") # Mensagem de sucesso
