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


def questao1(database):
    
    dados = PATH / database

    dsessao = a2.carrega_tabela(dados, 'sessao')
    
    # agrupa por filme a soma dos publicos de todas as sessões
    dfsessao = dsessao.groupby(by=['filme_id'])['publico'].sum().reset_index() 

    dfilme = a2.carrega_tabela(dados, 'filme')
    
    map_titulo = lambda x: dfilme.loc[dfilme['id'] == x, 'titulo_original'].item() # id -> nome do filme
    dfsessao['filme_id'] =  dfsessao['filme_id'].map(map_titulo).astype(str)
    
    return dfsessao

'''
2. Qual o filme de maior bilheteria em 2023, por país de origem?
'''

def questao2(database):

    dados = PATH / database

    dfilme = a2.carrega_tabela(dados, 'filme')
    dsessao = a2.carrega_tabela(dados, 'sessao')

    # agrupa o dataframe para que fique filme e publico total

    dfsessao = dsessao.groupby(by=['filme_id'])['publico'].sum().reset_index()
    
    # merge dos dados da sessao com os dados do filme
    merged_df = dfilme.merge(dfsessao, left_on='id', right_on='filme_id', how='left')
    
    # preenche valores faltando
    merged_df['publico'] = merged_df['publico'].fillna(0)
    
    paises = merged_df['pais_origem'].unique()
    
    dic = {}
    
    for pais in paises:
        
        # define o que é o filme mais visualizado do pais e o separa usando .iloc
        
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

def questao3(database):

    dados = PATH / database
    
    dsessao = a2.carrega_tabela(dados, 'sessao')
    dsala = a2.carrega_tabela(dados, 'sala')[['id', 'from_complexo']]
    dcomplexo = a2.carrega_tabela(dados, 'complexo')[['id', 'municipio']]

    # junta as sessões com as salas
    df = dsessao.merge(dsala, left_on='sala_id', right_on='id', how='left')

    # junta o dataframe anterior com o dcomplexo para obter as cidades
    df = df.merge(dcomplexo, left_on='from_complexo', right_on='id', how='left')

    # Agrupa por cidade e somo com o público
    cidades = df.groupby('municipio', as_index=False)['publico'].sum()

    # renomeia
    cidades = cidades.rename(columns={'publico': 'BILHETERIA'})

    # Selecionar as 100 cidades com a maior bilheteria
    top100 = cidades.sort_values('BILHETERIA', ascending=False).head(100).reset_index(drop=True)

    return top100




'''
4. Qual o filme com maior bilheteria em cada cidade? Retorne um dataframe
com as colunas CIDADE, FILME e BILHETERIA.
'''

def questao4(database):

    dados = PATH / database
    
    dsessao = a2.carrega_tabela(dados, 'sessao')
    dsala = a2.carrega_tabela(dados, 'sala')[['id', 'from_complexo']]
    dcomplexo = a2.carrega_tabela(dados, 'complexo')[['id', 'municipio']]
    dfilme = a2.carrega_tabela(dados, 'filme')[['id', 'titulo_original']]

    # junta a tabela de sessão e sala
    df = dsessao.merge(dsala, left_on='sala_id', right_on='id', how='left')
    df = df.rename(columns={'id_x': 'sessao_id', 'id_y': 'sala_id'})  

    # junta os dados do complexo
    df = df.merge(dcomplexo, left_on='from_complexo', right_on='id', how='left')
    df = df.rename(columns={'municipio': 'CIDADE'})
    
    # junta os dados do filme
    df = df.merge(dfilme, left_on='filme_id', right_on='id', how='left')
    df = df.rename(columns={'titulo_original': 'FILME'})

    # agrupa a soma dos publicos por cidade e filme exibido
    bilheteria = df.groupby(['CIDADE', 'FILME'], as_index=False)['publico'].sum()
    bilheteria = bilheteria.rename(columns={'publico': 'BILHETERIA'})

    # pega o top 1 de cada cidade
    resultado = bilheteria.sort_values('BILHETERIA', ascending=False).groupby('CIDADE').head(1)

    return resultado[['CIDADE', 'FILME', 'BILHETERIA']].reset_index(drop=True)


    
'''
5. Quais as cidades com as maiores bilheterias para filmes brasileiros? Ao
contar a bilheteria de filmes brasileiros, também some as bilheterias
de filmes estrangeiros. Retorne um dataframe com as colunas CIDADE,
BILHETERIA_BR, BILHETERIA_ESTRANGEIRA
'''  

def questao5(database):
    dados = PATH / database

    dsessao = a2.carrega_tabela(dados, 'sessao')
    dsala = a2.carrega_tabela(dados, 'sala')[['id', 'from_complexo']]
    dcomplexo = a2.carrega_tabela(dados, 'complexo')[['id', 'municipio']]
    dfilme = a2.carrega_tabela(dados, 'filme')[['id', 'pais_origem']]

    # Junta a sessão com a sala
    df = dsessao.merge(dsala, left_on='sala_id', right_on='id', how='left')
    df = df.rename(columns={'id_x': 'sessao_id', 'id_y': 'sala_id'})

    # Junta com complexo para pegar cidade
    df = df.merge(dcomplexo, left_on='from_complexo', right_on='id', how='left')
    df = df.rename(columns={'municipio': 'CIDADE'})

    # Junta com filme para saber o país de origem
    df = df.merge(dfilme, left_on='filme_id', right_on='id', how='left')

    # Classificar tipo de filme
    def classificar_tipo(pais):
        if isinstance(pais, str):
            paises = [p.strip().upper() for p in pais.split(',')]
            if len(paises) == 1 and paises[0] == 'BRASIL':
                return 'BR'
        return 'ESTRANGEIRO'

    df['tipo'] = df['pais_origem'].apply(classificar_tipo)

    bilheteria_estrangeira = (
        df[df['tipo'] == 'ESTRANGEIRO']
        .groupby('CIDADE', as_index=False)['publico']
        .sum()
        .rename(columns={'publico': 'BILHETERIA_ESTRANGEIRA'})
    )

    bilheteria_total = (
        df.groupby('CIDADE', as_index=False)['publico']
        .sum()
        .rename(columns={'publico': 'BILHETERIA_BR'})
    )

    resultado = bilheteria_total.merge(
        bilheteria_estrangeira, on='CIDADE', how='left'
    ).fillna(0)

    resultado['BILHETERIA_ESTRANGEIRA'] = resultado['BILHETERIA_ESTRANGEIRA'].astype(int)
    resultado['BILHETERIA_BR'] = resultado['BILHETERIA_BR'].astype(int)

    resultado = resultado.sort_values(by='BILHETERIA_BR', ascending=False).reset_index(drop=True)

    return resultado


def main():
    
    # questao1()
    print("Questão 1: \n", questao1('bilheteria.db'))
    # questao2()
    print("Questão 2: \n", questao2('bilheteria.db'))
    # questao3()
    print("Questão 3: \n", questao3('bilheteria.db'))
    # questao4()
    print("Questão 4: \n", questao4('bilheteria.db'))
    # questao5()
    print("Questão 5: \n", questao5('bilheteria.db'))
    
    
    print("feito por: ", AUTORES[0],", ", AUTORES[1])
    
    return 0

if __name__ == '__main__':
    main()