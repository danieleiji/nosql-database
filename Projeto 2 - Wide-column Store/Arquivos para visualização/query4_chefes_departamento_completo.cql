-- Consulta 4 (Combinada): Listar professores chefes de departamento com nomes.
-- EXECUÇÃO EM MÚLTIPLAS ETAPAS NECESSÁRIA NO CQLSH:

-- Etapa A: Obtenha os IDs dos chefes e os nomes dos departamentos.
-- Anote os 'id_chefe_departamento' retornados para usar na Etapa B.
USE fei;
SELECT id_chefe_departamento, nome FROM departamento;

-- Etapa B: Busque o nome do professor para cada ID de chefe obtido na Etapa A.
-- Substitua '...' pela lista de IDs obtida (ex: 1, 5, 8).
-- Execute este comando APÓS a Etapa A.
-- USE fei; -- (Opcional se já estiver no keyspace)
SELECT id_professor, nome FROM professor WHERE id_professor IN (...); -- Substitua '...' pelos IDs da Etapa A