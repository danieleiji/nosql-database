# Projeto 1 - Document Store (Modelo Acadêmico)

## Descrição

Este projeto simula um ambiente acadêmico simplificado utilizando um banco de dados NoSQL (MongoDB) como Document Store. Ele consiste em três scripts Python principais:

1.  **`Gerador.py`**: Gera dados fictícios (alunos, professores, cursos, disciplinas, departamentos, grupos de TCC) usando a biblioteca `Faker` e os salva em arquivos JSON.
2.  **`insert.py`**: Lê os arquivos JSON gerados e insere os dados nas coleções correspondentes em um banco de dados MongoDB.
3.  **`query.py`**: Oferece uma interface de linha de comando interativa para realizar consultas pré-definidas sobre os dados armazenados no MongoDB.

O objetivo é demonstrar a modelagem e manipulação de dados em um ambiente NoSQL orientado a documentos, focando nas relações e consultas comuns em um sistema acadêmico.

## Integrante

*   **[Coloque Seu Nome Aqui]** - ([Link para Seu GitHub/Contato Aqui - Opcional])

## Tecnologias e Pré-requisitos

*   **Python**: Versão 3.8 ou superior recomendada.
*   **Pip**: Gerenciador de pacotes do Python (geralmente incluído na instalação do Python).
*   **MongoDB**: Uma instância do MongoDB (versão 4.x ou superior) deve estar em execução. O script de inserção assume a URI padrão `mongodb://localhost:27017/`.
*   **MongoDB Shell (`mongosh`)**: Opcional, mas útil para verificar os dados diretamente no banco.
*   **Bibliotecas Python**:
    *   `pymongo`: Para interagir com o MongoDB.
    *   `Faker`: Para gerar dados fictícios.

## Instalação

1.  **Clone o Repositório:**
    ```bash
    git clone [URL do seu repositório]
    cd [nome-do-diretorio-do-projeto]
    ```

2.  **Instale as Dependências Python:**
    É recomendado criar um ambiente virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    # ou
    .\venv\Scripts\activate  # Windows
    ```
    Instale as bibliotecas:
    ```bash
    pip install pymongo Faker
    ```
    *   (Opcional) Você pode criar um arquivo `requirements.txt` com o seguinte conteúdo:
        ```txt
        pymongo>=4.0
        Faker>=10.0
        ```
        E então instalar com:
        ```bash
        pip install -r requirements.txt
        ```

3.  **Verifique o MongoDB:** Certifique-se de que o serviço MongoDB esteja em execução na sua máquina ou em um local acessível pela URI `mongodb://localhost:27017/`.

## Como Usar

Siga estes passos na ordem correta:

1.  **Gerar Dados (`Gerador.py`):**
    Execute o script para criar os arquivos JSON com os dados simulados.
    ```bash
    python Gerador.py
    ```
    Isso criará arquivos como `alunos.json`, `professores.json`, `cursos.json`, etc., no mesmo diretório.

2.  **Inserir Dados no MongoDB (`insert.py`):**
    Execute o script para popular o banco de dados `feidb` (ou o nome definido em `DATABASE_NAME` no script) com os dados dos arquivos JSON.
    ```bash
    python insert.py
    ```
    *   **Atenção:** Por padrão, o script `insert.py` está configurado com `LIMPAR_COLECOES_ANTES = True`. Isso significa que **ele apagará todos os dados existentes** nas coleções (`alunos`, `professores`, etc.) antes de inserir os novos. Mude para `False` se desejar apenas adicionar dados (cuidado com IDs duplicados).

3.  **Realizar Consultas (`query.py` ou `mongosh`):**

    *   **Usando o Script Interativo (`query.py`):**
        Execute o script para acessar o menu de consultas pré-definidas:
        ```bash
        python query.py
        ```
        Siga as instruções no menu para escolher a consulta desejada e fornecer os parâmetros necessários (como IDs ou semestres).

    *   **Usando o MongoDB Shell (`mongosh`):**
        Você pode conectar-se diretamente ao banco de dados para realizar consultas ad-hoc ou verificar os dados.
        ```bash
        # Conecte-se ao banco de dados 'feidb'
        mongosh "mongodb://localhost:27017/feidb"
        ```
        Uma vez conectado, você pode usar comandos do MongoDB. Exemplos:
        ```javascript
        // Listar todas as coleções
        show collections

        // Ver alguns alunos
        db.alunos.find().limit(5).pretty()

        // Ver um professor específico pelo ID (substitua 1 pelo ID desejado)
        db.professores.findOne({ _id: 1 })

        // Listar cursos
        db.cursos.find({}, { _id: 1, nome: 1 }).pretty()
        ```

    *   **Dica para a Consulta 3 (Alunos Graduados):**
        Se você quiser encontrar alunos graduados em um semestre específico diretamente no `mongosh` (além de usar a opção 3 no script `query.py`), você pode usar uma consulta como esta. Procure por documentos onde `graduado` é `true` e `semestre_graduacao` corresponde ao valor desejado:
        ```javascript
        // Exemplo: Encontrar alunos graduados em 2023.1
        const semestreAnoFormacao = "2023.1"; // <-- Defina o semestre/ano aqui

        db.alunos.find(
          {
            graduado: true,              // Condição essencial
            semestre_graduacao: semestreAnoFormacao // Filtra pelo semestre/ano
          },
          {                             // Projeção: quais campos mostrar
            _id: 1,                     // Mostrar o ID do aluno
            nome: 1                     // Mostrar o nome do aluno
          }
        ).pretty();
        ```
        Lembre-se que a existência de alunos graduados depende dos dados gerados aleatoriamente pelo `Gerador.py` e das regras de graduação (nota mínima e conclusão da matriz curricular).