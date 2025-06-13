import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
#from scipy.stats import gaussian_kde
#from matplotlib.lines import Line2D

import math
import matplotlib.ticker as mticker

import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle

from pathlib import Path
import ModuloA2 as a2
import statsmodels.api as sm
PATH =  Path(__file__).parent # bilheteria.db na mesma pasta que esse arquivo

dsessao = a2.carrega_tabela(PATH / 'bilheteria.db', 'sessao')
dsala = a2.carrega_tabela(PATH / 'bilheteria.db', 'sala')
dcomplexo = a2.carrega_tabela(PATH / 'bilheteria.db', 'complexo')
dexibidor = a2.carrega_tabela(PATH / 'bilheteria.db', 'exibidor')
ddistribuidora = a2.carrega_tabela(PATH / 'bilheteria.db', 'distribuidora')
dgrupo = a2.carrega_tabela(PATH / 'bilheteria.db', 'grupo_exibidor')
dfilme = a2.carrega_tabela(PATH / 'bilheteria.db', 'filme')


# grafico 1

def grafico1():
    df = dsessao.groupby(by=['data_exibicao'])['publico'].sum().reset_index()
    df['data_exibicao'] = pd.to_datetime(df['data_exibicao'], format="%d/%m/%Y")

    df['mes'] = df['data_exibicao'].dt.to_period('M').astype(str)
    df = df.sort_values(by=['data_exibicao'])
    plt.figure(figsize=(12, 6))
    sns.set_style("ticks")
    plt.title('Público por Data de Exibição', fontsize=18)
    plt.xlabel('Data de Exibição', fontsize=16)
    plt.ylabel('Público', rotation=0, loc='top', fontsize=16)
    plt.xticks(rotation=0, fontsize=14)
    plt.yticks(fontsize=14)
    plt.grid(True, linestyle='--', linewidth=0.6)

    sns.lineplot(x="mes", y="publico",
                 data=df, marker='o')


    plt.show()

