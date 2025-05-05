-- Consulta 2: Histórico de disciplinas ministradas por um professor.
-- Retorna o mapa de disciplinas ministradas, com semestre e ano.
-- Substitua 3 pelo ID do professor desejado antes de executar.
USE fei;
SELECT disciplinas_ministradas FROM professor WHERE id_professor = 3;