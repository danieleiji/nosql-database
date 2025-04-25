# --- START OF FILE Gerador.py ---

import json
import random
from faker import Faker
import datetime
import os
import math

# --- Configurações ---
NUM_ALUNOS = 100
NUM_PROFESSORES = 15
NUM_CURSOS = 8
NUM_DEPARTAMENTOS = 5
NUM_DISCIPLINAS = 20
NUM_GRUPOS_TCC = 8

# --- Inicialização ---
fake = Faker('pt_BR')
alunos, professores, cursos, departamentos, disciplinas, grupos_tcc = [], [], [], [], [], []
departamentos_ids, cursos_ids, disciplinas_ids, professores_ids, alunos_ids = [], [], [], [], []
disciplina_map = {}
disciplinas_por_curso = {}
codigos_disciplinas_usados = set()
dept_code_map = {}

# --- Helpers ---
def gerar_semestre(ano_inicio=2020, ano_fim=None):
    if ano_fim is None:
        ano_fim = datetime.datetime.now().year
    ano_fim = max(ano_inicio, ano_fim)
    ano = random.randint(ano_inicio, ano_fim)
    semestre = random.choice([1, 2])
    return f"{ano}.{semestre}"

def parse_semestre(semestre_str):
    try:
        ano, sem = map(int, semestre_str.split('.'))
        return ano, sem
    except:
        return 0, 0 # Fallback for invalid format

dept_codes_pool = ["INF", "MAT", "FIS", "QUI", "BIO", "LET", "HIS", "ECO", "ENG", "ADM"]
dept_nomes_base = ["Informática", "Matemática", "Física", "Química", "Biologia", "Letras", "História", "Economia", "Engenharia", "Administração"]
if len(dept_nomes_base) < NUM_DEPARTAMENTOS:
     dept_nomes_base.extend([f"Área {chr(65+i)}" for i in range(NUM_DEPARTAMENTOS - len(dept_nomes_base))])
dept_code_name_map = {code: name for code, name in zip(dept_codes_pool[:NUM_DEPARTAMENTOS], dept_nomes_base[:NUM_DEPARTAMENTOS])}

core_discipline_subjects = ["Algoritmos", "Cálculo", "Física", "Química", "Biologia", "Literatura", "História", "Economia", "Redes", "Banco de Dados", "Inteligência Artificial", "Engenharia de Software", "Sistemas Operacionais", "Estrutura de Dados", "Mecânica", "Eletromagnetismo"]
simple_modifiers = ["Básica", "Avançada", "I", "II", "Aplicada", "Experimental", "Computacional"]

# --- Geração de Dados ---

# 1. Departamentos
for i in range(NUM_DEPARTAMENTOS):
    dep_id = i + 1
    dep_code = dept_codes_pool[i]
    dep_nome = dept_code_name_map.get(dep_code, f"Departamento Genérico {i+1}")
    departamentos.append({
        "_id": dep_id,
        "nome": f"Departamento de {dep_nome}",
        "codigo_dept": dep_code,
        "chefe_id": None
    })
    departamentos_ids.append(dep_id)
    dept_code_map[dep_id] = dep_code

# 2. Cursos
for i in range(NUM_CURSOS):
    curso_id = i + 1
    dep_id_curso = random.choice(departamentos_ids) if departamentos_ids else None
    nome_base_curso = random.choice(core_discipline_subjects)
    curso = {
        "_id": curso_id,
        "nome": f"Graduação em {nome_base_curso}",
        "departamento_id": dep_id_curso,
        "disciplinas_ids": []
    }
    cursos.append(curso)
    cursos_ids.append(curso_id)
    if dep_id_curso is not None:
        disciplinas_por_curso[curso_id] = []

