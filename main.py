from tkinter import filedialog
from pandas import read_csv
from unidecode import unidecode
from sys import exit
from database import *
from catraca import *

if __name__ == '__main__':
    """Main function"""
    # open dialog to select file
    file = filedialog.askopenfile(mode='r', filetypes=[('csv', '.csv')], initialdir='~/Downloads')
    # read file do a dataframe
    dfTodo = read_csv(file)
    if dfTodo.empty or not {'cartao', 'pessoa', 'matricula', 'curso', 'id_curso'}.issubset(dfTodo.columns):
        print('Verifique se o arquivo csv possui as colunas cartao, pessoa, matricula, curso, id_curso')
        exit()
    # Normalize strings
    for pessoa, curso in zip(dfTodo['pessoa'], dfTodo['curso']):
        # remove accents and transform to upper
        pessoaNorm = unidecode(pessoa).upper()
        cursoNorm = unidecode(curso).upper()
        # replace old string with normalized ones
        dfTodo = dfTodo.replace(pessoa, pessoaNorm)
        dfTodo = dfTodo.replace(curso, cursoNorm)
    # remove duplicates inside dataframe
    dfTodo = dfTodo.drop_duplicates(subset='pessoa').drop_duplicates(subset='matricula')
    for row in dfTodo.itertuples():
        # find duplicates from dataframe in database
        isIndb = get_pessoa(row.pessoa, row.matricula)
        # if there is a duplicate, update cartao
        if isIndb is not None:
            update_pessoa(row.pessoa, row.matricula, row.cartao)
            print('######################## Cartão Atualizado ########################')
            print('Cartão antigo: %s Cartão Novo: %s Pessoa: %s' % (isIndb[2], row.cartao, row.pessoa))
            update_catraca("A", row.matricula, row.cartao, row.pessoa)
        # if it is not duplicate, insert into database
        else:
            insert_pessoa(row.pessoa, row.matricula, row.cartao, row.id_curso)
            print('######################## Pessoa Cadastrada ########################')
            print('Pessoa: %s Cartão Novo: %s ' % (row.pessoa, row.cartao))
            update_catraca("I", row.matricula, row.cartao, row.pessoa)
    close_db()