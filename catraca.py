from socket import socket, AF_INET, SOCK_STREAM
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
import logging
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


def operacao(op):
    switch = {
        'I': "00+ECAR+00+1+I[%s[%s[[[1[1[0[[[[W[2[[[[[0[%s",
        'A': "00+ECAR+00+1+A[%s[%s[[[1[1[0[[[[W[2[[[[[0[%s",
        'E': "00+ECAR+00+1+E[%s[%s[[[[[[[[[[[[[[[["
    }
    return switch.get(op)


def thread(index, op, matricula, cartao, pessoa):
    """Each thread will connect to a turntable and send the packet data"""
    logging.info("Thread %s: starting", index)
    # create connection
    conn = socket(AF_INET, SOCK_STREAM)
    # connect to a turntable
    conn.connect((params['c'+str(index + 1)], int(params['tcpport'])))
    # format evento as per the API reference
    evento = operacao(op) % (matricula, cartao, pessoa)
    # send packet
    conn.send(packet_format(evento).encode())
    # print the response
    print(params['c'+str(index + 1)]+" == "+conn.recv(int(params['buffersize'])).decode())
    # close connection
    conn.close()
    logging.info("Thread %s: finishing", index)


def update_catraca(op, matricula, cartao, pessoa):
    """create 4 threads to send data to the turntables"""
    # format logging for debug purposes
    formato = "%(asctime)s: %(message)s"
    logging.basicConfig(format=formato, level=logging.INFO,
                        datefmt="%H:%M:%S")
    # start 4 threads, each one will access one turntable and edit the register
    with ThreadPoolExecutor(max_workers=4) as executor:
        # executor.map(thread, range(4), matricula, cartao, pessoa)
        executor.map(thread, range(4), repeat(op), repeat(matricula), repeat(cartao), repeat(pessoa))
