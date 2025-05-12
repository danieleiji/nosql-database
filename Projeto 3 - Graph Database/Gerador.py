import random
from faker import Faker

fake = Faker('pt_BR')

# --- Configurações Globais ---
NUM_ALUNOS = 60
NUM_PROFESSORES = 15
NUM_DEPARTAMENTOS = 5
NUM_MATRIZES = 3
NUM_TCCS = 10
NUM_ALUNOS_FORMADOS_APROX = NUM_ALUNOS // 2  # Aproximadamente metade dos alunos se formarão
MIN_DISC_POR_MATRIZ = 4
MAX_DISC_POR_MATRIZ = 7
MIN_ALUNOS_TCC = 2
MAX_ALUNOS_TCC = 4
ANOS = list(range(2020, 2025))  # Anos para atividades acadêmicas
SEMESTRES = [1, 2]
NOTA_APROVACAO = 4.0  # Nota mínima para aprovação em uma disciplina

# Anos/Semestres específicos para garantir que alguns alunos se formem nestes períodos para testes
ANOS_TESTE_FORMATURA = [2023, 2022]
SEMESTRES_TESTE_FORMATURA = [1, 2]

disciplinas_base_nomes = [
    "Cálculo I", "Álgebra Linear", "Algoritmos", "Computação Gráfica",
    "Autômatos", "Compiladores", "Banco de Dados", "Redes", "POO",
    "Sistemas Operacionais", "IA", "Eng. Software", "Estruturas de Dados"
]

# --- Estruturas de Dados e Contadores ---
id_counters = {
    "aluno": 1, "professor": 1, "disciplina_idx": 0,
    "departamento": 1, "matriz": 1, "tcc": 1
}
data_store = {
    "alunos": {}, "professores": {}, "disciplinas": {},
    "departamentos": {}, "matrizes": {}, "tccs": {}
}
cypher_nodes_cmds = []  # Comandos Cypher para criar nós
cypher_rels_cmds = []   # Comandos Cypher para criar relacionamentos

# Rastreia os pares (ano, semestre) de formaturas geradas para facilitar a criação de queries de exemplo
formaturas_geradas_para_exemplo = []

# --- Funções Auxiliares para Cypher ---
def format_prop_value(value):
    """Formata um valor para ser usado em uma propriedade Cypher."""
    if isinstance(value, str):
        return f"'{str(value).replace("'", "\\'")}'"
    return str(value)

def props_to_cypher_str(properties):
    """Converte um dicionário de propriedades para uma string Cypher."""
    return ", ".join(f"{k}: {format_prop_value(v)}" for k, v in properties.items())

def add_node(label, properties):
    """Adiciona um comando Cypher para criar um nó."""
    cypher_nodes_cmds.append(f"CREATE (:{label} {{{props_to_cypher_str(properties)}}});")

def add_rel(lbl_from, props_from, rel_type, rel_props, lbl_to, props_to):
    """Adiciona um comando Cypher para criar um relacionamento."""
    match_from = f"(a:{lbl_from} {{{props_to_cypher_str(props_from)}}})"
    match_to = f"(b:{lbl_to} {{{props_to_cypher_str(props_to)}}})"
    rel_props_str = f" {{{props_to_cypher_str(rel_props)}}}" if rel_props else ""
    cypher_rels_cmds.append(f"MATCH {match_from}, {match_to} CREATE (a)-[:{rel_type}{rel_props_str}]->(b);")

print("Iniciando a geração de dados para Neo4j...")

# --- 1. Geração de Nós ---
print("  Criando Nós...")

# Disciplinas
for nome_disc in disciplinas_base_nomes:
    id_counters["disciplina_idx"] += 1
    codigo = f"DISC{id_counters['disciplina_idx']:03d}"
    data_store["disciplinas"][codigo] = {'codigo_disciplina': codigo, 'nome_disciplina': nome_disc}
    add_node("Disciplina", data_store["disciplinas"][codigo])

# Outros tipos de nós (Alunos, Professores, Departamentos, Matrizes Curriculares, TCCs)
node_configs = [
    ("Aluno", NUM_ALUNOS, "alunos", "id_aluno", "nome_aluno", lambda: fake.name(), "aluno"),
    ("Professor", NUM_PROFESSORES, "professores", "id_professor", "nome_professor", lambda: fake.name(), "professor"),
    ("Departamento", NUM_DEPARTAMENTOS, "departamentos", "id_departamento", "nome_departamento", lambda: f"Depto. {fake.bs().split(' ')[0]}", "departamento"),
    ("MatrizCurricular", NUM_MATRIZES, "matrizes", "id_matriz", "nome_matriz", lambda: f"Matriz {fake.color_name()} {random.choice(ANOS)-2}", "matriz"),
    ("TCC", NUM_TCCS, "tccs", "id_tcc", "titulo_tcc", lambda: f"TCC: {fake.catch_phrase()}", "tcc")
]

