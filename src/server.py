#!/usr/bin/env python
# encoding: utf-8

import socket
import sys
import threading
import json
import time
import struct
from bitstring import BitArray
from Queue import Queue

# Variaveis globais
client_list = [ ] # Lista de tuplas, do tipo (status, cliente). Status diz se o cliente ainda está vivo
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
def int_to_bit(n):
	return [1 if digit == '1' else 0 for digit in bin(n)[2:]]
#FIM int_to_bit
def bit_to_int(bitfield):
	total = 0
	i = 0
	for number in reversed(bitfield):
		if(number == 1):
			total += 2**i
		i+=1
	return total
#FIM bit_to_int	
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
def extend(bitfield):
	extenso = bitfield
	if(len(extenso)<32):
		i = len(extenso)
		while(i<32):
			extenso.insert(0,0)
			i+=1
	return extenso

def cagar_pares(bitfield):
	cagado = bitfield
	i=0
	while(i<len(cagado)):
		if(i%2==0):
			cagado[i] = not cagado[i]
		i+=1
	return cagado
#end cagar_pares

def cagar_impares(bitfield):
	cagado = bitfield
	i=0
	while(i<len(cagado)):
		if(i%2!=0):
			cagado[i] = not cagado[i]
		i+=1
	return cagado
#end cagar_impares

def receber_dados():
	global num_clients
	global client_list
	global addr
	global to_send
	data = b''
	while True:
		for client_pair in client_list:
			(client_online, com) = client_pair
			if client_online:   # Este IF e os Try/catch são tolerancia a falhas, caso o cliente caia

				try:
					sz_buf = com.recv(4)
				except socket.error:
					client_pair[0] = False
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
					client_pair[0]= False
					continue

				if data == b'':
					continue
				data_loaded = json.loads(data)
				vetor_bits = int_to_bit(data_loaded['payload'])
				vetor_bits = extend(vetor_bits)
				print vetor_bits
				vetor_bits = cagar_pares(vetor_bits)
				print vetor_bits
				data_loaded['payload'] = bit_to_int(vetor_bits)
				to_send.put(data_loaded)    # Coloca o dado recebido em uma fila sincrona de dados para serem enviados

# FIM receber_dados


def enviar_dados():
	global to_send
	while True:
		data_loaded = to_send.get()
		data = json.dumps(data_loaded)
		dest = int(data_loaded['dest'])

		if len(client_list) > dest: # Dropa o pacote se o cliente nao existir
			client_pair = client_list[dest]
			client_online, client = client_pair

			if client_online: # Este IF e os Try/catch são tolerancia a falhas, caso o cliente caia
				print "Enviando para: " + str(dest)
				n = len(data)
				sz_buf = struct.pack("@i", n)  # converte N em 4 bytes, para enviar pelo socket

				try:
					client.send(sz_buf) # envia o tamanho do dado antes
					client.send(data)
				except socket.error:
					client_pair[0]= False
					continue

		to_send.task_done()
# FIM enviar_dados


if __name__ == "__main__":
	main()
