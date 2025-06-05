import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import gaussian_kde
from matplotlib.lines import Line2D
import ModuloA2

# bases de dados

dsessao = a2.carrega_tabela(PATH / 'bilheteria.db', 'sessao')
dsala = a2.carrega_tabela(PATH / 'bilheteria.db', 'sala')
dcomplexo = a2.carrega_tabela(PATH / 'bilheteria.db', 'complexo')
dexibidor = a2.carrega_tabela(PATH / 'bilheteria.db', 'exibidor')
ddistribuidora = a2.carrega_tabela(PATH / 'bilheteria.db', 'distribuidora')
dgrupo = a2.carrega_tabela(PATH / 'bilheteria.db', 'grupo_exibidor')

