import math
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.patches import Rectangle
import seaborn as sns
import statsmodels.api as sm

import ModuloA2 as a2

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

    df['semana'] = df['data_exibicao'].dt.to_period('W').apply(lambda r: r.start_time)

    df_semana = df.groupby('semana')['publico'].agg(['mean', 'min', 'max']).reset_index()
    df_semana = df_semana.sort_values('semana')
    plt.figure(figsize=(12, 6))
    sns.set_style("ticks")
    plt.title('Média de Público por Semana', fontsize=20)
    plt.xlabel('Mês', fontsize=18)
    plt.ylabel('Público Médio', rotation=0, loc='top', fontsize=18)
    plt.xticks(rotation=0, fontsize=16)
    plt.yticks(fontsize=16)
    plt.ticklabel_format(style='plain', axis='y')
    plt.grid(True, linestyle='--', linewidth=0.6)

    plt.fill_between(
        df_semana['semana'],
        df_semana['min'],
        df_semana['max'],
        color='lightgray',
        alpha=0.4,
        label='Faixa entre Mínimo e Máximo'
    )

    sns.lineplot(x="semana", y="mean", data=df_semana, marker='o', label='Média Semanal')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())

    plt.legend()
    plt.tight_layout()
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

    cores = {'ESTADOS UNIDOS': 'blue', 'ESTRANGEIRO': 'orange'}
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
    plt.xticks(rotation=0, fontsize=14)    # Criar a coluna de categoria

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
    cor_cidade = 'lightskyblue'
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
    
    df2 = df2.merge(dfilme[['id', 'pais_origem']], left_on='filme_id', right_on='id', suffixes=('', '_filme'))
    
    df2_nacional = df2[df2['pais_origem'].str.upper() == 'BRASIL']
    
    top_cidades = df2_nacional.groupby('municipio', as_index=False)['publico'].sum()
    
    top_cidades = top_cidades.sort_values('publico', ascending=False).head(10)
    
    top_cidades['categoria'] = ['Top 3' if i < 3 else 'Outras' for i in range(len(top_cidades))]
    



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
    axes[0].set_title("Filmes Consumidos no Cinema Brasileiro por País de Origem", fontsize=18)
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
    axes[1].set_title("Consumo de Filmes Brasileiros por Unidade da Federação", fontsize=18)

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
    dfm['data_exibicao'] = pd.to_datetime(dfm['data_exibicao'], format="%d/%m/%Y")

    tempo_util_filme = (
        dfm.groupby('filme_id')['data_exibicao']
        .agg(['min', 'max'])
        .reset_index()
    )
    tempo_util_filme['tempo_util_dias'] = (tempo_util_filme['max'] - tempo_util_filme['min']).dt.days

    filme_pais = dfm[['filme_id', 'pais_origem']].drop_duplicates()
    tempo_util_filme = tempo_util_filme.merge(filme_pais, on='filme_id', how='left')

    pais_para_continente = {
        'SUÉCIA': 'Europa',
        'CHINA': 'Ásia',
        'BELARUS (BIELORUSSIA)': 'Europa',
        'ESPANHA': 'Europa',
        'IRÃ': 'Ásia',
        'ESTADOS UNIDOS': 'América do Norte',
        'CANADÁ': 'América do Norte',
        'POLÔNIA': 'Europa',
        'ÁUSTRIA': 'Europa',
        'BÉLGICA': 'Europa',
        'COLÔMBIA': 'América do Sul',
        'ALEMANHA': 'Europa',
        'EMIRADOS ÁRABES UNIDOS': 'Ásia',
        'PANAMÁ': 'América do Sul',
        'HOLANDA': 'Europa',
        'ARGENTINA': 'América do Sul',
        'REINO UNIDO': 'Europa',
        'FRANÇA': 'Europa',
        'DINAMARCA': 'Europa',
        'AUSTRÁLIA': 'Oceania',
        'ESTÔNIA': 'Europa',
        'BRASIL': 'América do Sul',
        'ITÁLIA': 'Europa',
        'ARGÉLIA': 'África',
        'FILIPINAS': 'Ásia',
        'UCRÂNIA': 'Europa',
        'RÚSSIA': 'Europa',
        'JAPÃO': 'Ásia',
        'ÍNDIA': 'Ásia',
        'CHILE': 'América do Sul',
        'IRLANDA': 'Europa',
        'INGLATERRA': 'Europa',
        'REPÚBLICA DOMINICANA': 'América do Sul',
        'SUÍÇA': 'Europa',
        'PORTUGAL': 'Europa',
        'REPÚBLICA TCHECA': 'Europa',
        'CORÉIA DO SUL': 'Ásia',
        'ESLOVÊNIA': 'Europa',
        'CORÉIA DO NORTE': 'Ásia',
        'PERU': 'América do Sul',
    } # deu trabalho
    tempo_util_filme['continente'] = tempo_util_filme['pais_origem'].map(pais_para_continente)
    tempo_util_filme = tempo_util_filme.dropna(subset=['continente'])

    max_dias = tempo_util_filme['tempo_util_dias'].max()
    dias = range(max_dias, -1, -1)

    plt.figure(figsize=(14, 7))

    continentes = tempo_util_filme['continente'].unique()

    for continente in continentes:
        filmes_continente = tempo_util_filme[tempo_util_filme['continente'] == continente]
        acumulado = [(filmes_continente['tempo_util_dias'] >= d).sum() for d in dias]
        plt.plot(dias, acumulado, label=continente)

    plt.title('Distribuição decrescente de filmes por tempo útil, por continente', fontsize=20)
    plt.xlabel('Tempo útil do filme (dias)', fontsize=18)
    plt.ylabel('Filmes', loc='top', rotation=0, fontsize=18)
    plt.legend(title='Continente', fontsize=12)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(title=None)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
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
    dfm['semana_mes'] = ((dfm['data_exibicao'].dt.day - 1) // 7) + 1

    dfm['dia_semana'] = dfm['data_exibicao'].dt.day_name()
    dfm['mes'] = dfm['data_exibicao'].dt.month

    def moda_dia(series):
        try:
            return series.mode().iloc[0] if not series.mode().empty else None
        except:
            return None

    
    def moda_geral(series):
        try:
            return int(series.mode().iloc[0]) if not series.mode().empty else None
        except:
            return None

    resumo_filmes = (
        dfm.groupby(['filme_id', 'titulo_br'])
        .agg(
            media_publico=('publico', 'mean'),
            desvio_padrao_publico=('publico', 'std'),
            moda_dia_semana=('dia_semana', moda_dia),
            moda_semana=('semana_mes', moda_geral),
            moda_mes=('mes', moda_geral)
        )
        .reset_index()
    )

    resumo_filmes = resumo_filmes.sort_values('media_publico', ascending=False).reset_index(drop=True)

    print(resumo_filmes)


def tabela3():
    dfm = dsessao.copy()
    dfm = dfm.merge(dfilme, left_on='filme_id', right_on='id', suffixes=('', '_filme'))
    dfm = dfm.merge(dsala, left_on='sala_id', right_on='id', suffixes=('', '_sala'))
    dfm = dfm.merge(dcomplexo, left_on='from_complexo', right_on='id', suffixes=('', '_complexo'))
    dfm = dfm.merge(ddistribuidora, left_on='from_distribuidora', right_on='id', suffixes=('', '_distribuidora'))

    dfm['data_exibicao'] = pd.to_datetime(dfm['data_exibicao'], format="%d/%m/%Y")

    tempo_util_filme = (
        dfm.groupby('filme_id')['data_exibicao']
        .agg(['min', 'max'])
        .reset_index()
    )
    tempo_util_filme['tempo_util_dias'] = (tempo_util_filme['max'] - tempo_util_filme['min']).dt.days

    filme_distribuidora = dfm[['filme_id', 'nome_distribuidora']].drop_duplicates()
    tempo_util_filme = tempo_util_filme.merge(filme_distribuidora, on='filme_id', how='left')

    resumo_distribuidora = (
        dfm.groupby('nome_distribuidora')
        .agg(
            total_publico=('publico', 'sum'),
            total_sessoes=('sala_id', 'count'),
            media_publico_sessao=('publico', 'mean'),
            desvio_padrao_publico=('publico', 'std'),
            qtd_filmes=('filme_id', pd.Series.nunique)
        )
        .reset_index()
    )

    media_tempo_util = (
        tempo_util_filme.groupby('nome_distribuidora')['tempo_util_dias']
        .mean()
        .reset_index()
        .rename(columns={'tempo_util_dias': 'media_tempo_util_dias'})
    )

    tabela_final = resumo_distribuidora.merge(media_tempo_util, on='nome_distribuidora', how='left')
    tabela_final = tabela_final.sort_values('total_publico', ascending=False).reset_index(drop=True)

    print(tabela_final.head(20))


def main():
    '''
    Chame as funções de plotagem individualmente:
    
    grafico1()
    grafico2()
    grafico3()
    grafico4() 
    
    '''

    
    #plot_colortable(mcolors.CSS4_COLORS)
    #plt.show()
    '''
    tabela1()
    tabela2()
    tabela3()
    '''
    print("Edite para selecionar qual gráfico ou tabela deve plotar.")

if __name__ == "__main__":
    main()