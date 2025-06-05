AUTORES = ['Nathan Loose Kuipper', 'Rafael Gontijo Ferreira']

import pandas as pd 
import sqlite3
from pathlib import Path
import ModuloA2 as a2

PATH =  Path(__file__).parent # bilheteria.db na mesma pasta que esse arquivo


'''
1. Qual o total de bilheteria de todos os filmes, ou seja, o público que foi aos
filmes listados?
'''


def questao1():
    
    dsessao = a2.carrega_tabela(PATH / 'bilheteria.db', 'sessao')
    dfsessao = dsessao.groupby(by=['filme_id'])['publico'].sum().reset_index()

    dfilme = a2.carrega_tabela(PATH / 'bilheteria.db', 'filme')
    
    map_titulo = lambda x: dfilme.loc[dfilme['id'] == x, 'titulo_original'].item()
    dfsessao['filme_id'] =  dfsessao['filme_id'].map(map_titulo).astype(str)
    
    return dfsessao

'''
2. Qual o filme de maior bilheteria em 2023, por país de origem?
'''

def questao2():
    dfilme = a2.carrega_tabela(PATH / 'bilheteria.db', 'filme')
    dsessao = a2.carrega_tabela(PATH / 'bilheteria.db', 'sessao')
    
    dfsessao = dsessao.groupby(by=['filme_id'])['publico'].sum().reset_index()
    
    merged_df = dfilme.merge(dfsessao, left_on='id', right_on='filme_id', how='left')
    
    merged_df['publico'] = merged_df['publico'].fillna(0)
    
    paises = merged_df['pais_origem'].unique()
    dic = {}
    
    for pais in paises:
        most_viewed_film = merged_df[merged_df['pais_origem'] == pais].sort_values(by='publico', ascending=False).iloc[0]
        dic[pais] = {
            'nome': dfilme.loc[dfilme['id'] == most_viewed_film['filme_id'], 'titulo_original'].item(),
            'publico': int(most_viewed_film['publico'])
        }
    
    return dic # modo de retorno não especificado, vou priorizar dicionario para caso precise separar por pais (key)


    


'''
3. Crie um dataframe com as 100 cidades com maior bilheteria em 2023,
ordenadas de forma decrescente de bilheteria.
'''

def questao3():
    resultado = 0 
    return resultado

'''
4. Qual o filme com maior bilheteria em cada cidade? Retorne um dataframe
com as colunas CIDADE, FILME e BILHETERIA.
'''

def questao4():
    return 0
    
    

'''
5. Quais as cidades com as maiores bilheterias para filmes brasileiros? Ao
contar a bilheteria de filmes brasileiros, também some as bilheterias
de filmes estrangeiros. Retorne um dataframe com as colunas CIDADE,
BILHETERIA_BR, BILHETERIA_ESTRANGEIRA
'''  

def questao5():
    resultado = 0 
    return resultado

def main():
    # questao1()
    #print("Questão 1: \n", questao1())
    # questao2()
    #print("Questão 2: \n", questao2())
    
    questao4()
    return 0

if __name__ == '__main__':
    main()