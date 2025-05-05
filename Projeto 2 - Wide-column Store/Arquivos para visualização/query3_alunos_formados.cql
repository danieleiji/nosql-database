-- Consulta 3: Listar alunos formados em um semestre/ano.
-- Retorna o ID e nome dos alunos formados no período especificado.
-- Substitua 2023 e 2 pelo ano e semestre desejados antes de executar.
USE fei;
SELECT id_aluno, nome FROM alunos_formado WHERE ano = 2023 AND semestre = 2;