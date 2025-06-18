AUTORES = ['Nathan Loose Kuipper', 'Rafael Gontijo Ferreira']

import pandas as pd 
import sqlite3



def queryconn(database, query):
    # executa uma dada query na base de dados
    
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall() # caso precise

        df = pd.read_sql_query(query, conn)
        
        return df
    
def carrega_tabela(database, tabela):
    # retorna o data frame dado uma tabela e uma base de dados
    
    with sqlite3.connect(database) as conn:
        query = f"SELECT * FROM {tabela}"
        df = pd.read_sql_query(query, conn)
    return df

def lista_tabelas(db_filename):
    # lista todas as tabelas de uma dada base de dados
    
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        table_row_counts = []
        for table in tables:
            table_name = table[0]
            query = f"SELECT COUNT(*) FROM {table_name};"
            cursor.execute(query)
            row_count = cursor.fetchone()[0]
            table_row_counts.append({"Table": table_name, "Row_Count": row_count})

        return pd.DataFrame(table_row_counts)
    
if __name__ == '__main__':
    print("Importe esse modulo para auxilar com o manejo da base de dados!")