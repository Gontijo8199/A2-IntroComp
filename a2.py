AUTORES = ['Nathan Loose Kuipper', 'Rafael Gontijo Ferreira']

import pandas as pd 
import sqlite3
 

def queryconn(database, query):
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        # [('distribuidora',), ('filme',), ('grupo_exibidor',), ('exibidor',), ('complexo',), ('sala',), ('sessao',)]

        df = pd.read_sql_query(query, conn)
        
        return df
    


'''
1. Qual o total de bilheteria de todos os filmes, ou seja, o público que foi aos
filmes listados?
'''


def questao1():
    dsessao = queryconn('bilheteria.db', 'select * from sessao')
    dfsessao = dsessao.groupby(by=['filme_id'])['publico'].sum().reset_index()

    dfilme = queryconn('bilheteria.db', 'select * from filme')
    #mapper = dfilme.groupby(by=['id'])['titulo_original']


    dic = { }
    for i in dfsessao['filme_id']:
        dic[i] = dfsessao.loc[dfsessao['filme_id'] == i, 'publico'].item()

    resultado = dic
    # dff['filme_id'] = map(lambda x: ... )
    return resultado


questao1()
'''
2. Qual o filme de maior bilheteria em 2023, por país de origem?
'''

def questao2():
    resultado = 0 
    return resultado

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