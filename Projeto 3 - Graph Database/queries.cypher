// 1. Histórico escolar do aluno ID 40
MATCH (a:Aluno {id_aluno: 40})-[r:CURSOU]->(d:Disciplina)
RETURN d.codigo_disciplina, d.nome_disciplina, r.semestre, r.ano, r.nota_final ORDER BY r.ano, r.semestre;

// 2. Disciplinas ministradas pelo professor ID 7
MATCH (p:Professor {id_professor: 7})-[r:MINISTROU]->(d:Disciplina)
RETURN d.nome_disciplina, r.semestre, r.ano ORDER BY r.ano, r.semestre;

// 3. Alunos formados em 2/2024 (Este semestre/ano teve formaturas geradas)
MATCH (a:Aluno)-[f:FORMADO_EM {semestre_formacao: 2, ano_formacao: 2024}]->(m:MatrizCurricular)
RETURN a.id_aluno, a.nome_aluno, m.nome_matriz ORDER BY a.nome_aluno;
//   Para testar outros anos/semestres, você pode verificar quais foram gerados:
//   MATCH ()-[f:FORMADO_EM]->() RETURN DISTINCT f.ano_formacao, f.semestre_formacao ORDER BY f.ano_formacao, f.semestre_formacao;

// 4. Professores chefes de departamento
MATCH (p:Professor)-[:CHEFE_DE]->(d:Departamento)
RETURN p.id_professor, p.nome_professor, d.nome_departamento ORDER BY d.nome_departamento;

// 5. Grupos de TCC e orientadores
MATCH (al:Aluno)-[:PARTICIPA_DE]->(tcc:TCC)<-[:ORIENTA]-(prof:Professor)
RETURN tcc.id_tcc, tcc.titulo_tcc, prof.nome_professor AS orientador, collect({id: al.id_aluno, nome: al.nome_aluno}) AS grupo_alunos
ORDER BY tcc.id_tcc;
