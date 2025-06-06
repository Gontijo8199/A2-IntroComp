import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
#from scipy.stats import gaussian_kde
#from matplotlib.lines import Line2D
from pathlib import Path
import ModuloA2 as a2

PATH =  Path(__file__).parent # bilheteria.db na mesma pasta que esse arquivo

dsessao = a2.carrega_tabela(PATH / 'bilheteria.db', 'sessao')
dsala = a2.carrega_tabela(PATH / 'bilheteria.db', 'sala')
dcomplexo = a2.carrega_tabela(PATH / 'bilheteria.db', 'complexo')
dexibidor = a2.carrega_tabela(PATH / 'bilheteria.db', 'exibidor')
ddistribuidora = a2.carrega_tabela(PATH / 'bilheteria.db', 'distribuidora')
dgrupo = a2.carrega_tabela(PATH / 'bilheteria.db', 'grupo_exibidor')

# grafico 1
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