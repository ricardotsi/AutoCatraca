from socket import socket, AF_INET, SOCK_STREAM
from config import catraca


params = catraca()


def packet_format(data):
    """
    Format de TCP packet and apply the API formatting (Check API reference page cartão)
    Packet = <SB><XXXX><II>+ECAR+00+<data><CS><EB>
    <SB>	Start byte		0x02
    <XXXX>	Quantidade de dados		?
    <II>	Índice da mensagem		?
    <CS>	Checksum		?
    <EB>	EndByte		0x03
    """
    # Initial Byte
    byteinit = chr(int("2", base=16))
    # End byte
    byteend = chr(int("3", base=16))
    # Quantity of data
    bytetam = [chr(len(data)), chr(int("0", base=16))]
    # bytetam.append(chr(len(data)))
    # bytetam.append(chr(int("0", base=16)))
    packet = ""
    # Insert <SB>
    packet += byteinit
    # Insert <XXXX>
    packet += bytetam[0]
    packet += bytetam[1]
    # Insert <II> and <data>
    packet += data
    # Checksum
    bytecksum = packet[1]
    for i in range(2, len(packet)):
        bytecksum = chr(ord(bytecksum) ^ ord(packet[i]))
    # Insert <SC>
    packet += bytecksum
    # Insert <EB>
    packet += byteend
    return packet


def update_catraca(matricula, cartao, pessoa):
    """Send data to the turntables"""
    for i in range(4):
        # create connection
        conn = socket(AF_INET, SOCK_STREAM)
        # connect to a turntable
        conn.connect((params['c'+str(i + 1)], int(params['tcpport'])))
        # format evento as per the API reference
        # evento = "00+ECAR+00+1+A[%s[%s[[[1[1[0[[[[W[2[[[[[0[%s" % (matricula, cartao, pessoa)
        evento = "00+ECAR+00+1+E[%s[%s[[[[[[[[[[[[[[[[" % (matricula, cartao)
        # send packet
        conn.send(packet_format(evento).encode())
        # print the response
        print(str(i+1)+": "+params['c'+str(i + 1)]+" == "+conn.recv(int(params['buffersize'])).decode())
        conn.close()
