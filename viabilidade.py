# APLICAÇÃO SIMULANDO A VIABILIDADE FINANCEIRA DE UMA ESCOLA

from math import ceil

import pandas as pd
import streamlit as st

########################################################################################
# Parâmetros livres

with st.sidebar:
    n_0 = st.number_input(
        'número inicial de alunos',
        min_value=0,
        max_value=100,
        value=30,
    )

    taxa_de_aumento_ate_agosto = st.number_input(
        'aumento mensal de alunos até agosto',
        min_value=0,
        max_value=100,
        value=4,
    )

    taxa_de_aumento_depois_agosto = st.number_input(
        'aumento mensal de alunos depois de agosto',
        min_value=0,
        max_value=100,
        value=1,
    )

    mensalidade_media= st.number_input(
        'mensalidade média dos alunos',
        min_value=1000,
        max_value=2500,
        value=1928,
    )


########################################################################################
# Funções

def func_despesas(n_alunos):

    n_auxiliares = 0.1* n_alunos
    
    salarios = pd.DataFrame(
        data=[
            # ['gestor', 5000, 30, 30, 1],
            ['diretor', 1780, 30, 30, 1],
            ['coordenador', 1675, 30, 30, 1],
            ['professor_necessidades_especiais', 1630, 44, 44, 1],
            ['auxiliar', 1405, 44, 30, n_auxiliares],
            ['professor', 1630, 20, 20, 6],
            ['professor_ed_fisica', 103, 1, 6, 1],
            ['professor_atividades_extras', 103, 1, 3, 5],
            ['cozinheiro', 1405, 44, 44, 1],
            ['auxiliar_de_servicos_gerais', 1479, 44, 44, 1],
            ['auxiliar_administrativo', 1524, 44, 44, 1],
            ['porteiro', 1479, 44, 44, 1],
        ],
        columns=['cargo', 'piso', 'horas_piso', 'horas_desejadas', 'n_funcionarios']
    )

    salarios['salario'] = salarios['piso'] / salarios['horas_piso'] * salarios['horas_desejadas']
    salarios['salario_total'] = salarios['salario'] * salarios['n_funcionarios']
    salarios['custo_do_funcionario'] = 1.4 * salarios['salario_total']

    despesas = pd.DataFrame(
        data=[
            ['folha_de_pagamento', salarios['custo_do_funcionario'].sum()],
            ['alimentacao', 157*n_alunos],
            ['aluguel', 14661],
            ['luz', 1571],
            ['agua', 1571],
            ['internet', 209],
            ['imposto', 4189]
        ],
        columns=['despesa', 'valor']
    )

    return despesas['valor'].sum()

#####################################################################################
# Cálculo de receitas e despesas mensais em função do número de alunos

mes_a_mes = pd.DataFrame(
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 ,12],
    columns=['mes']
)

n_alunos = []
for mes in range(1, 13):
    if mes == 1:
        n_alunos.append(n_0)
    elif mes <= 8:
        n_alunos.append(
            n_alunos[-1] + taxa_de_aumento_ate_agosto
        )
    else:
        n_alunos.append(
            n_alunos[-1] + taxa_de_aumento_depois_agosto
        )
    
mes_a_mes['n_alunos'] = n_alunos
mes_a_mes['mensalidades'] = mes_a_mes['n_alunos']*mensalidade_media


despesas_ate_agosto = mes_a_mes.iloc[:8].apply(
    lambda row: func_despesas(row['n_alunos'] ),
    axis=1,
)
despesas_depois_agosto = mes_a_mes.iloc[8:].apply(
    lambda row: func_despesas(row['n_alunos']),
    axis=1,
)
mes_a_mes['despesas'] = pd.concat([despesas_ate_agosto, despesas_depois_agosto])

mes_a_mes['lucro'] = mes_a_mes['mensalidades'] - mes_a_mes['despesas']

mes_a_mes['acumulado'] = mes_a_mes['lucro'].cumsum()

########################################################################################
# Visualização da tabela

fundo_do_poco = mes_a_mes['acumulado'].idxmin()

recuperacao = mes_a_mes[mes_a_mes['acumulado'].ge(0)]['acumulado'].idxmin()

def highlight_rows(row):
    if row.name == recuperacao:
        return ['background-color: lightgreen']*6
    elif row.name == fundo_do_poco:
        return ['background-color: red']*6
    else:
        return [None]*6

st.dataframe(
    mes_a_mes.style \
        .format(precision=2, thousands=" ", decimal=",") \
        .apply(highlight_rows, axis=1),
    hide_index=True,
    height=458,
    column_config={
        'mes': 'mês',
        'n_alunos': 'alunos',
    }
)
