# Cálculos para a viabilidade de uma escola

em construção...

-----------------

## Introdução

Uma escola de período integral recém comprada e com dívidas solicitou uma avaliação das finanças para guiar uma tomada de decisão: fechar, vender ou investir.

Para orientar melhor uma tomada de decisão sobre o futuro da escola, calculamos uma previsão das despesas e receitas para 2024. Os detalhes de diagnóstico financeiro estão no repositório diagnostico-escola. Os detalhes do cálculo das receitas de mensalidade estão no repositório calculo-de-mensalidade. 

Neste trabalho fizemos uma aplicação para simular as despesas, lucros ou prejuízos para o ano de 2024 em função do número de matrículas da escola.

## Dados

A MP-resuldados fez uma extensa pesquisa a respeito das leis e deliberações que regem o funcionamento da escola para conhecer a hierarquia padrão, os profissionais obrigatórios, os pisos salariais e todas as informações relevantes para um cálculo bem embasado. Contamos com a colaboração de um profissional da escola, um profissional do Conselho Regional de Educação e um contador.

Com os dados pesquisados, montamos uma tabela para os salários contendo:
- o nome do cargo;
- o piso salarial de cada cargo;
- o número de horas a que se refere o piso;
- o número de horas do contrato profissional;
- número de funcionarios no cargo.

Para a escola em questão, um aumento de alunos requer a contratação de mais auxiliares. Com base na lei e na distribuição de alunos da escola, utilizamos uma expressão para calcular o número de auxiliares necessários em função do número de alunos.

Utilizamos as informações da tabela para calcular os salários e o custo do funcionário para empresa (salários mais encargos).

Para a tabela de despesas, utlilizamos os dados de:
- folha de pagamento (calculado a partir da tabela de salários);
- aluguel;
- luz;
- água;
- internet;
- impostos;
- gastos com alimentação;

Como os gastos com alimentação dependem do número de alunos, utilizamos uma expressão onde multiplicamos o gasto por aluno pelo número de alunos. O gasto por aluno foi feito com base em dados da escola do meses de junho a novembro.

## Simulação

Como dados de entrada para a simulação temos:
- o número de alunos matriculados no início do ano;
- taxa de aumento mensal de alunos até agosto;
- taxa de aumento mensal de alunos após agosto;
- mensalidade média.

O número de alunos matriculados no início do ano se refere aos alunos com contratos já fechados para o presente ano (2024).

As taxas de aumento se referem às matrículas que são realizadas durante o ano letivo. Segundo dados da escola, a procura é maior no primeiro semestre do que no segundo, por isso as taxas estão separadas em antes e depois de agosto.

A mensalidade média foi calculada com base na distribuição de alunos do mês de agosto de 2023. É uma média ponderada já que o valor da mensalidade varia com o número de horas de permanência do aluno na escola.

A simulação pode ser rodada em [streamlit](https://viabilidade-de-negocio-3jpsfpfguz2qtrr7wde6dd.streamlit.app/).

As cores vermelho e verde que realçam a tabela se referem respectivamente a:
- mês de maior prejuízo acumulado;
- mês de recuperação do prejuízo acumulado.

## Conclusão

 continua...


-----------------------------------------------------------------------------
MP-resuldados

Dos dados aos resultados. Um pouco de física, matemática, negócios e finanças.