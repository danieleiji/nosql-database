# Projeto 1 - Document Store (Modelo Acadêmico)

## Descrição

Este projeto simula um ambiente acadêmico simplificado utilizando um banco de dados NoSQL (MongoDB) como Document Store. Ele consiste em três scripts Python principais:

1.  **`Gerador.py`**: Gera dados fictícios (alunos, professores, cursos, disciplinas, departamentos, grupos de TCC) usando a biblioteca `Faker` e os salva em arquivos JSON.
2.  **`insert.py`**: Lê os arquivos JSON gerados e insere os dados nas coleções correspondentes no banco de dados MongoDB `feidb`.
3.  **`query.py`**: Oferece uma interface de linha de comando interativa para realizar consultas pré-definidas sobre os dados armazenados no MongoDB.

O objetivo é demonstrar a modelagem e manipulação de dados em um ambiente NoSQL orientado a documentos, focando nas relações e consultas comuns em um sistema acadêmico.

## Integrante

*   **Daniel Eiji Osato Yoshida** - (RA: 22.121.131-1)

## Tecnologias e Pré-requisitos

*   **Python**: Versão 3.8 ou superior recomendada.
*   **Pip**: Gerenciador de pacotes do Python (geralmente incluído na instalação do Python).
*   **MongoDB**: Uma instância do MongoDB (versão 4.x ou superior) deve estar **instalada e em execução**.
*   **MongoDB Shell (`mongosh`)**: Ferramenta de linha de comando para interagir com o MongoDB (geralmente instalada com o servidor MongoDB).
*   **Bibliotecas Python**:
    *   `pymongo`: Para interagir com o MongoDB a partir do Python.
    *   `Faker`: Para gerar dados fictícios.

## Instalação do MongoDB (Guia Rápido)

Antes de executar os scripts do projeto, você precisa ter o MongoDB instalado e rodando.

1.  **Baixe e Instale:** Siga as instruções oficiais de instalação do MongoDB Community Server para o seu sistema operacional: [MongoDB Installation Tutorials](https://www.mongodb.com/docs/manual/installation/)
2.  **Inicie o Serviço:** Após a instalação, certifique-se de que o serviço MongoDB (`mongod`) esteja em execução. Os comandos para iniciar/parar/verificar o status variam conforme o sistema operacional (consulte a documentação).
3.  **Acesse o Shell (`mongosh`):** Abra um terminal ou prompt de comando e digite `mongosh`. Se conectar com sucesso, você estará no shell interativo do MongoDB.
4.  **Banco de Dados `feidb`:** O banco de dados `feidb` (usado por este projeto) será **criado automaticamente** pelo MongoDB na primeira vez que o script `insert.py` tentar inserir dados nele. Você não precisa criá-lo manualmente antes, mas pode selecioná-lo no `mongosh` com o comando `use feidb`.

## Descrição das Coleções

O banco de dados `feidb` utiliza as seguintes coleções para armazenar os dados da simulação acadêmica:

1.  **`departamentos`**
    *   **Propósito:** Armazena informações sobre os departamentos acadêmicos.
    *   **Estrutura:** `{ _id: Int, nome: String, codigo_dept: String, chefe_id: Int | Null }`

2.  **`cursos`**
    *   **Propósito:** Armazena informações sobre os cursos de graduação.
    *   **Estrutura:** `{ _id: Int, nome: String, departamento_id: Int | Null, disciplinas_ids: [Int] }`

3.  **`disciplinas`**
    *   **Propósito:** Armazena informações sobre as disciplinas individuais.
    *   **Estrutura:** `{ _id: Int, codigo: String, nome: String }`

4.  **`professores`**
    *   **Propósito:** Armazena informações sobre os professores.
    *   **Estrutura:** `{ _id: Int, nome: String, departamento_id: Int | Null, eh_chefe: Boolean, disciplinas_ministradas: [{ disciplina_id: Int, semestre: String, ano: Int }] }`

5.  **`alunos`**
    *   **Propósito:** Armazena informações sobre os alunos.
    *   **Estrutura:** `{ _id: Int, nome: String, curso_id: Int | Null, historico: [{ codigo: String, nome: String, semestre: String, ano: Int, nota_final: Double, status: String }], graduado: Boolean, semestre_graduacao: String | Null }`

6.  **`grupos_tcc`**
    *   **Propósito:** Armazena informações sobre os grupos de TCC.
    *   **Estrutura:** `{ _id: Int, orientador_id: Int | Null, alunos_ids: [Int], semestre: String }`

*Para detalhes completos dos campos, consulte o código `Gerador.py` ou inspecione os documentos no MongoDB.*

## Instalação do Projeto (Python)

1.  **Clone o Repositório:**
    ```bash
    # Substitua [URL_DO_SEU_REPOSITORIO] pela URL correta do seu repo
    git clone [URL_DO_SEU_REPOSITORIO]
    # Substitua [NOME_DA_PASTA_DO_PROJETO] pelo nome do diretório criado
    cd [NOME_DA_PASTA_DO_PROJETO]
    ```
    *(Exemplo de URL: `https://github.com/danieleiji/nosql-database.git`)*
    *(Exemplo de `cd`: `cd nosql-database/Projeto 1 - Document Store` - ajuste conforme sua estrutura)*

2.  **Crie e Ative um Ambiente Virtual (Recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    # ou
    .\venv\Scripts\activate  # Windows
    ```

3.  **Instale as Dependências Python:**
    ```bash
    pip install pymongo Faker
    ```
    *   (Opcional) Se houver um `requirements.txt`: `pip install -r requirements.txt`

## Criação Explícita das Coleções (Opcional)

Embora o MongoDB crie as coleções automaticamente na primeira inserção, você pode criá-las explicitamente no `mongosh` se desejar. Conecte-se ao banco (`mongosh "mongodb://localhost:27017/feidb"`) e execute:

```
db.createCollection("departamentos")
db.createCollection("cursos")
db.createCollection("disciplinas")
db.createCollection("professores")
db.createCollection("alunos")
db.createCollection("grupos_tcc")
show collections // Para verificar