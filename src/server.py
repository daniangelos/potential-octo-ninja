#!/usr/bin/env python
# encoding: utf-8

import socket
import sys
import threading
import json
import time
import struct
import optparse
import random
from random import randint
from random import uniform
from Queue import Queue

# Variaveis globais
client_list = [ ] # Lista de tuplas, do tipo (status, cliente). Status diz se o cliente ainda está vivo
addr = [ ]
num_clients=0
flipar = int()

mutex = threading.Lock()

# Fila síncrona de dados a serem enviados
to_send = Queue()

# Variaveis do socket DONT CHANGE!!!!!
s = socket.socket()
host = socket.gethostname()
port = 12345

def read_config(filename):
    file = open(filename, 'r')
    config = json.load(file)
    global flipar
    global port
    flipar = config["server"]["flip"]
    port = config["server"]["port"]


def handle_usage():
    """ Função para gerenciar uso do programa e passagem do argumentos através da linha de comando.  """

    usage = '''Se vira.'''

    parser = optparse.OptionParser(usage)
    # 0: nao flipar, 1: flipar aleatorio, 2: flipar pares, 3: flipar impares
    parser.add_option('-f', dest='filename',type='string',help='Nome do aquivo de configuração')

    return parser

def main():
    # Recebe os argumentos por linha de comando
    parser = handle_usage()
    (options, args) = parser.parse_args()

    if options.filename == None:
        print parser.usage
        return

    try:
        read_config(options.filename)
    except Exception as e:
        print "Forneça um arquivo de configuração válido, em JSON"
        return

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
        client_list.append( (True, c_aux) ) # True diz que o cliente ainda está vivo
        addr.append(addr_aux)

        num_clients+=1
        id_buf = struct.pack("@i", (num_clients - 1)) #Codifica o ID do cliente para mandar pelo socket
        c_aux.send(id_buf)


# FIM esperar_clientes
def flip(bit):
    return 1 if bit == 0 else 0

def flipar_paleatorio(bitfield,porcentagem):
    flipado = bitfield
    i=0
    lista = []
    sorteio = randint(0,len(flipado)-1)
    lista.append(sorteio)
    flipado[sorteio] = not flipado[sorteio]
    numero = len(flipado)*porcentagem
    while(i<numero-1):

        while(sorteio in lista):
            sorteio = randint(0,len(flipado)-1)

        lista.append(sorteio)
        flipado[sorteio] = flip(flipado[sorteio])
        i+=1
    return flipado

def flipar_pares(bitfield):
    flipado = bitfield
    i=0
    while(i<len(flipado)):
        if(i%2==0):
            flipado[i] = flip(flipado[i])
        i+=1
    return flipado

#FIM flipar_pares
def flipar_impares(bitfield):
    flipado = bitfield
    i=0
    while(i<len(flipado)):
        if(i%2!=0):
            flipado[i] = flip(flipado[i])
        i+=1
    return flipado
#FIM flipar_impares

def bit32_to_string(lista_bits):
    string = ""
    for elemento in lista_bits:
        aux = bit32_to_int(elemento);
        aux = chr(aux)
        string+=aux
    return string
#FIM bit32_to_chr

def string_to_bit32(checksum):
    aux = checksum
    lista_bits = []
    for elemento in aux:
        elemento = ord(elemento)
        bitfield = int_to_bit(elemento)
        lista_bits.append(bitfield)
    return lista_bits

def int_to_bit32(n):
    aux = int_to_bit(n)
    aux = extend(aux)
    return aux
#FIM int_to_32bit

def int_to_bit(n):
    return [1 if digit == '1' else 0 for digit in bin(n)[2:]]
#FIM int_to_bit

def bit32_to_int(bitfield):
    total = 0
    i = 0
    for number in reversed(bitfield):
        if(number == 1):
            total += 2**i
        i+=1
    return total
#FIM bit_to_int

def extend(bitfield):
    extenso = bitfield
    if(len(extenso)<32):
        i = len(extenso)
        while(i<32):
            extenso.insert(0,0)
            i+=1
        return extenso
    return bitfield
#FIM extend

def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def frombits(bits):
    chars = []
    for b in range(len(bits) / 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)

def receber_dados():
    global num_clients
    global client_list
    global addr
    global to_send
    data = b''
    while True:
        for i in range(len(client_list)):
            mutex.acquire()
            (client_online, com) = client_list[i]
            mutex.release()
            if client_online:   # Este IF e os Try/catch são tolerancia a falhas, caso o cliente caia

                try:
                    sz_buf = com.recv(4)
                except socket.error:
                    mutex.acquire()
                    client_list[i] = (False, com)
                    mutex.release()
                    continue

                size = 0

                try:
                    size = struct.unpack("@i", sz_buf)[0]
                except struct.error as msg:
                    continue

                if size == 0:
                    continue

                try:
                    data = com.recv(size)
                except socket.error:
                    mutex.acquire()
                    client_list[i] = (False, com)
                    mutex.release()
                    continue

                if data == b'':
                    continue
                data_loaded = json.loads(data) #De-serializa o data recebido
                bitfield_msg = int_to_bit32(data_loaded['msg']) #passa o inteiro da mensagem para bitfield
                # Passa o checksum pra bits:
                vetor_bits_check = int_to_bit32(data_loaded['check'])
                for bitfield in vetor_bits_check:
                    bitfield_msg.append(bitfield)
                    pass
                #print vetor_bits_check
                if flipar == 1:
                    #como usar o de porcentagem aleatoria
                    porcentagem = random.uniform(0,1)
                    bitfield_msg = flipar_paleatorio(bitfield_msg,porcentagem)
                elif flipar == 2:
                    #como usar o flip de pares
                    bitfield_msg = flipar_pares(bitfield_msg)
                elif flipar == 3:
                    #como usar o flip de impares
                    bitfield_msg = flipar_impares(bitfield_msg)

                #Passa o bitfield para inteiro
                _mensagem = bitfield_msg[0:32]
                _check = bitfield_msg[32:]
                print _check
                
                data_loaded['msg'] = bit32_to_int(_mensagem)
                data_loaded['check'] = bit32_to_int(_check)
                # Coloca o dado recebido em uma fila sincrona de dados para serem enviados
                to_send.put(data_loaded)
                # FIM receber_dados


def enviar_dados():
    global to_send
    while True:
        data_loaded = to_send.get()
        data = json.dumps(data_loaded)
        dest = int(data_loaded['dest'])

        if len(client_list) > dest: # Dropa o pacote se o cliente nao existir
            mutex.acquire()
            client_pair = client_list[dest]
            client_online, client = client_pair
            mutex.release()

            if client_online: # Este IF e os Try/catch são tolerancia a falhas, caso o cliente caia
                print "Enviando para: " + str(dest)
                n = len(data)
                sz_buf = struct.pack("@i", n)  # converte N em 4 bytes, para enviar pelo socket

                try:
                    client.send(sz_buf) # envia o tamanho do dado antes
                    client.send(data)
                except socket.error:
                    mutex.acquire()
                    client_list[dest] = (False, client)
                    mutex.release()
                    continue

        to_send.task_done()
        # FIM enviar_dados


if __name__ == "__main__":
    main()