for label, count, store_key, id_key_name, name_key_name, name_func, id_counter_key_cfg in node_configs:
    print(f"    Gerando {count} nós do tipo '{label}'...")
    for _ in range(count):
        current_id = id_counters[id_counter_key_cfg]
        data_store[store_key][current_id] = {id_key_name: current_id, name_key_name: name_func()}
        add_node(label, data_store[store_key][current_id])
        id_counters[id_counter_key_cfg] += 1

# --- 2. Geração de Relacionamentos ---
print("  Criando Relacionamentos...")
all_prof_ids = list(data_store["professores"].keys())
all_aluno_ids = list(data_store["alunos"].keys())
all_disc_cods = list(data_store["disciplinas"].keys())
all_matriz_ids = list(data_store["matrizes"].keys())
all_dept_ids = list(data_store["departamentos"].keys())
all_tcc_ids = list(data_store["tccs"].keys())

# Relacionamento: Professor CHEFE_DE Departamento
print("    Gerando relacionamentos CHEFE_DE...")
shuffled_prof_ids_for_chief = random.sample(all_prof_ids, k=min(len(all_prof_ids), len(all_dept_ids)))
for i, dept_id in enumerate(all_dept_ids):
    if i < len(shuffled_prof_ids_for_chief):
        add_rel("Professor", {'id_professor': shuffled_prof_ids_for_chief[i]},
                "CHEFE_DE", {},
                "Departamento", {'id_departamento': dept_id})

# Relacionamento: MatrizCurricular CONTEM_DISCIPLINA Disciplina
print("    Gerando relacionamentos CONTEM_DISCIPLINA...")
matriz_disciplinas_map = {} # Mapeia id_matriz para lista de cod_disciplina
for mat_id in all_matriz_ids:
    num_disc_na_matriz = random.randint(MIN_DISC_POR_MATRIZ, min(MAX_DISC_POR_MATRIZ, len(all_disc_cods)))
    disciplinas_para_matriz = random.sample(all_disc_cods, num_disc_na_matriz)
    matriz_disciplinas_map[mat_id] = disciplinas_para_matriz
    for cod_disc in disciplinas_para_matriz:
        add_rel("MatrizCurricular", {'id_matriz': mat_id},
                "CONTEM_DISCIPLINA", {},
                "Disciplina", {'codigo_disciplina': cod_disc})

# Relacionamento: Aluno CURSOU Disciplina
print("    Gerando relacionamentos CURSOU...")
alunos_aprovacoes = {al_id: {} for al_id in all_aluno_ids} # {id_aluno: {cod_disciplina: nota}}
alunos_max_ano_curso = {al_id: ANOS[0] -1 for al_id in all_aluno_ids} # Ano máximo que o aluno cursou algo

# Determina um subconjunto de alunos que serão candidatos à formatura (cursarão mais disciplinas)
alunos_candidatos_formatura = set(random.sample(all_aluno_ids, NUM_ALUNOS_FORMADOS_APROX))

