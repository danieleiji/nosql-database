-- Consulta 1: Histórico escolar de um aluno.
-- Retorna o mapa de disciplinas concluídas, com semestre, ano e nota.
-- Substitua 1 pelo ID do aluno desejado antes de executar.
USE fei;
SELECT disciplinas_concluidas FROM alunos WHERE id_aluno = 1;