import random
from faker import Faker

fake = Faker('pt_BR')

# --- Configurações ---
NUM_ALUNOS = 75
NUM_PROFESSORES = 20
NUM_DEPARTAMENTOS = 5
NUM_MATRIZES = 3
NUM_TCCS = 15
NUM_ALUNOS_FORMADOS_APROX = NUM_ALUNOS // 3

MIN_DISC_POR_MATRIZ = 4
MAX_DISC_POR_MATRIZ = 7
MIN_ALUNOS_TCC = 2
MAX_ALUNOS_TCC = 4
ANOS = list(range(2020, 2025))
SEMESTRES = [1, 2]
NOTA_APROVACAO = 7.0

disciplinas_base_nomes = [
    "Cálculo I", "Álgebra Linear", "Algoritmos", "Computação Gráfica",
    "Autômatos", "Compiladores", "Banco de Dados", "Redes", "POO",
    "Sistemas Operacionais", "IA", "Eng. Software", "Estruturas de Dados"
]

# Contadores de ID e Armazenamento de Dados
id_counters = {"aluno": 1, "professor": 1, "disciplina_idx": 0, "departamento": 1, "matriz": 1, "tcc": 1}
data_store = {
    "alunos": {}, "professores": {}, "disciplinas": {},
    "departamentos": {}, "matrizes": {}, "tccs": {}
}
cypher_nodes_cmds, cypher_rels_cmds = [], []

# --- Funções Auxiliares ---
def format_prop_value(value):
    return f"'{str(value).replace("'", "\\'")}'" if isinstance(value, str) else str(value)

def props_to_cypher_str(properties):
    return ", ".join(f"{k}: {format_prop_value(v)}" for k, v in properties.items())

def add_node(label, properties):
    cypher_nodes_cmds.append(f"CREATE (:{label} {{{props_to_cypher_str(properties)}}});")

def add_rel(lbl_from, props_from, rel_type, rel_props, lbl_to, props_to):
    match_from = f"(a:{lbl_from} {{{props_to_cypher_str(props_from)}}})"
    match_to = f"(b:{lbl_to} {{{props_to_cypher_str(props_to)}}})"
    rel_props_str = f" {{{props_to_cypher_str(rel_props)}}}" if rel_props else ""
    cypher_rels_cmds.append(f"MATCH {match_from}, {match_to} CREATE (a)-[:{rel_type}{rel_props_str}]->(b);")

print("Gerando dados para Neo4j...")

# --- 1. Geração de Nós ---
print("  Criando Nós...")
for nome_disc in disciplinas_base_nomes:
    id_counters["disciplina_idx"] += 1
    codigo = f"DISC{id_counters['disciplina_idx']:03d}"
    data_store["disciplinas"][codigo] = {'codigo_disciplina': codigo, 'nome_disciplina': nome_disc}
    add_node("Disciplina", data_store["disciplinas"][codigo])

node_configs = [
    # label,           count,             store_key,       id_key_name,        name_key_name,      name_func,                                      id_counter_key
    ("Aluno",          NUM_ALUNOS,        "alunos",        "id_aluno",         "nome_aluno",       lambda: fake.name(),                            "aluno"),
    ("Professor",      NUM_PROFESSORES,   "professores",   "id_professor",     "nome_professor",   lambda: fake.name(),                            "professor"),
    ("Departamento",   NUM_DEPARTAMENTOS, "departamentos", "id_departamento",  "nome_departamento",lambda: f"Depto. {fake.bs().split(' ')[0]}", "departamento"),
    ("MatrizCurricular",NUM_MATRIZES,      "matrizes",      "id_matriz",        "nome_matriz",      lambda: f"Matriz {fake.color_name()} {random.choice(ANOS)-2}", "matriz"),
    ("TCC",            NUM_TCCS,          "tccs",          "id_tcc",           "titulo_tcc",       lambda: f"TCC: {fake.catch_phrase()}",       "tcc")
]
for label, count, store_key, id_key_name, name_key_name, name_func, id_counter_key_cfg in node_configs:
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

# CHEFE_DE
shuffled_prof_ids = random.sample(all_prof_ids, k=min(len(all_prof_ids), len(data_store["departamentos"])))
for i, dept_id in enumerate(data_store["departamentos"].keys()):
    if i < len(shuffled_prof_ids):
        add_rel("Professor", {'id_professor': shuffled_prof_ids[i]}, "CHEFE_DE", {}, "Departamento", {'id_departamento': dept_id})

# Matriz CONTEM_DISCIPLINA
matriz_disciplinas_map = {}
for mat_id in data_store["matrizes"].keys():
    num_disc = random.randint(MIN_DISC_POR_MATRIZ, min(MAX_DISC_POR_MATRIZ, len(all_disc_cods)))
    matriz_disciplinas_map[mat_id] = random.sample(all_disc_cods, num_disc)
    for cod_disc in matriz_disciplinas_map[mat_id]:
        add_rel("MatrizCurricular", {'id_matriz': mat_id}, "CONTEM_DISCIPLINA", {}, "Disciplina", {'codigo_disciplina': cod_disc})

