from psycopg2 import connect, DatabaseError
from config import settings


try:
    # connect to the Postgres server
    conn = connect(**settings.postgresql)
    # create a cursor
    cur = conn.cursor()
except (Exception, DatabaseError) as error:
    print(error)


def get_pessoa(pessoa, matricula):
    """check if a person exists in database"""
    cur.execute('select * from ifpracessomain_pessoa where nome_pessoa=%s or matricula_pessoa=%s',
                (pessoa, matricula))
    return cur.fetchone()


def update_pessoa(pessoa, matricula, cartao):
    """update person with new cartao"""
    try:
        cur.execute('update ifpracessomain_pessoa set cracha_pessoa=%s where nome_pessoa=%s or matricula_pessoa=%s',
                    (cartao, pessoa, matricula))
    except (Exception, DatabaseError) as er:
        print(er)
    finally:
        conn.commit()


def insert_pessoa(pessoa, matricula, cartao, curso, ano):
    """insert person into database"""
    # get max id for new register
    cur.execute('select max(id) from ifpracessomain_pessoa')
    maxid = cur.fetchone()
    # insert new person in database
    try:
        cur.execute('insert into ifpracessomain_pessoa values (%s, %s, %s, %s, %s, %s, %s)',
                    (maxid[0]+1, pessoa, cartao, matricula, ano, 'S', curso))
    except (Exception, DatabaseError) as er:
        print(er)
    finally:
        conn.commit()


def close_db():
    """ Close the connection to the Postgres database server """
    if conn is not None:
        cur.close()
        conn.close()