# 3. Disciplinas
for i in range(NUM_DISCIPLINAS):
    disciplina_id = i + 1
    nome_base = random.choice(core_discipline_subjects)
    if random.random() < 0.5:
        nome_disciplina = f"{nome_base} {random.choice(simple_modifiers)}"
    else:
        nome_disciplina = nome_base

    curso_associado = random.choice(cursos) if cursos else None
    dept_id_disciplina = curso_associado['departamento_id'] if curso_associado and curso_associado.get('departamento_id') is not None else random.choice(departamentos_ids) if departamentos_ids else None
    prefixo_codigo = dept_code_map.get(dept_id_disciplina, "GEN") if dept_id_disciplina else "GEN"

    codigo_disciplina = None
    tentativas_codigo = 0
    while tentativas_codigo < 50:
        codigo_tentativa = f"{prefixo_codigo}{random.randint(100, 699)}"
        if codigo_tentativa not in codigos_disciplinas_usados:
            codigo_disciplina = codigo_tentativa
            codigos_disciplinas_usados.add(codigo_disciplina)
            break
        tentativas_codigo += 1
    if not codigo_disciplina:
         codigo_disciplina = f"DIS{disciplina_id:03d}"
         codigos_disciplinas_usados.add(codigo_disciplina)

    disciplina = {
        "_id": disciplina_id,
        "codigo": codigo_disciplina,
        "nome": nome_disciplina,
    }
    disciplinas.append(disciplina)
    disciplinas_ids.append(disciplina_id)
    disciplina_map[disciplina_id] = {"codigo": disciplina["codigo"], "nome": disciplina["nome"]}

    if curso_associado and curso_associado["_id"] in disciplinas_por_curso:
         disciplinas_por_curso[curso_associado["_id"]].append(disciplina_id)

