Projeto 1 - Document Store (Modelo Acadêmico)
Este projeto simula um ambiente acadêmico simplificado utilizando um banco de dados NoSQL (MongoDB) como Document Store. Ele demonstra a modelagem e manipulação de dados, focando nas relações e consultas comuns em um sistema acadêmico.
O projeto é composto por três scripts Python principais:
Gerador.py: Responsável por gerar dados fictícios (alunos, professores, cursos, disciplinas, departamentos, grupos de TCC) utilizando a biblioteca Faker. Os dados gerados são salvos em arquivos JSON na pasta data.
insert.py: Lê os arquivos JSON da pasta data e insere os dados correspondentes nas coleções no banco de dados MongoDB feidb.
query.py: Fornece uma interface de linha de comando interativa para executar consultas pré-definidas sobre os dados no MongoDB.
Integrante
Daniel Eiji Osato Yoshida - (RA: 22.121.131-1)
Tecnologias e Pré-requisitos
Para rodar este projeto, você precisará ter instalado:
Python: Versão 3.8 ou superior é recomendada.
Pip: Gerenciador de pacotes do Python.
MongoDB: Uma instância do MongoDB (versão 4.x ou superior) deve estar instalada e em execução.
MongoDB Shell (mongosh): Ferramenta de linha de comando para interagir com o MongoDB.
Bibliotecas Python: Instale-as via pip:
pymongo: Para a comunicação com o MongoDB.
Faker: Para a geração de dados fictícios.
Instalação do MongoDB (Guia Rápido)
Se você ainda não possui o MongoDB instalado, siga este guia rápido:
Baixe e Instale: Siga as instruções oficiais para seu sistema operacional em: MongoDB Installation Tutorials (https://www.mongodb.com/docs/manual/installation/)
Inicie o Serviço: Certifique-se de que o serviço mongod esteja rodando após a instalação. Os comandos variam por sistema (consulte a documentação).
Acesse o Shell: Abra um terminal e digite mongosh.
Banco de Dados feidb: Este banco de dados será criado automaticamente pelo MongoDB na primeira vez que o script insert.py tentar inserir dados nele.
Descrição das Coleções do Banco de Dados feidb
O banco de dados feidb organiza os dados nas seguintes coleções:
departamentos
Propósito: Armazena informações sobre os departamentos acadêmicos.
Estrutura: { _id: Int, nome: String, codigo_dept: String, chefe_id: Int | Null }
cursos
Propósito: Armazena informações sobre os cursos de graduação.
Estrutura: { _id: Int, nome: String, departamento_id: Int | Null, disciplinas_ids: [Int] }
disciplinas
Propósito: Armazena informações sobre as disciplinas oferecidas.
Estrutura: { _id: Int, codigo: String, nome: String }
professores
Propósito: Armazena informações sobre os professores.
Estrutura: { _id: Int, nome: String, departamento_id: Int | Null, eh_chefe: Boolean, disciplinas_ministradas: [{ disciplina_id: Int, semestre: String, ano: Int }] }
alunos
Propósito: Armazena informações sobre os alunos.
Estrutura: { _id: Int, nome: String, curso_id: Int | Null, historico: [{ codigo: String, nome: String, semestre: String, ano: Int, nota_final: Double, status: String }], graduado: Boolean, semestre_graduacao: String | Null }
grupos_tcc
Propósito: Armazena informações sobre os grupos de Trabalho de Conclusão de Curso.
Estrutura: { _id: Int, orientador_id: Int | Null, alunos_ids: [Int], semestre: String }
Consulte o código Gerador.py ou inspecione os documentos no MongoDB para detalhes completos dos campos.
Instalação do Projeto (Python)
Siga estes passos para configurar o ambiente Python do projeto:
Clone o Repositório:
Substitua [URL_DO_SEU_REPOSITORIO] pela URL correta do seu repositório
git clone [URL_DO_SEU_REPOSITORIO]
Navegue para a pasta do projeto
cd [NOME_DA_PASTA_DO_PROJETO]
(Exemplo de URL: https://github.com/danieleiji/nosql-database.git)
(Exemplo de cd: cd nosql-database/Projeto 1 - Document Store - ajuste conforme sua estrutura de diretórios)
Crie e Ative um Ambiente Virtual (Recomendado):
python -m venv venv
Para ativar no Linux/macOS:
source venv/bin/activate
Para ativar no Windows:
.\venv\Scripts\activate
Instale as Dependências Python:
pip install pymongo Faker
(Opcional) Se houver um requirements.txt: pip install -r requirements.txt
Criação Explícita das Coleções (Opcional)
Embora o MongoDB crie as coleções na primeira inserção, você pode criá-las explicitamente usando o mongosh. Conecte-se ao banco (mongosh "mongodb://localhost:27017/feidb") e execute os comandos:
db.createCollection("departamentos")
db.createCollection("cursos")
db.createCollection("disciplinas")
db.createCollection("professores")
db.createCollection("alunos")
db.createCollection("grupos_tcc")
show collections // Verifique se foram criadas
Como Usar e Validar o Projeto
Siga a ordem abaixo, garantindo que o servidor MongoDB esteja rodando:
Gerar Dados (Gerador.py):
Este passo criará os arquivos JSON na pasta data/.
python Gerador.py
Inserir Dados no MongoDB (insert.py):
Este passo lerá os JSONs e populará o banco de dados feidb.
python insert.py
Observação: O script insert.py possui a flag LIMPAR_COLECOES_ANTES = True (padrão), que apagará todos os dados existentes nas coleções antes de inserir os novos.
Realizar e Validar Consultas:
Usando o Script Interativo (query.py):
Execute o script principal de consultas.
python query.py
Siga as opções do menu interativo (consultas 1 a 5) para executar as operações pré-definidas.
Usando o MongoDB Shell (mongosh):
Para validação direta ou consultas manuais. Conecte-se ao banco:
mongosh "mongodb://localhost:27017/feidb"
Você pode verificar a contagem de documentos, inspecionar dados ou executar consultas de validação. Exemplos:
// Verificar coleções
show collections
// Contar documentos (exemplo com alunos)
db.alunos.countDocuments()
// Ver os primeiros 5 documentos de professores
db.professores.find().limit(5).pretty()
// Exemplo de validação da Query 3 (Alunos Graduados em um semestre)
const semestre = "2023.1"; // Ajuste para um semestre gerado
db.alunos.find( { graduado: true, semestre_graduacao: semestre }, { _id: 1, nome: 1 } ).pretty()
Compare os resultados obtidos no mongosh com os do script query.py para validar a lógica.
