from math import ceil

import pandas as pd
import streamlit as st


########################################################################################
# Parâmetros livres.
with st.sidebar:
    n_alunos_janeiro = st.number_input(
        'número de alunos em janeiro',
        min_value=0,
        max_value=100,
        value=30,
    )

    mensalidade_media_alunos_antigos = st.number_input(
        'mensalidade média em janeiro',
        min_value=1000.,
        max_value=2250.,
        value=1702,
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

    mensalidade_media_alunos_novos = st.number_input(
        'mensalidade média dos alunos novos',
        min_value=1000.,
        max_value=2500.,
        value=1928,
    )


########################################################################################
# Funções.

def func_despesas(n_alunos):

    n_auxiliares = 0.217* n_alunos
    n_auxiliares = 0.3 * n_alunos

    salarios = pd.DataFrame(
        data=[
            # ['gestor', True, 5000, 30, 30, 1],
            ['diretor', True, 1780, 30, 30, 1],
            ['coordenador', True, 1675, 30, 30, 1],
            ['professor_necessidades_especiais', True, 1630, 44, 44, 1],
            ['auxiliar', False, 1405, 44, 30, n_auxiliares],
            ['professor', True, 1630, 20, 20, 6],
            ['professor_ed_fisica', True, 1032, 1, 6, 1],
            ['professor_atividades_extras', True, 1032, 1, 3, 5],
            ['cozinheiro', True, 1405, 44, 44, 1],
            ['auxiliar_de_servicos_gerais', True, 1479, 44, 44, 1],
            ['auxiliar_administrativo', True, 1524, 44, 44, 1],
            ['porteiro', True, 1479, 44, 44, 1],
        ],
        columns=['cargo', 'fixo', 'piso', 'horas_piso', 'horas_desejadas', 'n_funcionarios']
    )

    salarios['salario'] = salarios['piso'] / salarios['horas_piso'] * salarios['horas_desejadas']
    salarios['salario_total'] = salarios['salario'] * salarios['n_funcionarios']
    salarios['encargo'] = 1.4 * salarios['salario_total']

    despesas = pd.DataFrame(
        data=[
            ['encargos_variaveis', 'var', salarios[~salarios['fixo']]['encargo'].sum()],
            ['mercado', 'var', 157*n_alunos],
            ['encargos_fixos', 'fixo', salarios[salarios['fixo']]['encargo'].sum()],
            ['aluguel', 'fixo', 14661],
            ['luz', 'fixo', 1571],
            ['agua', 'fixo', 1571],
            ['internet', 'fixo', 209],
            ['imposto', 'fixo', 4189]
        ],
        columns=['despesa', 'tipo', 'valor']
    )

    return despesas['valor'].sum()

#####################################################################################3

n_auxiliares_janeiro = ceil(n_alunos_janeiro / 6)

salarios_janeiro = pd.DataFrame(
    data=[
        # ['gestor', True, 5000, 30, 30, 1],
        ['diretor', True, 1780, 30, 30, 1],
        ['auxiliar', False, 1405, 44, 30, n_auxiliares_janeiro],
        ['cozinheiro', True, 1405, 44, 44, 1],
        ['auxiliar_de_servicos_gerais', True, 1479, 44, 44, 1],
        ['auxiliar_administrativo', True, 1524, 44, 44, 1],
    ],
    columns=['cargo', 'fixo', 'piso', 'horas_piso', 'horas_desejadas', 'n_funcionarios']
)

salarios_janeiro['salario'] = salarios_janeiro['piso'] / salarios_janeiro['horas_piso'] * salarios_janeiro['horas_desejadas']
salarios_janeiro['salario_total'] = salarios_janeiro['salario'] * salarios_janeiro['n_funcionarios']
salarios_janeiro['encargo'] = 1.4 * salarios_janeiro['salario_total']

despesas_janeiro = pd.DataFrame(
    data=[
        ['mercado', 'var', 157*n_alunos_janeiro],
        ['aluguel', 'fixo', 14661],
        ['luz', 'fixo', 1571],
        ['agua', 'fixo', 1571],
        ['internet', 'fixo', 209],
        ['imposto', 'fixo', 4189]
    ],
    columns=['despesa', 'tipo', 'valor']
)

receitas_janeiro = pd.DataFrame(
    [
        ['mensalidades', n_alunos_janeiro * mensalidade_media_alunos_antigos]
    ],
    columns=['receita', 'valor']
)

lucro_janeiro = receitas_janeiro['valor'].sum() - despesas_janeiro['valor'].sum()


#####################################################################################


mes_a_mes = pd.DataFrame(
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 ,12],
    columns=['mes']
)

n_alunos = []
for mes in range(1, 13):
    if mes == 1:
        n_alunos.append(n_alunos_janeiro)
    elif mes <= 8:
        n_alunos.append(
            n_alunos[-1] + taxa_de_aumento_ate_agosto
        )
    else:
        n_alunos.append(
            n_alunos[-1] + taxa_de_aumento_depois_agosto
        )
    
mensalidades = [n_alunos_janeiro * mensalidade_media_alunos_antigos]
for mes in range(1, 12):
    mensalidades.append(
        mensalidades[-1] + (n_alunos[mes] - n_alunos[mes-1])* mensalidade_media_alunos_novos 
    )


mes_a_mes['n_alunos'] = n_alunos
mes_a_mes['mensalidades'] = mensalidades








despesas_ate_agosto = mes_a_mes.iloc[:8].apply(
    lambda row: func_despesas(row['n_alunos'] - taxa_de_aumento_ate_agosto),
    axis=1,
)
despesas_depois_agosto = mes_a_mes.iloc[8:].apply(
    lambda row: func_despesas(row['n_alunos'] - taxa_de_aumento_depois_agosto),
    axis=1,
)
mes_a_mes['despesas'] = pd.concat([despesas_ate_agosto, despesas_depois_agosto])
mes_a_mes['despesas'].iloc[0] = despesas_janeiro['valor'].sum()

mes_a_mes['lucro'] = mes_a_mes['mensalidades'] - mes_a_mes['despesas']

mes_a_mes['acumulado'] = mes_a_mes['lucro'].cumsum()

########################################################################################
# Visualização da tabela.

fundo_do_poco = mes_a_mes['acumulado'].idxmin()

def highlight_rows(row):
    if row.name == fundo_do_poco:
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
