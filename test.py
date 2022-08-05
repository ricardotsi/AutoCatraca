import socket
import psycopg2
from psycopg2 import Error
from datetime import datetime

def textFormat (data):
        aux2=""
        BYTE_TAM=[]
        BYTE_INIT = chr(int("2", base=16))#conf. bit inicial
        BYTE_END = chr(int("3", base=16))#conf. bit final
        BYTE_TAM.append(chr(len(data)))#conf. tamanho dos dados
        BYTE_TAM.append(chr(int("0", base=16)))
        aux2 += BYTE_INIT#Inserindo byte inicial
        aux2 += BYTE_TAM[0]#Inserindo byte do tamanho
        aux2 += BYTE_TAM[1]
        aux = aux2+data# concatenando com a informação
        BYTE_CKSUM = aux[1]#Calculo do Checksum
        for a in range(2,len(aux)):
            BYTE_CKSUM = chr(ord(BYTE_CKSUM) ^ ord(aux[a]))
        aux += BYTE_CKSUM#Inserindo Checksum
        aux += BYTE_END#Inserindo byte Final
        return aux

TCP_IP = ['172.17.150.1',
            '172.17.150.2',
            '172.17.150.3',
            '172.17.150.4']
TCP_PORT = 3000
BUFFER_SIZE = 1024

for ip in TCP_IP:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        connection = psycopg2.connect(user = "postgres", password = "M4nut3nc40", host = "172.17.0.249", port = "5432", database = "ifpracesso")
        cursor = connection.cursor()
        query = connection.cursor()
        s.connect((ip, TCP_PORT))
        cursor.execute("select max(id_registro) from ifpracessomain_registro where nr_catraca=%s", (int(ip[-1]),))
        result = cursor.fetchone()
        if result[0] is not None:
            idRegistro = int(result[0])
        else:
            idRegistro = 1
        while True:
            EVENTO = "01+RR+00+T]01]"+str(idRegistro)
            s.sendall(textFormat(EVENTO).encode())
            data = s.recv(BUFFER_SIZE).decode().split("[")
            if "01+RR+050=" in data[0]:
                break
            else:
                cursor.execute("select * from ifpracessomain_registro where id_registro=%s and nr_catraca=%s", (int(data[0][-9:].lstrip("0")),ip[-1],))
                if not cursor.fetchone():
                    if data[2].isdigit():
                        insertQuery = "insert into ifpracessomain_registro (nr_catraca, id_registro, matricula, dt_registro, operacao) VALUES (%s, %s, %s, %s, %s)"
                        vars = ip[-1], data[0][-9:], data[2], datetime.strptime(data[3], '%d/%m/%Y %H:%M:%S'), data[4]
                        query.execute(insertQuery, vars)
                        connection.commit()
                        print(data)
            idRegistro+=1
    except Exception as e:
        print(e)
    s.close()
    if(connection):
        cursor.close()
        connection.close()