# Aluno CURSOU Disciplina
alunos_aprovacoes = {al_id: {} for al_id in all_aluno_ids}
for al_id in all_aluno_ids:
    num_cursadas = random.randint(max(1, len(all_disc_cods) // 4), max(2, len(all_disc_cods) // 3)) # MODIFICADO
    for cod_disc in random.sample(all_disc_cods, num_cursadas):
        nota = round(random.uniform(0.0, 10.0), 1)
        props_cursou = {'semestre': random.choice(SEMESTRES), 'ano': random.choice(ANOS), 'nota_final': nota}
        add_rel("Aluno", {'id_aluno': al_id}, "CURSOU", props_cursou, "Disciplina", {'codigo_disciplina': cod_disc})
        if nota >= NOTA_APROVACAO:
            alunos_aprovacoes[al_id][cod_disc] = nota

# Aluno FORMADO_EM MatrizCurricular
shuffled_aluno_ids = random.sample(all_aluno_ids, len(all_aluno_ids))
formados_count = 0
for al_id in shuffled_aluno_ids:
    if formados_count >= NUM_ALUNOS_FORMADOS_APROX: break
    for mat_id, disc_matriz in matriz_disciplinas_map.items():
        if all(cod_d in alunos_aprovacoes[al_id] for cod_d in disc_matriz):
            props_formado = {'semestre_formacao': random.choice(SEMESTRES), 'ano_formacao': random.choice(ANOS[-2:])}
            add_rel("Aluno", {'id_aluno': al_id}, "FORMADO_EM", props_formado, "MatrizCurricular", {'id_matriz': mat_id})
            formados_count += 1
            break

# Professor MINISTROU Disciplina
for prof_id in all_prof_ids:
    num_minist = random.randint(1, max(1, len(all_disc_cods) // 3))
    for cod_disc in random.sample(all_disc_cods, num_minist):
        add_rel("Professor", {'id_professor': prof_id}, "MINISTROU",
                {'semestre': random.choice(SEMESTRES), 'ano': random.choice(ANOS)},
                "Disciplina", {'codigo_disciplina': cod_disc})

# TCCs: Aluno PARTICIPA_DE e Professor ORIENTA
for tcc_id in data_store["tccs"].keys():
    orient_id = random.choice(all_prof_ids)
    add_rel("Professor", {'id_professor': orient_id}, "ORIENTA", {}, "TCC", {'id_tcc': tcc_id})

    num_alunos_grupo = random.randint(MIN_ALUNOS_TCC, MAX_ALUNOS_TCC)
    alunos_grupo = random.sample(all_aluno_ids, min(num_alunos_grupo, len(all_aluno_ids)))
    for al_id_tcc in alunos_grupo:
        add_rel("Aluno", {'id_aluno': al_id_tcc}, "PARTICIPA_DE", {}, "TCC", {'id_tcc': tcc_id})

# --- 3. Escrever Arquivos Cypher ---
output_filenames = {"nodes": "nodes.cypher", "relationships": "relationships.cypher", "queries": "queries.cypher"}

with open(output_filenames["nodes"], "w", encoding="utf-8") as f:
    f.write("MATCH (n) DETACH DELETE n;\n\n")
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
    f.write("// Constraints e Índices\n" + "\n".join(constraints_indices) + "\n\n// Criação de Nós\n")
    f.write("\n".join(cypher_nodes_cmds))
print(f"Arquivo '{output_filenames['nodes']}' gerado com {len(cypher_nodes_cmds)} comandos de nós.")

with open(output_filenames["relationships"], "w", encoding="utf-8") as f:
    f.write("// Criação de Relacionamentos\n" + "\n".join(cypher_rels_cmds))
print(f"Arquivo '{output_filenames['relationships']}' gerado com {len(cypher_rels_cmds)} comandos de relacionamentos.")

ex_al_id = random.choice(all_aluno_ids) if all_aluno_ids else 1
ex_prof_id = random.choice(all_prof_ids) if all_prof_ids else 1
ex_ano, ex_sem = random.choice(ANOS[-2:]), random.choice(SEMESTRES)

queries_texto = f"""\
// 1. Histórico escolar do aluno ID {ex_al_id}
MATCH (a:Aluno {{id_aluno: {ex_al_id}}})-[r:CURSOU]->(d:Disciplina)
RETURN d.codigo_disciplina, d.nome_disciplina, r.semestre, r.ano, r.nota_final ORDER BY r.ano, r.semestre;

// 2. Disciplinas ministradas pelo professor ID {ex_prof_id}
MATCH (p:Professor {{id_professor: {ex_prof_id}}})-[r:MINISTROU]->(d:Disciplina)
RETURN d.nome_disciplina, r.semestre, r.ano ORDER BY r.ano, r.semestre;

// 3. Alunos formados em {ex_sem}/{ex_ano}
MATCH (a:Aluno)-[f:FORMADO_EM {{semestre_formacao: {ex_sem}, ano_formacao: {ex_ano}}}]->(m:MatrizCurricular)
RETURN a.id_aluno, a.nome_aluno, m.nome_matriz ORDER BY a.nome_aluno;

// 4. Professores chefes de departamento
MATCH (p:Professor)-[:CHEFE_DE]->(d:Departamento)
RETURN p.id_professor, p.nome_professor, d.nome_departamento ORDER BY d.nome_departamento;

// 5. Grupos de TCC e orientadores
MATCH (al:Aluno)-[:PARTICIPA_DE]->(tcc:TCC)<-[:ORIENTA]-(prof:Professor)
RETURN tcc.id_tcc, tcc.titulo_tcc, prof.nome_professor AS orientador, collect({{id: al.id_aluno, nome: al.nome_aluno}}) AS grupo_alunos
ORDER BY tcc.id_tcc;
"""
with open(output_filenames["queries"], "w", encoding="utf-8") as f:
    f.write(queries_texto)
print(f"Arquivo '{output_filenames['queries']}' gerado.")
print("\nProcesso de geração concluído!")