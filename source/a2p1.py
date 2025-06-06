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
    
    return pd.DataFrame(dic) 


    


'''
3. Crie um dataframe com as 100 cidades com maior bilheteria em 2023,
ordenadas de forma decrescente de bilheteria.
'''

def questao3():
    # Carregar os dataframes que vou utilizar
    dsessao = a2.carrega_tabela(PATH / 'bilheteria.db', 'sessao')
    dsala = a2.carrega_tabela(PATH / 'bilheteria.db', 'sala')[['id', 'from_complexo']]
    dcomplexo = a2.carrega_tabela(PATH / 'bilheteria.db', 'complexo')[['id', 'municipio']]

    # junta as sessões com as salas
    df = dsessao.merge(dsala, left_on='sala_id', right_on='id', how='left')

    # junta o dataframe anterior com o dcomplexo para obter as cidades
    df = df.merge(dcomplexo, left_on='from_complexo', right_on='id', how='left')

    # Agrupa por cidade e somo com o público
    cidades = df.groupby('municipio', as_index=False)['publico'].sum()

    #renomeio pra ficar bonitinho kkkk
    cidades = cidades.rename(columns={'publico': 'BILHETERIA'})

    # Selecionar as 100 cidades com a maior bilheteria
    top100 = cidades.sort_values('BILHETERIA', ascending=False).head(100)

    return top100




'''
4. Qual o filme com maior bilheteria em cada cidade? Retorne um dataframe
com as colunas CIDADE, FILME e BILHETERIA.
'''

def questao4():
    
    dsessao = a2.carrega_tabela(PATH / 'bilheteria.db', 'sessao')
    dsala = a2.carrega_tabela(PATH / 'bilheteria.db', 'sala')[['id', 'from_complexo']]
    dcomplexo = a2.carrega_tabela(PATH / 'bilheteria.db', 'complexo')[['id', 'municipio']]

    dfilme = a2.carrega_tabela(PATH / 'bilheteria.db', 'filme')[['id', 'titulo_original']]

    df = dsessao.merge(dsala, left_on='sala_id', right_on='id', how='left')
    df = df.rename(columns={'id_x': 'sessao_id', 'id_y': 'sala_id'})  

    df = df.merge(dcomplexo, left_on='from_complexo', right_on='id', how='left')
    df = df.rename(columns={'municipio': 'CIDADE'})
    
    df = df.merge(dfilme, left_on='filme_id', right_on='id', how='left')
    df = df.rename(columns={'titulo_original': 'FILME'})

    bilheteria = df.groupby(['CIDADE', 'FILME'], as_index=False)['publico'].sum()
    bilheteria = bilheteria.rename(columns={'publico': 'BILHETERIA'})

    resultado = bilheteria.sort_values('BILHETERIA', ascending=False).groupby('CIDADE').head(1)

    return resultado[['CIDADE', 'FILME', 'BILHETERIA']]


    
'''
5. Quais as cidades com as maiores bilheterias para filmes brasileiros? Ao
contar a bilheteria de filmes brasileiros, também some as bilheterias
de filmes estrangeiros. Retorne um dataframe com as colunas CIDADE,
BILHETERIA_BR, BILHETERIA_ESTRANGEIRA
'''  

def questao5():
    # Carregar os dataframes que vou utilizar
    dsessao = a2.carrega_tabela(PATH / 'bilheteria.db', 'sessao')
    dsala = a2.carrega_tabela(PATH / 'bilheteria.db', 'sala')[['id', 'from_complexo']]
    dcomplexo = a2.carrega_tabela(PATH / 'bilheteria.db', 'complexo')[['id', 'municipio']]
    dfilme = a2.carrega_tabela(PATH / 'bilheteria.db', 'filme')[['id', 'pais_origem']]

    # Junta a sessão com a sala
    df = dsessao.merge(dsala, left_on='sala_id', right_on='id', how='left')
    df = df.rename(columns={'id_x': 'sessao_id', 'id_y': 'sala_id'})

    # Juntar com complexo para obter a cidade
    df = df.merge(dcomplexo, left_on='from_complexo', right_on='id', how='left')
    df = df.rename(columns={'municipio': 'CIDADE'})

    # Juntar com filme para saber de qual cidade é qual
    df = df.merge(dfilme, left_on='filme_id', right_on='id', how='left')

    # Cria uma coluna de tipo do filme (se é BR ou ESTRANGEIRO)
    df['tipo'] = df['pais_origem'].apply(lambda x: 'BR' if isinstance(x, str) and 'BRASIL' in x else 'ESTRANGEIRO')
    print(df)

    # Agrupar por cidade e tipo de filme
    bilheteria = df.groupby(['CIDADE', 'tipo'], as_index=False)['publico'].sum()
    print(bilheteria)

    # Pivotar a tabela para colunas separadas
    tabela_final = bilheteria.pivot(index='CIDADE', columns='tipo', values='publico').fillna(0)

    # Renomeia as colunas do jeitinho que o professor quer
    tabela_final = tabela_final.rename(columns={'BR': 'BILHETERIA_BR', 'ESTRANGEIRO': 'BILHETERIA_ESTRANGEIRA'}).reset_index()
    

    # hello_world('print')
    return tabela_final




def main():
    # questao1()
    #print("Questão 1: \n", questao1())
    # questao2()
    # print("Questão 2: \n", questao2())
    # questao3()
    #print("Questão 3: \n", questao3())
    #questao4()
    #print("Questão 4: \n", questao4())
    questao5()
    #print("Questão 5: \n", questao5())
    return 0

if __name__ == '__main__':
    main()