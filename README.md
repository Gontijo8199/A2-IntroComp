# A2-IntroComp


## Descrição
Este repositório contém o trabalho da Avaliação 2 da disciplina de Introdução à Computação. O objetivo deste trabalho é analisar dados de bilheteira de filmes, utilizando Python e SQLite para manipulação e consulta de dados.

## Estrutura do Projeto
- `source/bilheteria.db`: Banco de dados SQLite contendo informações sobre filmes, sessões e bilheteira.
- `source/a2_parte1.py`: Parte 1 da Avaliação 2.
- `source/a2_parte2.py`: Parte 2 da Avaliação 2.
- `source/ModuloA2.py`: Módulo com funções para o manejo da base de dados.
- `tex/relatorio.tex`: Documento em LaTeX que compila o relatório do trabalho.
- `tex/relatorio.pdf`: Relatório compilado em um pdf
## Questões
Na parte 1 são respondidas as seguintes questões:
1. **Questão 1**: Qual o total de bilheteria de todos os filmes, ou seja, o público que foi aos
filmes listados?
2. **Questão 2**: Qual o filme de maior bilheteria em 2023, por país de origem?
3. **Questão 3**: Crie um dataframe com as 100 cidades com maior bilheteria em 2023,
ordenadas de forma decrescente de bilheteria.
4. **Questão 4**: Qual o filme com maior bilheteria em cada cidade? Retorne um dataframe
com as colunas CIDADE, FILME e BILHETERIA.
5. **Questão 5**: Quais as cidades com as maiores bilheterias para filmes brasileiros? Ao
contar a bilheteria de filmes brasileiros, também some as bilheterias
de filmes estrangeiros. Retorne um dataframe com as colunas CIDADE,
BILHETERIA_BR, BILHETERIA_ESTRANGEIRA.

## Requisitos
- Python 3.x
- Bibliotecas: `pandas`, `matplotlib`, `numpy`, `statsmodels`, entre outras ... (instale usando `pip install -r requirements.txt` em sua venv).
- TeX Live
- SQLIte 3