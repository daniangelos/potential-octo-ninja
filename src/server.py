#!/usr/bin/env python

import socket
import sys
import threading
import json
import time
import struct

# Variaveis globais
c = [ ]
addr = [ ]
num_clients=0

# Variaveis do socket DONT CHANGE!!!!!
s = socket.socket()
host = socket.gethostname()
port = 12345

def main():
	thr1 = threading.Thread(target = esperar_clientes)
	thr2 = threading.Thread(target = receber_dados)

	# Inicializar o servidor:
	s.bind((host,port))
	s.listen(5)

	thr1.start()
	thr2.start()

	thr1.join()
	thr2.join()

# FIM DA MAIN

def esperar_clientes():
	global num_clients
	global c
	global addr

	while True:
		c_aux, addr_aux = s.accept()
		c.append(c_aux)
		addr.append(addr_aux)
		#print 'Got connection from', addr[num_clients]
		num_clients+=1
		for com in c:
			data = {'QTD_CLIENTES': num_clients,'SEU_ID': num_clients-1}
			data_string = json.dumps(data)
			com.send(data_string)
			pass
		pass

# FIM esperar_clientes

def receber_dados():
	global num_clients
	global c
	global addr
	data = b''
	while True:
		for com in c:
			sz_buf = com.recv(4)
			size = struct.unpack("@i", sz_buf)[0]
			data = com.recv(size)
			if data == b'': continue
			data_loaded = json.loads(data)
                        print '{source: %s, dest: %s, payload: %s}' %(
                                data_loaded['source'],
                                data_loaded['dest'],
                                data_loaded['payload'])
			#print "\n"
		pass

# FIM receber_dados

if __name__ == "__main__":
	main()
