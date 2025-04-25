# --- START OF FILE query.py ---

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

# --- config do MongoDB ---
MONGO_URI = "mongodb://localhost:27017/"  # Ajuste se necessário
DATABASE_NAME = "feidb"

# --- Funcoes para cada Query ---

def query_historico_aluno(db):
    """Query 1: Histórico escolar de um aluno."""
    try:
        aluno_id_str = input("Digite o ID do aluno para ver o histórico: ")
        aluno_id = int(aluno_id_str)
    except ValueError:
        print("Erro: ID do aluno inválido. Por favor, digite um número.")
        return

    pipeline = [
      { '$match': { '_id': aluno_id } },
      {
        '$project': {
          '_id': 0,
          'nome_aluno': '$nome',
          'curso_id': '$curso_id', # Adicionado para contexto
          'graduado': '$graduado', # Adicionado para contexto
          'semestre_graduacao': '$semestre_graduacao', # Adicionado para contexto
          'historico_formatado': {
            '$map': {
              'input': '$historico',
              'as': 'item',
              'in': {
                'codigo_disciplina': '$$item.codigo',
                'nome_disciplina': '$$item.nome',
                'semestre_cursado': '$$item.semestre',
                'nota': '$$item.nota_final',
                'status': '$$item.status' # Adicionado status
              }
            }
          }
        }
      }
    ]
    try:
        resultado = list(db.alunos.aggregate(pipeline))
        if resultado:
            aluno_data = resultado[0]
            print("\n--- Histórico do Aluno ---")
            print(f"Nome: {aluno_data.get('nome_aluno')}")
            print(f"Curso ID: {aluno_data.get('curso_id')}")
            print(f"Graduado: {'Sim' if aluno_data.get('graduado') else 'Não'}")
            if aluno_data.get('graduado'):
                print(f"Semestre Graduação: {aluno_data.get('semestre_graduacao')}")
            print("Disciplinas Cursadas:")
            if aluno_data.get('historico_formatado'):
                for item in aluno_data['historico_formatado']:
                    print(f"  - {item.get('codigo_disciplina')} ({item.get('nome_disciplina')} | Sem: {item.get('semestre_cursado')} | Nota: {item.get('nota')} | Status: {item.get('status')})")
            else:
                print("  (Nenhum registro no histórico)")
        else:
            print(f"Aluno com ID {aluno_id} não encontrado.")
    except OperationFailure as e:
        print(f"Erro ao executar a query no MongoDB: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


def query_historico_professor(db):
    """Query 2: Histórico de disciplinas ministradas por um professor."""
    try:
        prof_id_str = input("Digite o ID do professor para ver o histórico: ")
        prof_id = int(prof_id_str)
    except ValueError:
        print("Erro: ID do professor inválido. Por favor, digite um número.")
        return

    # Pipeline para buscar professor e depois as informações das disciplinas
    pipeline = [
        {'$match': {'_id': prof_id}},
        {'$lookup': {
            'from': 'disciplinas',  # Junta com a coleção de disciplinas
            'localField': 'disciplinas_ministradas.disciplina_id',
            'foreignField': '_id',
            'as': 'disciplinas_info'
        }},
        {'$project': {
            '_id': 0,
            'nome_professor': '$nome',
            'disciplinas_ministradas': {
                '$map': {
                    'input': '$disciplinas_ministradas',
                    'as': 'ministrada',
                    'in': {
                        'disciplina_id': '$$ministrada.disciplina_id',
                        'semestre': '$$ministrada.semestre',
                        'ano': '$$ministrada.ano',
                        # Encontra a info da disciplina correspondente no array 'disciplinas_info'
                        'info': {
                            '$first': {
                                '$filter': {
                                    'input': '$disciplinas_info',
                                    'as': 'disc_info',
                                    'cond': {'$eq': ['$$disc_info._id', '$$ministrada.disciplina_id']}
                                }
                            }
                        }
                    }
                }
            }
        }},
        # Formata a saída final
        {'$project': {
            'nome_professor': 1,
            'disciplinas_formatadas': {
                '$map': {
                    'input': '$disciplinas_ministradas',
                    'as': 'item',
                    'in': {
                        'codigo_disciplina': '$$item.info.codigo',
                        'nome_disciplina': '$$item.info.nome',
                        'semestre_ministrado': '$$item.semestre',
                        'ano_ministrado': '$$item.ano'
                    }
                }
            }
        }}
    ]

    try:
        resultado = list(db.professores.aggregate(pipeline))
        if resultado:
            prof_data = resultado[0]
            print("\n--- Histórico do Professor ---")
            print(f"Nome: {prof_data.get('nome_professor')}")
            print("Disciplinas Ministradas:")
            if prof_data.get('disciplinas_formatadas'):
                for item in prof_data['disciplinas_formatadas']:
                    print(f"  - {item.get('codigo_disciplina')} ({item.get('nome_disciplina')} | Sem: {item.get('semestre_ministrado')})")
            else:
                print("  (Nenhuma disciplina registrada)")
        else:
            print(f"Professor com ID {prof_id} não encontrado.")
    except OperationFailure as e:
        print(f"Erro ao executar a query no MongoDB: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


def query_alunos_graduados(db):
    """Query 3: Listar alunos graduados em um semestre/ano."""
    semestre_ano = input("Digite o semestre de graduação (formato AAAA.S, ex: 2023.1): ")
    # Validação simples do formato AAAA.S
    try:
        ano, sem = map(int, semestre_ano.split('.'))
        if sem not in [1, 2] or ano < 1900 or ano > 2100:
             raise ValueError("Formato inválido ou ano/semestre fora do esperado.")
    except ValueError:
         print(f"Erro: Formato inválido '{semestre_ano}'. Use AAAA.S (ex: 2023.1 ou 2023.2).")
         return

    query_filter = {
        'graduado': True,
        'semestre_graduacao': semestre_ano
    }
    projection = {
        '_id': 1, # Mostrar o ID do aluno
        'nome': 1
    }
    try:
        # find() retorna um cursor, convertemos para lista para exibir
        resultados = list(db.alunos.find(query_filter, projection))
        if resultados:
            print(f"\n--- Alunos Graduados em {semestre_ano} ---")
            for aluno in resultados:
                # Acessa os campos pelo nome definido na projeção
                print(f"  ID: {aluno.get('_id')}, Nome: {aluno.get('nome')}")
        else:
            print(f"Nenhum aluno encontrado graduado em {semestre_ano}.")
    except OperationFailure as e:
        print(f"Erro ao executar a query no MongoDB: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


def query_chefes_departamento(db):
    """Query 4: Listar professores chefes e seus departamentos."""
    pipeline = [
      { '$match': { 'eh_chefe': True } },
      {
        '$lookup': {
          'from': 'departamentos',
          'localField': 'departamento_id',
          'foreignField': '_id',
          'as': 'info_departamento'
        }
      },
      # Se um chefe pudesse não ter departamento (improvável), use left outer join (unwind com preserveNullAndEmptyArrays)
      { '$unwind': {'path': '$info_departamento', 'preserveNullAndEmptyArrays': True} },
      {
        '$project': {
          '_id': 0,
          'id_professor': '$_id',
          'nome_professor': '$nome',
          'id_departamento': '$info_departamento._id', # Pode ser null se preserveNullAndEmptyArrays=True e não houver match
          'nome_departamento': '$info_departamento.nome', # Pode ser null
          'codigo_departamento': '$info_departamento.codigo_dept' # Adicionado código
        }
      }
    ]
    try:
        resultados = list(db.professores.aggregate(pipeline))
        if resultados:
            print("\n--- Professores Chefes de Departamento ---")
            for chefe in resultados:
                print(f"  Prof ID: {chefe.get('id_professor')}, Nome: {chefe.get('nome_professor')}")
                if chefe.get('id_departamento'):
                     print(f"     -> Dept ID: {chefe.get('id_departamento')}, Código: {chefe.get('codigo_departamento')}, Nome: {chefe.get('nome_departamento')}")
                else:
                     print(f"     -> (Departamento não encontrado ou não associado)")

        else:
            print("Nenhum professor chefe de departamento encontrado.")
    except OperationFailure as e:
        print(f"Erro ao executar a query no MongoDB: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


def query_grupo_tcc(db):
    """Query 5: Detalhes de um grupo de TCC (alunos e orientador)."""
    try:
        grupo_id_str = input("Digite o ID do grupo de TCC: ")
        grupo_id = int(grupo_id_str)
    except ValueError:
        print("Erro: ID do grupo inválido. Por favor, digite um número.")
        return

    pipeline = [
      { '$match': { '_id': grupo_id } },
      {
        '$lookup': {
          'from': 'professores',
          'localField': 'orientador_id',
          'foreignField': '_id',
          'as': 'orientador_info'
        }
      },
      {
        '$lookup': {
          'from': 'alunos',
          'localField': 'alunos_ids',
          'foreignField': '_id',
          'as': 'alunos_info'
        }
      },
      # Unwind do orientador para facilitar o acesso (assume 1 orientador)
      # Usar preserveNullAndEmptyArrays caso um grupo possa existir sem orientador (improvável)
      { '$unwind': {'path': '$orientador_info', 'preserveNullAndEmptyArrays': True} },
      {
        '$project': {
          '_id': 0,
          'grupo_id': '$_id',
          'semestre_tcc': '$semestre',
          'orientador': { # Será null se o lookup/unwind não encontrar
            'id': '$orientador_info._id',
            'nome': '$orientador_info.nome'
          },
          'alunos': {
            '$map': {
              'input': '$alunos_info', # alunos_info será [] se o lookup não achar nenhum
              'as': 'aluno',
              'in': {
                'id': '$$aluno._id',
                'nome': '$$aluno.nome'
              }
            }
          }
        }
      }
    ]
    try:
        resultado = list(db.grupos_tcc.aggregate(pipeline))
        if resultado:
            grupo_data = resultado[0]
            print("\n--- Detalhes do Grupo de TCC ---")
            print(f"Grupo ID: {grupo_data.get('grupo_id')}")
            print(f"Semestre: {grupo_data.get('semestre_tcc')}")
            orientador = grupo_data.get('orientador')
            if orientador and orientador.get('id'):
                 print(f"Orientador: ID {orientador.get('id')}, Nome: {orientador.get('nome')}")
            else:
                 print("Orientador: (Não encontrado ou não definido)")
            print("Alunos:")
            alunos_lista = grupo_data.get('alunos')
            if alunos_lista:
                for aluno in alunos_lista:
                     print(f"  - ID: {aluno.get('id')}, Nome: {aluno.get('nome')}")
            else:
                print("  (Nenhum aluno encontrado neste grupo)")
        else:
            print(f"Grupo de TCC com ID {grupo_id} não encontrado.")
    except OperationFailure as e:
        print(f"Erro ao executar a query no MongoDB: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")


def main():
    """Função principal que exibe o menu e chama as queries."""
    client = None
    try:
        # conexão com o mongo
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000) # de 5 de Time out
        client.admin.command('ping')
        print(f"Conectado com sucesso ao MongoDB em {MONGO_URI}")
        db = client[DATABASE_NAME]

    except ConnectionFailure as e:
        print(f"Erro: Não foi possível conectar ao MongoDB em {MONGO_URI}.")
        print(f"Detalhes: {e}")
        return

    while True:
        print("\n--- Menu de Consultas ---")
        print("1: Histórico escolar de um aluno")
        print("2: Histórico de disciplinas de um professor")
        print("3: Listar alunos graduados em um semestre/ano")
        print("4: Listar professores chefes de departamento")
        print("5: Detalhes de um grupo de TCC")
        print("0: Sair")

        escolha = input("Digite o número da consulta desejada: ")

        if escolha == '1':
            query_historico_aluno(db)
        elif escolha == '2':
            query_historico_professor(db)
        elif escolha == '3':
            query_alunos_graduados(db)
        elif escolha == '4':
            query_chefes_departamento(db)
        elif escolha == '5':
            query_grupo_tcc(db)
        elif escolha == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

        # Adiciona uma pausa para melhor visualização no terminal
        input("\nPressione Enter para continuar...")

    if client:
        client.close()
        print("Conexão com MongoDB fechada.")


if __name__ == "__main__":
    main()