# grafico 2
def grafico2():
    dsessao['sala_id'] = 1  

    df = dsessao.groupby('filme_id')[['publico', 'sala_id']].sum().reset_index()

    dfm = dfilme.merge(df, left_on='id', right_on='filme_id')

    dfm['pais_origem'] = dfm['pais_origem'].apply(lambda x: 'ESTADOS UNIDOS' if x == 'ESTADOS UNIDOS' else 'ESTRANGEIRO')

    dfm.rename(columns={'sala_id': 'qtd_salas'}, inplace=True)

    limite_salas = 10
    dfm_filtrado = dfm[(dfm['qtd_salas'] >= limite_salas) &
                       (dfm['qtd_salas'] > 0) &
                       (dfm['publico'] > 0)].copy()

    dfm_filtrado['log_publico'] = np.log10(dfm_filtrado['publico'])
    dfm_filtrado['log_salas'] = np.log10(dfm_filtrado['qtd_salas'])

    plt.figure(figsize=(10, 6))
    sns.set(style="ticks")

    cores = {'ESTADOS UNIDOS': 'tab:blue', 'ESTRANGEIRO': 'tab:green'}
    for origem, grupo in dfm_filtrado.groupby('pais_origem'):
        x = grupo['log_publico']
        y = grupo['log_salas']


        X = sm.add_constant(x)
        model = sm.OLS(y, X).fit()
        a = model.params[1]
        b = model.params[0]


        sns.scatterplot(x=grupo['publico'], y=grupo['qtd_salas'],
                        label=origem, color=cores[origem], alpha=0.3)


        x_vals = np.linspace(grupo['publico'].min(), grupo['publico'].max(), 100)
        y_vals = 10 ** (a * np.log10(x_vals) + b)
        plt.plot(x_vals, y_vals, color=cores[origem], linestyle='--')




    plt.xscale('log')
    plt.yscale('log')

    plt.grid(True, linestyle='--', linewidth=0.6)
    plt.xticks(rotation=0, fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel('Público (log)', fontsize=16)
    plt.ylabel('Salas (log)', fontsize=16, loc='top', rotation=0)
    plt.title(f'Público vs. Quantidade de Salas (≥ {limite_salas} salas)', fontsize=18)
    plt.tight_layout()
    plt.legend()
    plt.show()

# grafico 3

def grafico3():
    
    cor_brasil = 'coral'
    cor_cidade = 'lightblue'
    cor_outros = 'lightgray'

    df1 = dsessao.groupby('filme_id')[['publico', 'sala_id']].sum().reset_index()
    dfm = dfilme.merge(df1, left_on='id', right_on='filme_id')

    dfm_pais_publico = dfm.groupby('pais_origem')['publico'].sum().reset_index()
    dfm_pais_publico = dfm_pais_publico.sort_values('publico', ascending=False).head(10)
    dfm_pais_publico['destaque'] = dfm_pais_publico['pais_origem'].apply(
        lambda x: 'BRASIL' if x.upper() == 'BRASIL' else 'OUTROS'
    )

    df2 = dsessao.merge(dsala, left_on='sala_id', right_on='id')
    df2 = df2.merge(dcomplexo, left_on='from_complexo', right_on='id')

    top_cidades = df2.groupby('municipio', as_index=False)['publico'].sum()
    top_cidades = top_cidades.sort_values('publico', ascending=False).head(10)
    top_cidades['categoria'] = ['Top 3' if i < 3 else 'Outras' for i in range(len(top_cidades))]

    fig, axes = plt.subplots(1, 2, figsize=(20, 8))
    fig.suptitle("Cinematografia Brasileira: Visão Global e Nacional", fontsize=20)

    sns.barplot(
        ax=axes[0],
        data=dfm_pais_publico,
        y='pais_origem',
        x='publico',
        hue='destaque',
        dodge=False,
        palette={'BRASIL': cor_brasil, 'OUTROS': cor_outros}
    )
    axes[0].set_xscale('log')
    axes[0].set_title("Top 10 Bilheterias Globais", fontsize=18)
    axes[0].set_xlabel("Bilheteria (log)", fontsize=16)
    axes[0].tick_params(axis='y', labelsize=12)
    axes[0].tick_params(axis='x', labelsize=12)
    axes[0].set_ylabel(" ")
    axes[0].legend().remove()
    axes[0].grid(True, linestyle='--', alpha=0.6)

    sns.barplot(
        ax=axes[1],
        data=top_cidades,
        y='municipio',
        x='publico',
        hue='categoria',
        dodge=False,
        palette={'Top 3': cor_cidade, 'Outras': cor_outros}
    )
    axes[1].set_title("Top 10 Bilheterias Nacionais", fontsize=18)

    max_publico = top_cidades['publico'].max()
    margem = max_publico * 0.20  
    axes[1].set_xlim(0, max_publico + margem)

    axes[1].set_xlabel("Bilheteria", fontsize=16)
    axes[1].tick_params(axis='y', labelsize=12)
    axes[1].tick_params(axis='x', labelsize=12)
    axes[1].set_ylabel(" ")
    axes[1].legend().remove()
    axes[1].grid(True, linestyle='--', alpha=0.6)

    xlim0 = axes[0].get_xlim()
    for i, pais in enumerate(dfm_pais_publico['pais_origem']):
        publico = dfm_pais_publico.loc[dfm_pais_publico['pais_origem'] == pais, 'publico'].values[0]
        if pais.upper() == 'BRASIL':
            y = i
            x = publico
            deslocamento = (xlim0[1] - xlim0[0]) * 0.002
            x_text = x + deslocamento
            axes[0].text(
                x_text,
                y,
                f"{int(publico):,}",
                va='center',
                ha='left',
                fontsize=12,
                color=cor_brasil,
                fontweight='bold'
            )

    xlim1 = axes[1].get_xlim()
    for i, row in top_cidades.iterrows():
        if row['categoria'] == 'Top 3':
            y = top_cidades.index.get_loc(i)
            x = row['publico']
            deslocamento = (xlim1[1] - xlim1[0]) * 0.02  
            x_text = x + deslocamento
            axes[1].text(
                x_text,
                y,
                f"{int(x):,}",
                va='center',
                ha='left',
                fontsize=12,
                color=cor_cidade,
                fontweight='bold'
            )

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()


# grafico 4
def grafico4():
    dfm = dsessao.copy()
    dfm = dfm.merge(dfilme, left_on='filme_id', right_on='id', suffixes=('', '_filme'))
    dfm = dfm.merge(dsala, left_on='sala_id', right_on='id', suffixes=('', '_sala'))
    dfm = dfm.merge(dcomplexo, left_on='from_complexo', right_on='id', suffixes=('', '_complexo'))

    dfm_brasil = dfm[dfm['pais_origem'].str.upper() == 'BRASIL'].copy()
    dfm_brasil['data_exibicao'] = pd.to_datetime(dfm_brasil['data_exibicao'], format="%d/%m/%Y")
    dfm_brasil['data_mes'] = dfm_brasil['data_exibicao'].dt.month

    agrupado = dfm_brasil.groupby(['filme_id', 'data_mes'])['publico'].sum().reset_index()


    plt.figure(figsize=(14, 7))
    sns.boxplot(data=agrupado, x='data_mes', y='publico')
    plt.xlabel("Mês")
    plt.yscale('log')
    plt.ylabel("Público por Filme")
    plt.title("Distribuição do Público por Filme Brasileiro em Cada Mês")
    plt.grid(True, axis='y', linestyle='--', alpha=0.6)
    plt.show()


''' apoio para a tabela de cores'''

def plot_colortable(colors, *, ncols=4, sort_colors=True):

    cell_width = 212
    cell_height = 22
    swatch_width = 48
    margin = 12

    if sort_colors is True:
        names = sorted(
            colors, key=lambda c: tuple(mcolors.rgb_to_hsv(mcolors.to_rgb(c))))
    else:
        names = list(colors)

    n = len(names)
    nrows = math.ceil(n / ncols)

    width = cell_width * ncols + 2 * margin
    height = cell_height * nrows + 2 * margin
    dpi = 72

    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)
    fig.subplots_adjust(margin/width, margin/height,
                        (width-margin)/width, (height-margin)/height)
    ax.set_xlim(0, cell_width * ncols)
    ax.set_ylim(cell_height * (nrows-0.5), -cell_height/2.)
    ax.yaxis.set_visible(False)
    ax.xaxis.set_visible(False)
    ax.set_axis_off()

    for i, name in enumerate(names):
        row = i % nrows
        col = i // nrows
        y = row * cell_height

        swatch_start_x = cell_width * col
        text_pos_x = cell_width * col + swatch_width + 7

        ax.text(text_pos_x, y, name, fontsize=14,
                horizontalalignment='left',
                verticalalignment='center')

        ax.add_patch(
            Rectangle(xy=(swatch_start_x, y-9), width=swatch_width,
                      height=18, facecolor=colors[name], edgecolor='0.7')
        )

    return fig


