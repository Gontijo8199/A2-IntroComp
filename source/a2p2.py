import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
#from scipy.stats import gaussian_kde
#from matplotlib.lines import Line2D

import math

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

def grafico3():
        
    df = dsessao.groupby('filme_id')[['publico', 'sala_id']].sum().reset_index()
    dfm = dfilme.merge(df, left_on='id', right_on='filme_id')

    dfm_pais_publico = dfm.groupby('pais_origem')['publico'].sum().reset_index().fillna(0)
    dfm_pais_publico = dfm_pais_publico.sort_values('publico', ascending=False).head(10)

    top3_paises = dfm_pais_publico.head(3)['pais_origem'].tolist()
    dfm_pais_publico['top3'] = dfm_pais_publico['pais_origem'].apply(lambda x: 'Top 3' if x in top3_paises else 'Outros')

    plt.yscale('log')

    sns.barplot(dfm_pais_publico, x='pais_origem', y='publico', hue='top3', palette=[ 'sandybrown', 'skyblue'] )
    plt.ylabel("Público", fontsize=16, loc='top', rotation=0)
    plt.xlabel("País", fontsize=16)
    plt.grid(True, linestyle='--',zorder=1)
    plt.legend().remove()
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=14)
    plt.title("Top 10 Países por bilheteria", fontsize=18)

    plt.show()

def grafico4():
    df = dsessao.merge(dsala, left_on='sala_id', right_on='id')
    df = df.merge(dcomplexo, left_on='from_complexo', right_on='id')

    top_cidades = df.groupby('municipio', as_index=False)['publico'].sum()
    top_cidades = top_cidades.sort_values('publico', ascending=False).head(10)

    top_cidades['top3'] = ['Top 3' if i < 3 else 'Outras' for i in range(len(top_cidades))]

    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_cidades, y='municipio', x='publico', hue='top3', palette=['green', 'blue'])

    plt.xscale('log')  
    plt.xlabel("Público", fontsize=16)
    plt.ylabel("Cidade", fontsize=16)
    plt.grid(True, axis='x', linestyle='--', zorder=1)
    plt.legend().remove()
    plt.xticks(fontsize=13)
    plt.yticks(fontsize=14)
    plt.title("Top 10 Cidades por Bilheteria (Escala Log)", fontsize=18)
    plt.tight_layout()
    plt.show()


''' apoio para a tabela de cores'''

def plot_colortable(colors, *, ncols=4, sort_colors=True):

    cell_width = 212
    cell_height = 22
    swatch_width = 48
    margin = 12

    # Sort colors by hue, saturation, value and name.
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

def main():
    # grafico1()
    # grafico2()
    
    
    #plot_colortable(mcolors.CSS4_COLORS)
    #plt.show()
    
    #grafico3()
    return 0
if __name__ == "__main__":
    main()