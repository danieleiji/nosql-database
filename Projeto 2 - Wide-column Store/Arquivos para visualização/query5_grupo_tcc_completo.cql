-- Consulta 5 (Combinada): Membros e orientador de um grupo de TCC com nomes.
-- EXECUÇÃO EM MÚLTIPLAS ETAPAS NECESSÁRIA NO CQLSH:

-- Etapa A: Obtenha o ID do professor orientador e a lista de IDs dos membros.
-- Substitua 2 pelo ID do grupo desejado.
-- Anote o 'id_professor' e a lista 'membros' retornados para usar nas Etapas B e C.
USE fei;
SELECT id_professor, membros FROM grupo_proj WHERE id_grupo = 2;

-- Etapa B: Busque o nome do professor orientador.
-- Substitua '...' pelo 'id_professor' obtido na Etapa A.
-- Execute este comando APÓS a Etapa A.
-- USE fei; -- (Opcional se já estiver no keyspace)
SELECT nome FROM professor WHERE id_professor = ...; -- Substitua '...' pelo ID do professor da Etapa A

-- Etapa C: Busque os nomes dos alunos membros.
-- Substitua '...' pela lista de IDs de 'membros' obtida na Etapa A (ex: 10, 15, 22).
-- Execute este comando APÓS a Etapa A.
-- USE fei; -- (Opcional se já estiver no keyspace)
SELECT id_aluno, nome FROM alunos WHERE id_aluno IN (...); -- Substitua '...' pela lista de IDs de membros da Etapa A