# 3.1 Atualiza Cursos com suas listas de disciplinas
for curso in cursos:
    curso_id = curso["_id"]
    if curso_id in disciplinas_por_curso:
        disciplinas_base = disciplinas_por_curso[curso_id]
        min_disciplinas_curso = max(1, NUM_DISCIPLINAS // NUM_CURSOS - 2 if NUM_CURSOS > 0 else 1)
        num_a_adicionar = min_disciplinas_curso - len(disciplinas_base)

        disciplinas_disponiveis = [d_id for d_id in disciplinas_ids if d_id not in disciplinas_base]
        random.shuffle(disciplinas_disponiveis)
        if num_a_adicionar > 0 and disciplinas_disponiveis:
            disciplinas_base.extend(disciplinas_disponiveis[:min(num_a_adicionar, len(disciplinas_disponiveis))])

        num_eletivas = random.randint(0, 3)
        disciplinas_disponiveis_eletivas = [d_id for d_id in disciplinas_ids if d_id not in disciplinas_base]
        random.shuffle(disciplinas_disponiveis_eletivas)
        if num_eletivas > 0 and disciplinas_disponiveis_eletivas:
             disciplinas_base.extend(disciplinas_disponiveis_eletivas[:min(num_eletivas, len(disciplinas_disponiveis_eletivas))])

        curso["disciplinas_ids"] = list(set(disciplinas_base))

# 4. Professores
professores_disponiveis_chefia = list(range(1, NUM_PROFESSORES + 1))
random.shuffle(professores_disponiveis_chefia)

for i in range(NUM_PROFESSORES):
    prof_id = i + 1
    professor = {
        "_id": prof_id,
        "nome": fake.name(),
        "departamento_id": random.choice(departamentos_ids) if departamentos_ids else None,
        "eh_chefe": False,
        "disciplinas_ministradas": []
    }
    professores.append(professor)
    professores_ids.append(prof_id)

# 4.1 Define Chefes de Departamento
departamentos_sem_chefe = list(departamentos_ids)
random.shuffle(departamentos_sem_chefe)
chefes_definidos = 0
for prof_id_chefe in professores_disponiveis_chefia:
    if not departamentos_sem_chefe: break
    dep_id_para_chefiar = departamentos_sem_chefe.pop()
    for dep in departamentos:
        if dep["_id"] == dep_id_para_chefiar:
            dep["chefe_id"] = prof_id_chefe
            break
    for prof in professores:
        if prof["_id"] == prof_id_chefe:
            prof["eh_chefe"] = True
            prof["departamento_id"] = dep_id_para_chefiar
            chefes_definidos += 1
            break

# 4.2 Gera Histórico de Disciplinas Ministradas
if disciplinas_ids and professores:
    for prof in professores:
        num_disciplinas_ministradas_hist = random.randint(2, 5) # *** Limitado conforme sugestão (era 2 a 8) ***
        disciplinas_ja_ministradas_semestre = set()

        disciplinas_dept = []
        if prof["departamento_id"]:
             dept_code_prof = dept_code_map.get(prof["departamento_id"])
             if dept_code_prof:
                 for disc_id, disc_info in disciplina_map.items():
                      if disc_info['codigo'].startswith(dept_code_prof):
                          disciplinas_dept.append(disc_id)

        disciplinas_candidatas = disciplinas_dept + [d for d in disciplinas_ids if d not in disciplinas_dept]
        if not disciplinas_candidatas: continue

        for _ in range(num_disciplinas_ministradas_hist):
            if not disciplinas_candidatas: break
            disciplina_id = random.choice(disciplinas_candidatas)
            semestre = gerar_semestre(2021)
            chave_unica = (disciplina_id, semestre)

            if chave_unica not in disciplinas_ja_ministradas_semestre:
                prof["disciplinas_ministradas"].append({
                    "disciplina_id": disciplina_id,
                    "semestre": semestre,
                    "ano": int(semestre.split('.')[0])
                })
                disciplinas_ja_ministradas_semestre.add(chave_unica)
else:
    if not disciplinas_ids: print("   AVISO: Não há disciplinas para gerar histórico de professores.")
    if not professores: print("   AVISO: Não há professores para gerar histórico.")


# 5. Alunos e Histórico Escolar (com verificação de graduação integrada)
alunos_graduados_count = 0
for i in range(NUM_ALUNOS):
    aluno_id = i + 1
    curso_id_aluno = random.choice(cursos_ids) if cursos_ids else None

    aluno = {
        "_id": aluno_id,
        "nome": fake.name(),
        "curso_id": curso_id_aluno,
        "historico": [],
        "graduado": False,
        "semestre_graduacao": None
    }

    disciplinas_aprovadas_neste_aluno = set()
    if disciplinas_ids and curso_id_aluno:
        # Define quantas disciplinas do catalogo geral o aluno vai cursar
        # Continua pegando uma boa parte para ter chance de completar a matriz
        num_disciplinas_a_cursar = random.randint(math.ceil(NUM_DISCIPLINAS * 0.5), NUM_DISCIPLINAS)
        disciplinas_para_historico_ids = random.sample(disciplinas_ids, min(num_disciplinas_a_cursar, len(disciplinas_ids)))

        ultimo_ano_cursado = 2020
        ultimo_semestre_num = 0

        # Gera o histórico do aluno
        for disc_id in disciplinas_para_historico_ids:
            # Lógica simples para avanço de semestre/ano
            if ultimo_semestre_num == 2:
                ano_cursado = ultimo_ano_cursado + 1
                semestre_num = 1
            elif ultimo_semestre_num == 1:
                 ano_cursado = ultimo_ano_cursado
                 semestre_num = 2
            else: # Primeiro semestre
                 ano_cursado = ultimo_ano_cursado + random.randint(0,1) # Pode começar em 2020 ou 2021
                 semestre_num = random.choice([1, 2])


            semestre_cursado = f"{ano_cursado}.{semestre_num}"
            ultimo_ano_cursado = ano_cursado
            ultimo_semestre_num = semestre_num

            nota = round(random.uniform(2.0, 10.0), 1) # Nota pode ser baixa
            # *** MUDANÇA PRINCIPAL: Nota de corte 4.0 ***
            status = "Aprovado" if nota >= 4.0 else "Reprovado"
            disciplina_info = disciplina_map.get(disc_id)

            if disciplina_info:
                aluno["historico"].append({
                    "codigo": disciplina_info["codigo"],
                    "nome": disciplina_info["nome"],
                    "semestre": semestre_cursado,
                    "ano": ano_cursado,
                    "nota_final": nota,
                    "status": status
                })
                if status == "Aprovado":
                    disciplinas_aprovadas_neste_aluno.add(disc_id)

        # Verifica graduação após gerar histórico completo
        matriz_curso_ids = set()
        curso_encontrado = False
        for c in cursos:
            if c["_id"] == curso_id_aluno:
                matriz_curso_ids = set(c.get("disciplinas_ids", []))
                curso_encontrado = True
                break

        # Graduado se aprovado em TODAS as disciplinas da matriz do seu curso
        # A lógica de verificação continua a mesma, mas a chance de status="Aprovado" aumentou
        if curso_encontrado and matriz_curso_ids and matriz_curso_ids.issubset(disciplinas_aprovadas_neste_aluno):
             aluno["graduado"] = True
             alunos_graduados_count += 1
             # Encontra o último semestre cursado no histórico para ser o semestre de graduação
             if aluno["historico"]:
                 try:
                     # Encontra o registro com o maior semestre/ano
                     ultimo_registro = max(aluno["historico"], key=lambda x: parse_semestre(x.get("semestre", "0.0")))
                     aluno["semestre_graduacao"] = ultimo_registro.get("semestre")
                 except (ValueError, TypeError):
                      aluno["semestre_graduacao"] = None # Caso de erro no formato do semestre
                      aluno["graduado"] = False # Não pode graduar sem semestre válido
                      if alunos_graduados_count > 0: # Garante que não fique negativo
                          alunos_graduados_count -= 1


    alunos.append(aluno)
    alunos_ids.append(aluno_id)


# 6. Grupos de TCC
alunos_disponiveis_tcc = list(alunos_ids)
random.shuffle(alunos_disponiveis_tcc)
professores_disponiveis_tcc = list(professores_ids)
random.shuffle(professores_disponiveis_tcc)
grupos_gerados = 0

for i in range(NUM_GRUPOS_TCC):
    if not professores_disponiveis_tcc:
        print("   AVISO: Não há mais professores disponíveis para orientação de TCC.")
        break
    min_alunos_grupo = 2
    if len(alunos_disponiveis_tcc) < min_alunos_grupo:
        print("   AVISO: Não há alunos suficientes disponíveis para formar mais grupos de TCC.")
        break

    grupo_id = i + 1
    orientador_id = random.choice(professores_disponiveis_tcc)

    max_alunos_grupo = 4
    num_alunos_grupo = random.randint(min_alunos_grupo, min(max_alunos_grupo, len(alunos_disponiveis_tcc)))
    alunos_grupo_ids = [alunos_disponiveis_tcc.pop() for _ in range(num_alunos_grupo)]

    grupo = {
        "_id": grupo_id,
        "orientador_id": orientador_id,
        "alunos_ids": alunos_grupo_ids,
        "semestre": gerar_semestre(datetime.datetime.now().year - 1) # TCC em semestre recente
    }
    grupos_tcc.append(grupo)
    grupos_gerados += 1


# --- Salvar em arquivos JSON ---
def salvar_json(data, filename):
    filepath = filename
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"   Arquivo salvo: {filepath}") # MANTIDO
    except IOError as e:
        print(f"   ERRO ao salvar {filepath}: {e}") # MANTIDO (Erro)
    except TypeError as e:
         print(f"   ERRO de tipo ao serializar {filepath}: {e}") # MANTIDO (Erro)

print("\nSalvando arquivos JSON...") # MANTIDO
salvar_json(departamentos, "departamentos.json")
salvar_json(cursos, "cursos.json")
salvar_json(disciplinas, "disciplinas.json")
salvar_json(professores, "professores.json")
salvar_json(alunos, "alunos.json")
salvar_json(grupos_tcc, "grupos_tcc.json")

print("\n--- Geração Concluída ---") # MANTIDO
