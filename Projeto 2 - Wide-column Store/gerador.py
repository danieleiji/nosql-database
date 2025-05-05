import random
from faker import Faker

fake = Faker('pt_BR')

disciplinas = ["Cálculo I", "Álgebra Linear", "Complexidade de Algoritmo", "Computação Grafica", "CC6240", "Compilador",
                "Banco de Dados", "Redes de Computadores","Software orientado a objetos","Sistemas Operacionais"]

aluno_counter = 1
professor_counter = 1
departamento_counter = 1
grupo_counter = 1

# Listas para armazenar os IDs gerados
departamentos_ids = []
alunos_ids = []
professor_ids = []

def generate_insert_statements(num_alunos=75, num_professores=20, num_departamentos=10, num_alunos_formados=40, num_grupos=15):
    global aluno_counter, professor_counter, departamento_counter, grupo_counter

    alunos_inserts = []
    professores_inserts = []
    departamentos_inserts = []
    alunos_formados_inserts = []
    grupo_proj_inserts = []

    # --- Departamentos (Gerar primeiro para ter IDs disponíveis para professores) ---
    for _ in range(num_departamentos):
        id_departamento = departamento_counter
        departamentos_ids.append(id_departamento)
        # id_chefe_departamento será definido depois que os professores forem criados
        nome_departamento = fake.company()
        # Seleciona um número aleatório de disciplinas para o departamento
        num_disciplinas_dept = random.randint(1, 3)
        departamento_disciplinas = random.sample(disciplinas, num_disciplinas_dept)
        disciplinas_str = ', '.join([f"'{d}'" for d in departamento_disciplinas])
        # Adiciona um placeholder para id_chefe_departamento
        departamentos_inserts.append(
            (id_departamento, nome_departamento, disciplinas_str) # Tupla temporária
        )
        departamento_counter += 1

    # --- Professores ---
    for _ in range(num_professores):
        id_professor = professor_counter
        professor_ids.append(id_professor)
        nome = fake.name()
        # Garante que o departamento exista
        id_departamento = random.choice(departamentos_ids)
        disciplinas_ministradas = {}
        num_disciplinas_ministradas = random.randint(1, 4) # Prof pode ministrar mais de 1
        disciplinas_selecionadas = random.sample(disciplinas, num_disciplinas_ministradas)
        for disciplina in disciplinas_selecionadas:
            semestre = random.randint(1, 2)
            ano = random.randint(2018, 2024)
            disciplinas_ministradas[disciplina] = (semestre, ano)

        # Formata o mapa corretamente para CQL
        disciplinas_ministradas_str = '{' + ', '.join([f"'{k}': ({v[0]}, {v[1]})" for k, v in disciplinas_ministradas.items()]) + '}'

        professores_inserts.append(
            f"INSERT INTO professor (id_professor, nome, id_departamento, disciplinas_ministradas) "
            f"VALUES ({id_professor}, '{nome}', {id_departamento}, {disciplinas_ministradas_str});"
        )
        professor_counter += 1

    # --- Atualizar Departamentos com Chefes ---
    final_departamentos_inserts = []
    temp_professor_ids = professor_ids[:] # Copia para poder remover
    for id_dept, nome_dept, disciplinas_str_dept in departamentos_inserts:
         # Garante que o chefe seja um professor válido e único (se possível)
        if temp_professor_ids:
            id_chefe = random.choice(temp_professor_ids)
            temp_professor_ids.remove(id_chefe) # Evita chefe repetido se houver profs suficientes
        elif professor_ids: # Se não há mais únicos, repete
             id_chefe = random.choice(professor_ids)
        else:
            id_chefe = 0 # Placeholder se não houver professores

        final_departamentos_inserts.append(
            f"INSERT INTO departamento (id_departamento, nome, id_chefe_departamento, disciplinas) "
            f"VALUES ({id_dept}, '{nome_dept}', {id_chefe}, {{ {disciplinas_str_dept} }});"
        )


    # --- Alunos ---
    for _ in range(num_alunos):
        id_aluno = aluno_counter
        alunos_ids.append(id_aluno)
        nome = fake.name()
        # id_curso = random.randint(1, 5) # Se precisar de ID de curso
        # id_disciplina = random.randint(1, 10) # Se precisar de ID de disciplina

        disciplinas_concluidas = {}
        num_disciplinas_concluidas = random.randint(1, len(disciplinas))
        disciplinas_selecionadas = random.sample(disciplinas, num_disciplinas_concluidas)
        for disciplina in disciplinas_selecionadas:
            semestre = random.randint(1, 8)
            ano = random.randint(2018, 2024)
            nota = round(random.uniform(0, 10), 2)
            disciplinas_concluidas[disciplina] = (semestre, ano, nota)

        # Formata o mapa corretamente para CQL
        disciplinas_concluidas_str = '{' + ', '.join([f"'{k}': ({v[0]}, {v[1]}, {v[2]})" for k, v in disciplinas_concluidas.items()]) + '}'

        alunos_inserts.append(
            # f"INSERT INTO alunos (id_aluno, nome, id_curso, id_disciplina, disciplinas_concluidas) VALUES ({id_aluno}, '{nome}', {id_curso}, {id_disciplina}, {disciplinas_concluidas_str});" # Com IDs curso/disciplina
            f"INSERT INTO alunos (id_aluno, nome, disciplinas_concluidas) VALUES ({id_aluno}, '{nome}', {disciplinas_concluidas_str});" # Sem IDs curso/disciplina
        )
        aluno_counter += 1

    # --- Alunos Formados ---
    # Garante que alunos formados sejam um subconjunto dos alunos existentes
    alunos_formados_sample = random.sample(alunos_ids, min(num_alunos_formados, len(alunos_ids)))
    for id_aluno_formado in alunos_formados_sample:
        ano = random.randint(2020, 2024)
        semestre = random.randint(1, 2)
        # Precisamos buscar o nome do aluno? A tabela alunos_formado tem nome. Vamos gerar um novo nome ou buscar?
        # A query 3 só pede id e nome, então podemos gerar um nome aqui ou buscar na tabela alunos (requereria ler dados).
        # Vamos gerar um nome fake aqui para simplificar o gerador.
        nome_formado = fake.name() # Ou buscar o nome correspondente ao id_aluno_formado se necessário
        alunos_formados_inserts.append(
            f"INSERT INTO alunos_formado (ano, semestre, id_aluno, nome) VALUES ({ano}, {semestre}, {id_aluno_formado}, '{nome_formado}');"
        )

    # --- Grupo Proj ---
    # Garante que professores e alunos existam
    if professor_ids and len(alunos_ids) >= 2: # Precisa de pelo menos 1 prof e 2 alunos
        for _ in range(num_grupos):
            id_grupo = grupo_counter
            id_professor_grupo = random.choice(professor_ids)
            num_membros = random.randint(2, min(5, len(alunos_ids))) # Garante que não tente pegar mais alunos do que existem
            membros_ids = random.sample(alunos_ids, num_membros)
            membros_str = '[' + ', '.join(map(str, membros_ids)) + ']' # Converte IDs para string para o join

            grupo_proj_inserts.append(
                f"INSERT INTO grupo_proj (id_grupo, id_professor, membros) VALUES ({id_grupo}, {id_professor_grupo}, {membros_str});"
            )
            grupo_counter += 1

    return (
        alunos_inserts,
        professores_inserts,
        final_departamentos_inserts, # Usa a lista final com chefes
        alunos_formados_inserts,
        grupo_proj_inserts,
    )


def save_to_cql_files(alunos, professores, departamentos, formados, grupos):
    def write_to_file(filename, queries):
        with open(filename, 'w', encoding='utf-8') as f:
            for query in queries:
                f.write(query + '\n')

    write_to_file('1alunos.cql', alunos)
    write_to_file('1professores.cql', professores)
    write_to_file('1departamentos.cql', departamentos)
    write_to_file('1alunos_formados.cql', formados)
    write_to_file('1grupo_proj.cql', grupos)


alunos, professores, departamentos, formados, grupos = generate_insert_statements()
save_to_cql_files(alunos, professores, departamentos, formados, grupos)
