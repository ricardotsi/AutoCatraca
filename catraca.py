import socket


def text_format (data):
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

# TCP_IP = ['172.17.150.1']#,
#             #'172.17.150.2',
#             #'172.17.150.3',
#             #'172.17.150.4']
# TCP_PORT = 3000
# BUFFER_SIZE = 1024


with open('deletar.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    #for ip in TCP_IP:
    try:
        for row in csv_reader:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP[2], TCP_PORT))
            EVENTO = "01+ECAR+00+1+E["+row[2]+"["+row[2]+"[[[1[1[1[[[[W[2[1[1[0[[0["+row[0]+"["+row[1]+"["
            s.sendall(textFormat(EVENTO).encode())
            data = s.recv(BUFFER_SIZE).decode()
            print(TCP_IP[2])
            print(row)
            print(data)
            s.close()
    except Exception as e:
        print(e)