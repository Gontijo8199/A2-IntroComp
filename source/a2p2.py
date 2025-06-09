import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
#from scipy.stats import gaussian_kde
#from matplotlib.lines import Line2D
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


def main():
    # grafico1()
    # grafico2()
    
    return 0
if __name__ == "__main__":
    main()