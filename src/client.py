#!/usr/bin/env python
# encoding: utf-8


import socket
import sys
import optparse
import threading
from random import randint
import json
import struct
import time

num_clients = 0
my_id = int()
destino = int()

s = socket.socket()
host = socket.gethostname()
port = 12345

def handle_usage():
    """ Função para gerenciar uso do programa e passagem do argumentos através da linha de comando.  """

    usage = '''Se vira.'''

    parser = optparse.OptionParser(usage)
    parser.add_option('-m', dest='max', type='int', help='Número máximo de clientes, deve ser maior que zero.')

    return parser

def main():

    # Recebe os argumentos por linha de comando
    parser = handle_usage()
    (options, args) = parser.parse_args()

    if options.max <= 0:
        print parser.usage
        return

    s.connect((host,port))

    global my_id
    data = str(s.recv(4))
    my_id = struct.unpack("@i", data)[0]

    global destino
    destino = randint(0, options.max - 1)
    thr1 = threading.Thread(target = receber)
    thr2 = threading.Thread(target = enviar)

    thr1.setDaemon(True)
    thr2.setDaemon(True)

    thr1.start()
    thr2.start()

    try:
        while (input()):
            pass
    except EOFError:
        s.close()
        return

    return

# FIM DA MAIN

def receber():
    global my_id
    global s

    while True:
        sz_buf = 0

        try:
            sz_buf = s.recv(4)
            size = struct.unpack("@i", sz_buf)[0]
            data = s.recv(size)
        except socket.error as msg:
            print "Servidor não encontrado!"
            return
        except struct.error as msg:
            return

        if data == b'':
            continue
        data_loaded = json.loads(data)
        print "Recebido de: " + str(data_loaded['source']) + " : " + str(data_loaded['payload'])

# FIM receber()
def enviar():
    global num_clients
    global destino
    i = 0
    while True:
        data = {'source': my_id, 'dest': destino, 'payload': i}
        data_string = json.dumps(data) # serialize data para mandar por socket
        n = len(data_string)
        sz_buf = struct.pack("@i", n)  # converte N em 4 bytes, para enviar pelo socket

        time.sleep(0.5)

        try:
            s.send(sz_buf)
            s.send(data_string)
        except socket.error as msg:
            print "Servidor não encontrado!"
            return

        # todo: gerar payload de envio
        i += 1
        pass

# FIM enviar()

if __name__ == "__main__":
    main()