for al_id in all_aluno_ids:
    if al_id in alunos_candidatos_formatura:
        # Candidatos à formatura cursam um número maior de disciplinas
        num_disciplinas_cursadas = random.randint(MIN_DISC_POR_MATRIZ, min(MAX_DISC_POR_MATRIZ + 2, len(all_disc_cods)))
    else:
        # Outros alunos cursam menos
        num_disciplinas_cursadas = random.randint(max(1, len(all_disc_cods) // 5), max(2, len(all_disc_cods) // 3))

    disciplinas_cursadas_pelo_aluno = random.sample(all_disc_cods, num_disciplinas_cursadas)
    for cod_disc in disciplinas_cursadas_pelo_aluno:
        # Garante que o ano cursado não seja o último ano da lista (para permitir formatura posterior)
        ano_cursado = random.choice(ANOS[:-1]) if len(ANOS) > 1 else ANOS[0]
        semestre_cursado = random.choice(SEMESTRES)
        nota = round(random.uniform(0.0, 10.0), 1)

        props_cursou = {'semestre': semestre_cursado, 'ano': ano_cursado, 'nota_final': nota}
        add_rel("Aluno", {'id_aluno': al_id}, "CURSOU", props_cursou, "Disciplina", {'codigo_disciplina': cod_disc})

        if ano_cursado > alunos_max_ano_curso[al_id]:
            alunos_max_ano_curso[al_id] = ano_cursado
        if nota >= NOTA_APROVACAO:
            alunos_aprovacoes[al_id][cod_disc] = nota

# Relacionamento: Aluno FORMADO_EM MatrizCurricular
print("    Gerando relacionamentos FORMADO_EM...")
shuffled_aluno_ids_para_formar = list(alunos_candidatos_formatura)
random.shuffle(shuffled_aluno_ids_para_formar)
formados_count = 0
alunos_ja_formados_ids = set()

# Prioriza anos/semestres de teste para formatura, depois outros anos
anos_para_formar_prioridade = ANOS_TESTE_FORMATURA + [y for y in ANOS if y not in ANOS_TESTE_FORMATURA]

for al_id in shuffled_aluno_ids_para_formar:
    if al_id in alunos_ja_formados_ids or formados_count >= NUM_ALUNOS_FORMADOS_APROX :
        continue # Aluno já formado ou já atingimos o número desejado de formados

    for mat_id, disciplinas_da_matriz in matriz_disciplinas_map.items():
        # Verifica se o aluno foi aprovado em todas as disciplinas da matriz curricular
        if all(cod_d in alunos_aprovacoes[al_id] for cod_d in disciplinas_da_matriz):
            # Determina o ano e semestre de formatura
            # O aluno deve se formar, no mínimo, no ano seguinte ao último ano em que cursou alguma disciplina
            ano_formacao_possivel = max(alunos_max_ano_curso[al_id] + 1, ANOS[0])
            
            ano_formacao_final = None
            semestre_formacao_final = None

            # Tenta encaixar a formatura nos anos/semestres de teste primeiro
            # Distribui uma parte dos formados nos períodos de teste
            alunos_por_periodo_teste = (NUM_ALUNOS_FORMADOS_APROX // (len(ANOS_TESTE_FORMATURA) * len(SEMESTRES_TESTE_FORMATURA) or 1)) // 2 or 1
            if formados_count < len(ANOS_TESTE_FORMATURA) * len(SEMESTRES_TESTE_FORMATURA) * alunos_por_periodo_teste:
                for ano_teste in ANOS_TESTE_FORMATURA:
                    if ano_teste >= ano_formacao_possivel:
                        for sem_teste in SEMESTRES_TESTE_FORMATURA:
                             # Verifica se já não colocamos muitos formados neste período específico
                            chave_periodo = (ano_teste, sem_teste)
                            if formaturas_geradas_para_exemplo.count(chave_periodo) < alunos_por_periodo_teste + 1:
                                ano_formacao_final = ano_teste
                                semestre_formacao_final = sem_teste
                                break
                    if ano_formacao_final:
                        break
            
            # Se não encaixou nos períodos de teste ou já passou dessa fase, escolhe outros períodos
            if ano_formacao_final is None:
                anos_validos_formacao = [y for y in anos_para_formar_prioridade if y >= ano_formacao_possivel and y <= ANOS[-1]]
                if not anos_validos_formacao: # Se o aluno cursou disciplinas muito tarde
                    ano_formacao_final = ANOS[-1] # Forma no último ano disponível
                else:
                    ano_formacao_final = random.choice(anos_validos_formacao)
                semestre_formacao_final = random.choice(SEMESTRES)

            props_formado = {'semestre_formacao': semestre_formacao_final, 'ano_formacao': ano_formacao_final}
            add_rel("Aluno", {'id_aluno': al_id}, "FORMADO_EM", props_formado, "MatrizCurricular", {'id_matriz': mat_id})
            
            formaturas_geradas_para_exemplo.append((ano_formacao_final, semestre_formacao_final))
            alunos_ja_formados_ids.add(al_id)
            formados_count += 1
            break # Aluno se forma em uma matriz curricular e não precisa verificar outras

# Relacionamento: Professor MINISTROU Disciplina
print("    Gerando relacionamentos MINISTROU...")
for prof_id in all_prof_ids:
    num_disciplinas_ministradas = random.randint(1, max(1, len(all_disc_cods) // 3))
    disciplinas_para_ministrar = random.sample(all_disc_cods, num_disciplinas_ministradas)
    for cod_disc in disciplinas_para_ministrar:
        add_rel("Professor", {'id_professor': prof_id}, "MINISTROU",
                {'semestre': random.choice(SEMESTRES), 'ano': random.choice(ANOS)},
                "Disciplina", {'codigo_disciplina': cod_disc})

# Relacionamentos de TCC: Professor ORIENTA TCC e Aluno PARTICIPA_DE TCC
print("    Gerando relacionamentos de TCC (ORIENTA, PARTICIPA_DE)...")
for tcc_id in all_tcc_ids:
    # Escolhe um professor orientador
    orientador_id = random.choice(all_prof_ids)
    add_rel("Professor", {'id_professor': orientador_id}, "ORIENTA", {}, "TCC", {'id_tcc': tcc_id})

    # Escolhe alunos para o grupo do TCC
    num_alunos_no_grupo = random.randint(MIN_ALUNOS_TCC, MAX_ALUNOS_TCC)
    # Garante que não tentamos pegar mais alunos do que o disponível e que não estão já em TCCs demais (simplificado aqui)
    alunos_disponiveis_para_tcc = random.sample(all_aluno_ids, min(num_alunos_no_grupo, len(all_aluno_ids)))
    for aluno_id_tcc in alunos_disponiveis_para_tcc:
        add_rel("Aluno", {'id_aluno': aluno_id_tcc}, "PARTICIPA_DE", {}, "TCC", {'id_tcc': tcc_id})

# --- 3. Escrever Arquivos Cypher ---
print("  Escrevendo arquivos Cypher...")
output_filenames = {"nodes": "nodes.cypher", "relationships": "relationships.cypher"}

# Arquivo de Nós (nodes.cypher)
with open(output_filenames["nodes"], "w", encoding="utf-8") as f:
    f.write("MATCH (n) DETACH DELETE n;\n\n") # Limpa o banco de dados (CUIDADO!)
    
    # Constraints e Índices para otimizar consultas e garantir unicidade
    constraints_indices = [
        "CREATE CONSTRAINT IF NOT EXISTS FOR (a:Aluno) REQUIRE a.id_aluno IS UNIQUE;",
        "CREATE INDEX IF NOT EXISTS FOR (a:Aluno) ON (a.nome_aluno);",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Professor) REQUIRE p.id_professor IS UNIQUE;",
        "CREATE INDEX IF NOT EXISTS FOR (p:Professor) ON (p.nome_professor);",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (d:Disciplina) REQUIRE d.codigo_disciplina IS UNIQUE;",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (dp:Departamento) REQUIRE dp.id_departamento IS UNIQUE;",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (m:MatrizCurricular) REQUIRE m.id_matriz IS UNIQUE;",
        "CREATE CONSTRAINT IF NOT EXISTS FOR (t:TCC) REQUIRE t.id_tcc IS UNIQUE;"
    ]
    f.write("// Constraints e Índices\n")
    f.write("\n".join(constraints_indices))
    f.write("\n\n// Criação de Nós\n")
    f.write("\n".join(cypher_nodes_cmds))
print(f"Arquivo '{output_filenames['nodes']}' gerado com {len(cypher_nodes_cmds)} comandos de criação de nós.")

# Arquivo de Relacionamentos (relationships.cypher)
with open(output_filenames["relationships"], "w", encoding="utf-8") as f:
    f.write("// Criação de Relacionamentos\n")
    f.write("\n".join(cypher_rels_cmds))
print(f"Arquivo '{output_filenames['relationships']}' gerado com {len(cypher_rels_cmds)} comandos de criação de relacionamentos.")

print("\nProcesso de geração de dados concluído!")
if formaturas_geradas_para_exemplo:
    print("\nAlguns exemplos de períodos de formatura gerados (ano, semestre):")
    unique_formaturas = sorted(list(set(formaturas_geradas_para_exemplo)))
    for i, (ano, sem) in enumerate(unique_formaturas):
        if i < 5 or (ano in ANOS_TESTE_FORMATURA and sem in SEMESTRES_TESTE_FORMATURA): # Mostra alguns ou os de teste
             print(f"  Ano: {ano}, Semestre: {sem}")
        elif i == 5 and len(unique_formaturas) > 7:
            print("  ...") # Indica que há mais
    if not any(af in ANOS_TESTE_FORMATURA for af, asem in unique_formaturas):
        print("  Atenção: Pode ser que nenhum aluno tenha se formado nos ANOS_TESTE_FORMATURA especificados nesta execução.")
else:
    print("\nNenhum aluno se formou nesta execução com base nos critérios.")