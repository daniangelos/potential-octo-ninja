#!/usr/bin/env python
# encoding: utf-8

import socket
import sys
import threading
import json
import time
import struct
from Queue import Queue

# Variaveis globais
client_list = [ ]
addr = [ ]
num_clients=0

# Fila síncrona de dados a serem enviados
to_send = Queue()

# Variaveis do socket DONT CHANGE!!!!!
s = socket.socket()
host = socket.gethostname()
port = 12345

def main():
    thr1 = threading.Thread(target = esperar_clientes)
    thr2 = threading.Thread(target = receber_dados)
    thr3 = threading.Thread(target = enviar_dados)

    # Inicializar o servidor:
    s.bind((host,port))
    s.listen(5)


    thr1.setDaemon(True)
    thr2.setDaemon(True)
    thr3.setDaemon(True)

    thr1.start()
    thr2.start()
    thr3.start()


    # Encerra o programa caso Ctrl+D (EOF) seja inserido
    try:
        while (input()):
            pass
    except EOFError:
        s.close()
        return

# FIM DA MAIN

def esperar_clientes():
    global num_clients
    global client_list
    global addr

    while True:
        c_aux, addr_aux = s.accept()
        client_list.append( (True, c_aux) )
        addr.append(addr_aux)

        num_clients+=1
        id_buf = struct.pack("@i", (num_clients - 1))
        c_aux.send(id_buf)


# FIM esperar_clientes

def receber_dados():
    global num_clients
    global client_list
    global addr
    global to_send
    data = b''
    while True:
        for (status, com) in client_list:
            if status:
                sz_buf = com.recv(4)
                size = 0
                size = struct.unpack("@i", sz_buf)[0]
                if size == 0:
                    continue

                data = com.recv(size)
                if data == b'':
                    continue
                data_loaded = json.loads(data)
                to_send.put(data_loaded)    # Coloca o dado recebido em uma fila sincrona de dados para serem enviados

# FIM receber_dados


def enviar_dados():
    global to_send
    while True:
        data_loaded = to_send.get()
        data = json.dumps(data_loaded)
        dest = int(data_loaded['dest'])

        print "Enviando para: " + str(dest)
        if len(client_list) > dest:
            n = len(data)
            sz_buf = struct.pack("@i", n)  # converte N em 4 bytes, para enviar pelo socket

            status, client = client_list[dest]
            if status:
                client.send(sz_buf) # envia o tamanho do dado antes
                client.send(data)
        to_send.task_done()


if __name__ == "__main__":
    main()
