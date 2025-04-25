# --- START OF FILE insert.py ---

import json
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, BulkWriteError

# --- Configurações do MongoDB ---
MONGO_URI = "mongodb://localhost:27017/" # Ajuste se necessário
DATABASE_NAME = "feidb"

# --- Arquivos JSON e Nomes das Coleções Esperados ---
# O nome da coleção será derivado do nome do arquivo (sem a extensão)
JSON_FILES = [
    "departamentos.json",
    "cursos.json",
    "disciplinas.json",
    "professores.json",
    "alunos.json",
    "grupos_tcc.json",
]

# --- Opção de Limpeza ---
# Defina como True se quiser limpar CADA coleção correspondente antes de inserir.
# Use com CUIDADO, pois apaga dados existentes nessas coleções.
LIMPAR_COLECOES_ANTES = True

def inserir_dados_multi_colecao():
    """Conecta ao MongoDB, lê arquivos JSON e insere em coleções separadas."""
    try:
        client = MongoClient(MONGO_URI)
        client.admin.command('ping') # Verifica a conexão
        print(f"Conectado com sucesso ao MongoDB em {MONGO_URI}")
    except ConnectionFailure as e:
        print(f"Erro ao conectar ao MongoDB: {e}")
        return

    db = client[DATABASE_NAME]
    print(f"Usando banco de dados: '{DATABASE_NAME}'")

    total_docs_sucesso_geral = 0
    erros_cont_geral = 0

    for filename in JSON_FILES:
        # Deriva o nome da coleção do nome do arquivo
        collection_name = os.path.splitext(filename)[0]
        collection = db[collection_name] # Obtém o objeto da coleção (será criada na primeira inserção se não existir)
        print(f"\n--- Processando '{filename}' para a coleção '{collection_name}' ---")

        # Opcional: Limpar a coleção específica antes de inserir
        if LIMPAR_COLECOES_ANTES:
            print(f"Limpando a coleção '{collection_name}'...")
            try:
                delete_result = collection.delete_many({})
                print(f"  -> {delete_result.deleted_count} documentos removidos da coleção '{collection_name}'.")
            except Exception as e:
                print(f"  ERRO ao limpar a coleção '{collection_name}': {e}")
                # Decide se quer continuar ou parar se a limpeza falhar
                # Neste caso, vamos tentar inserir mesmo assim, mas registrar o erro.
                erros_cont_geral += 1


        docs_inseridos_arquivo = 0
        erros_arquivo = 0

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Verifica se é uma lista e não está vazia
            if not isinstance(data, list) or not data:
                print(f"AVISO: {filename} está vazio ou não é uma lista JSON. Pulando.")
                continue

            # Filtra para garantir que estamos inserindo apenas dicionários e que eles têm um _id
            docs_para_inserir = []
            for doc in data:
                if isinstance(doc, dict):
                    if '_id' in doc: # Verifica se o _id essencial está presente
                        docs_para_inserir.append(doc)
                    else:
                        print(f"  AVISO: Documento em {filename} sem campo '_id'. Pulando item: {doc}")
                        erros_arquivo += 1
                else:
                     print(f"  AVISO: Item não é um dicionário em {filename}. Item: {doc}. Pulando item.")
                     erros_arquivo += 1


            if not docs_para_inserir:
                 print(f"AVISO: Nenhum documento válido (dicionário com _id) encontrado em {filename}. Pulando inserção.")
                 erros_cont_geral += erros_arquivo # Adiciona erros de validação ao total
                 continue

            # Insere os documentos na coleção específica
            print(f"Tentando inserir {len(docs_para_inserir)} documentos na coleção '{collection_name}'...")
            try:
                result = collection.insert_many(docs_para_inserir, ordered=False) # ordered=False tenta inserir o máximo possível
                print(f"  -> Sucesso: {len(result.inserted_ids)} documentos inseridos.")
                docs_inseridos_arquivo = len(result.inserted_ids)
            except BulkWriteError as bwe:
                # Erro comum aqui é E11000 se houver _id duplicado DENTRO do mesmo arquivo JSON
                print(f"  ERRO (BulkWriteError) ao inserir em '{collection_name}':")
                print(f"    -> {bwe.details['nInserted']} inseridos com sucesso.")
                print(f"    -> {len(bwe.details['writeErrors'])} falhas (ex: _id duplicado?).")
                # print(f"    -> Detalhes dos erros: {bwe.details['writeErrors']}") # Descomente para ver detalhes
                docs_inseridos_arquivo = bwe.details['nInserted']
                erros_arquivo += len(bwe.details['writeErrors'])
            except Exception as e:
                print(f"  ERRO inesperado (DB) ao inserir em '{collection_name}': {e}")
                erros_arquivo += len(docs_para_inserir) # Assume que todos falharam nesta exceção


        except FileNotFoundError:
            print(f"ERRO: Arquivo '{filename}' não encontrado. Pulando.")
            erros_arquivo += 1
        except json.JSONDecodeError:
            print(f"ERRO: Arquivo '{filename}' não contém JSON válido. Pulando.")
            erros_arquivo += 1
        except Exception as e:
            print(f"ERRO inesperado ao processar o arquivo {filename}: {e}")
            erros_arquivo += 1 # Conta como um erro geral para o arquivo

        total_docs_sucesso_geral += docs_inseridos_arquivo
        erros_cont_geral += erros_arquivo
        print(f"--- Fim do processamento para '{filename}' ---")


    print("\n========= Resumo Geral da Inserção =========")
    print(f"Total de documentos inseridos com sucesso em todas as coleções: {total_docs_sucesso_geral}")
    if erros_cont_geral > 0:
        print(f"Número total de erros (validação, escrita, arquivo): {erros_cont_geral}")
    print("============================================")

    client.close()
    print("Conexão com MongoDB fechada.")

if __name__ == "__main__":
    inserir_dados_multi_colecao()
# --- END OF FILE insert.py ---