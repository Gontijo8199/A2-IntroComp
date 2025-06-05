AUTORES = ['Nathan Loose Kuipper', 'Rafael Gontijo Ferreira']

import pandas as pd 
import sqlite3
from pathlib import Path

PATH =  Path(__file__).parent # bilheteria.db na mesma pasta que esse arquivo

def queryconn(database, query):
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        df = pd.read_sql_query(query, conn)
        
        return df
    


'''
1. Qual o total de bilheteria de todos os filmes, ou seja, o público que foi aos
filmes listados?
'''


def questao1():
    
    dsessao = queryconn(PATH / 'bilheteria.db', 'SELECT * FROM sessao')
    dfsessao = dsessao.groupby(by=['filme_id'])['publico'].sum().reset_index()

    dfilme = queryconn(PATH / 'bilheteria.db', 'SELECT * FROM filme')
    
    map_titulo = lambda x: dfilme.loc[dfilme['id'] == x, 'titulo_original'].item()
    dfsessao['filme_id'] =  dfsessao['filme_id'].map(map_titulo).astype(str)
    
    return dfsessao

'''
2. Qual o filme de maior bilheteria em 2023, por país de origem?
'''

def questao2():
    dfilme = queryconn(PATH / 'bilheteria.db', 'select * from filme')
    dsessao = queryconn(PATH / 'bilheteria.db', 'select * from sessao')
    
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
    
    return dic


    


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
    resultado = 0 
    return resultado

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
    # print("Questão 1: \n", questao1())
    # questao2()
    # print("Questão 2: \n", questao())
    
    return 0

if __name__ == '__main__':
    main()