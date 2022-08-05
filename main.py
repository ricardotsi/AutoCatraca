from tkinter import filedialog
from pandas import read_csv
from unidecode import unidecode
from sys import exit, argv, executable
from os import execv
from datetime import datetime
from database import *
from catraca import update_catraca
from etiqueta import criar_etiquetas


def save_log(listalog):
    with open('log' + str(datetime.now()) + '.txt', 'w') as sfile:
        for item in listalog:
            sfile.write('\n' + item)


def normalize_string(dataframe):
    # Normalize strings
    for pessoa, curso in zip(dataframe['pessoa'], dataframe['curso']):
        # remove accents and transform to upper
        # replace old string with normalized ones
        dataframe = dataframe.replace(pessoa, unidecode(pessoa).upper())
        dataframe = dataframe.replace(curso, unidecode(curso).upper())
    # remove duplicates inside dataframe
    dataframe = dataframe.drop_duplicates(subset='pessoa').drop_duplicates(subset='matricula')
    return dataframe


if __name__ == '__main__':
    """Main function"""
    # Print menu
    print("Selecione a ação desejada:\n"
          "1)Adicionar pessoas(BD, catracas) e gerar etiquetas\n"
          "2)Somente gerar etiquetas\n"
          "3)Deletar pessoas(catraca)\n")
    opcao = input()
    # if not valid option, restart
    if opcao not in ('1', '2', '3'):
        execv(executable, ['python'] + argv)
    # open dialog to select file
    openFile = filedialog.askopenfile(mode='r', filetypes=[('csv', '.csv')], initialdir='~/Downloads')
    # read file to a dataframe
    dfTodo = read_csv(openFile)
    # check if csv is correct
    if dfTodo.empty or not {'cartao', 'pessoa', 'matricula', 'curso', 'id_curso'}.issubset(dfTodo.columns):
        print('Verifique se o arquivo csv possui as colunas '
              'cartao, pessoa, matricula, curso, id_curso e se o arquivo não está vazio')
        exit()
    log = []
    if opcao == '1':
        dfTodo = normalize_string(dfTodo)
        for row in dfTodo.itertuples():
            # find duplicates from dataframe in database
            isIndb = get_pessoa(row.pessoa, row.matricula)
            # if there is a duplicate, update cartao
            if isIndb is not None:
                update_pessoa(row.pessoa, row.matricula, row.cartao)
                res = update_catraca("A", row)
                log.append('######################## Atualizado ########################')
                log.append('Cartão antigo: %s Cartão Novo: %s Pessoa: %s' % (isIndb[2], row.cartao, row.pessoa))
                for r in res:
                    log.append(r)
            # if it is not duplicate, insert into database
            else:
                insert_pessoa(row.pessoa, row.matricula, row.cartao, row.id_curso, row.ano)
                res = update_catraca("I", row)
                log.append('@@@@@@@@@@@@@@@@@@@@@@@@ Cadastrado @@@@@@@@@@@@@@@@@@@@@@@@')
                log.append('Pessoa: %s Cartão: %s ' % (row.pessoa, row.cartao))
                for r in res:
                    log.append(r)
        # close database
        close_db()
        # Save log
        save_log(log)
        # create labels for printing
        criar_etiquetas(dfTodo)
    # create labels for printing
    elif opcao == '2':
        dfTodo = normalize_string(dfTodo)
        criar_etiquetas(dfTodo)
    # delete from turntables
    elif opcao == '3':
        for row in dfTodo.itertuples():
            res = (update_catraca("E", row))
            log.append('&&&&&&&&&&&&&&&&&&&&&&&&& Deletado &&&&&&&&&&&&&&&&&&&&&&&&&')
            log.append('Pessoa: %s Cartão: %s Matricula: %s' % (row.pessoa, row.cartao, row.matricula))
            for r in res:
                log.append(r)
        save_log(log)