''' tabelas '''

def tabela1():
    
    dfm = dsessao.copy()
    dfm = dfm.merge(dfilme, left_on='filme_id', right_on='id', suffixes=('', '_filme'))
    dfm = dfm.merge(dsala, left_on='sala_id', right_on='id', suffixes=('', '_sala'))
    dfm = dfm.merge(dcomplexo, left_on='from_complexo', right_on='id', suffixes=('', '_complexo'))
    
    dfm['data_exibicao'] = pd.to_datetime(dfm['data_exibicao'], format="%d/%m/%Y")
    tempo_util_filme = (
    dfm.groupby('filme_id')['data_exibicao']
    .agg(['min', 'max'])
    .reset_index()
    )

    tempo_util_filme['tempo_util_dias'] = (tempo_util_filme['max'] - tempo_util_filme['min']).dt.days


    filme_pais = dfm[['filme_id', 'pais_origem']].drop_duplicates()

    tempo_util_filme = tempo_util_filme.merge(filme_pais, on='filme_id', how='left')


    tempo_util_por_pais = (
        tempo_util_filme.groupby('pais_origem')['tempo_util_dias']
        .mean()
        .reset_index()
        .rename(columns={'tempo_util_dias': 'tempo_util_medio_dias'})
    )

    tempo_util_por_pais = tempo_util_por_pais.sort_values('tempo_util_medio_dias', ascending=False).reset_index(drop=True)

    print(tempo_util_por_pais)
       



def tabela2():

    
    dfm = dsessao.copy()
    dfm = dfm.merge(dfilme, left_on='filme_id', right_on='id', suffixes=('', '_filme'))
    dfm = dfm.merge(dsala, left_on='sala_id', right_on='id', suffixes=('', '_sala'))
    dfm = dfm.merge(dcomplexo, left_on='from_complexo', right_on='id', suffixes=('', '_complexo'))
    
    dfm['data_exibicao'] = pd.to_datetime(dfm['data_exibicao'], format="%d/%m/%Y")
    
    dfm['dia_semana'] = dfm['data_exibicao'].dt.day_name()

    def moda_dia(series):
        try:
            return series.mode().iloc[0] if not series.mode().empty else None
        except:
            return None


    resumo_filmes = (
        dfm.groupby(['filme_id', 'titulo_br'])
        .agg(
            media_publico=('publico', 'mean'),
            desvio_padrao_publico=('publico', 'std'),
            moda_dia_semana=('dia_semana', moda_dia)
        )
        .reset_index()
    )

    resumo_filmes = resumo_filmes.sort_values('media_publico', ascending=False).reset_index(drop=True)

    print(resumo_filmes)
    #print(resumo_filmes.head(10))

    

def tabela3():
    ...
    return 0


def main():
    # grafico1()
    # grafico2()
    # grafico3()
    # grafico4() TODO: Refazer o gráfico 4
    
    
    #plot_colortable(mcolors.CSS4_COLORS)
    #plt.show()
    
    #tabela1()
    tabela2()
    
    return 0

if __name__ == "__main__":
    main()