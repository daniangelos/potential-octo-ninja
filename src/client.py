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
from modulo_assinatura import generate_md5
from modulo_assinatura import generate_sha1
from modulo_assinatura import generate_hamming
from modulo_assinatura import generate_crc8

num_clients = 0
my_id = int()
destino = int()
cript = int()

s = socket.socket()
host = socket.gethostname()
port = 12345
dest_list = []

def read_config(filename):
    file = open(filename, 'r')
    config = json.load(file)
    global cript
    global port
    global dest_list
    cript = config["clients"]["algoritmo"]
    port = config["clients"]["server_port"]
    dest_list = list(config["clients"]["destinos"])

def handle_usage():
    """ Função para gerenciar uso do programa e passagem do argumentos através da linha de comando.  """

    usage = '''Se vira.'''

    parser = optparse.OptionParser(usage)
    parser.add_option('-m', dest='max', type='int', help='Número máximo de clientes, deve ser maior que zero.')
    parser.add_option('-e', dest='_cript',type='int',help='Tipo de encriptacao.')
    parser.add_option('-f', dest='filename',type='string',help='Nome do aquivo de configuração')

    return parser

def main():

    # Recebe os argumentos por linha de comando
    parser = handle_usage()
    (options, args) = parser.parse_args()

    #if options.max == None or options._cript == None:
        #print parser.usage
        #return
    #else:
        #if options.max <= 0:
            #print parser.usage
            #return


    if options.filename == None:
        print parser.usage
        return

    #global cript
    #cript = options._cript

    try:
        read_config(options.filename)
    except Exception as e:
        print "Forneça um arquivo de configuração válido, em JSON"
        return

    s.connect((host,port))

    global my_id
    data = str(s.recv(4))
    my_id = struct.unpack("@i", data)[0]

    global destino
    #destino = randint(0, options.max - 1)

    print dest_list
    if len(dest_list) > my_id:
        destino = dest_list[my_id]
        print destino
    else:
        print "Cliente não configurado!"
        return

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

        # Deteccao de erros:
        payload_recv = data_loaded['msg']
        check_recv = data_loaded['check']
        if(cript==0): #SHA1
            check_sum = generate_sha1(payload_recv)
        elif(cript==1): #MD5
            check_sum = generate_md5(payload_recv)
        elif(cript==2): #Hamming
            check_sum = generate_hamming(payload_recv)
        elif(cript==3):#CRC-8
            check_sum = generate_crc8(payload_recv)

        if check_recv == check_sum:
            print str(data_loaded['dest']) + "-> Recebido de: " + str(data_loaded['source']) + \
            " : " + str(data_loaded['msg']) + " : " + str(check_sum)
            pass
        else:
            print "Mensagem recebida com erro"
            pass




# FIM receber()
def enviar():
    global num_clients
    global destino
    i = 0
    check = ""
    while True:
        if(cript==0):#SHA1
            check = generate_sha1(i)
        elif(cript==1):#MD5
            check = generate_md5(i)
        elif(cript==2):#Hamming
            check = generate_hamming(i)
        elif(cript==3):#CRC-8
            check = generate_crc8(i)
        data = {'source': my_id, 'dest': destino, 'msg': i, 'check' : check}
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
