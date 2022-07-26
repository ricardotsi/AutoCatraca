from tkinter import filedialog
from pandas import read_csv
from unidecode import unidecode
from sys import exit, argv, executable
from os import execv
from datetime import datetime
# from database import *
# from catraca import update_catraca
from etiqueta import criar_etiquetas


def save_log(listalog):
    with open('log' + str(datetime.now()) + '.txt', 'w') as sfile:
        for item in listalog:
            print(item)
            sfile.write('\n' + item)


if __name__ == '__main__':
    """Main function"""
    print("\nSelecione a ação desejada:\n1)Adicionar pessoas(BD, catracas) e gerar etiquetas\n"
          "2)Somente gerar etiquetas\n3)Deletar pessoas(catraca)\n")
    opcao = input()
    if opcao not in ('1', '2', '3'):
        execv(executable, ['python'] + argv)
    # open dialog to select file
    ofile = filedialog.askopenfile(mode='r', filetypes=[('csv', '.csv')], initialdir='~/Downloads')
    # read file do a dataframe
    dfTodo = read_csv(ofile)
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
    log = []
    if opcao == '1':
        # for row in dfTodo.itertuples():
        #     # find duplicates from dataframe in database
        #     isIndb = get_pessoa(row.pessoa, row.matricula)
        #     # if there is a duplicate, update cartao
        #     if isIndb is not None:
        #         update_pessoa(row.pessoa, row.matricula, row.cartao)
        #         res = update_catraca("A", row.matricula, row.cartao, row.pessoa)
        #         log.append('######################## Atualizado ########################')
        #         log.append('Cartão antigo: %s Cartão Novo: %s Pessoa: %s' % (isIndb[2], row.cartao, row.pessoa))
        #         for r in res:
        #             log.append(r)
        #     # if it is not duplicate, insert into database
        #     else:
        #         insert_pessoa(row.pessoa, row.matricula, row.cartao, row.id_curso, row.ano)
        #         res = (update_catraca("E", row.matricula, row.cartao, row.pessoa))
        #         log.append('@@@@@@@@@@@@@@@@@@@@@@@@ Cadastrado @@@@@@@@@@@@@@@@@@@@@@@@')
        #         log.append('Pessoa: %s Cartão: %s ' % (row.pessoa, row.cartao))
        #         for r in res:
        #             log.append(r)
        # # close database
        # close_db()
        # # Save log
        # save_log(log)
        # # create labels for printing
        criar_etiquetas(dfTodo)
    elif opcao == '2':
        criar_etiquetas(dfTodo)
    elif opcao == '3':
        # delete from turntables
        # for row in dfTodo.itertuples():
        #     res = (update_catraca("E", row.matricula, row.cartao, row.pessoa))
        #     log.append('&&&&&&&&&&&&&&&&&&&&&&&&& Deletado &&&&&&&&&&&&&&&&&&&&&&&&&')
        #     log.append('Pessoa: %s Cartão: %s ' % (row.pessoa, row.cartao))
        #     for r in res:
        #         log.append(r)
        save_log(log)
