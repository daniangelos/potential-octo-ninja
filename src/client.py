#!/usr/bin/env python
# encoding: utf-8

import socket
import sys
import threading

num_clients = 0

s = socket.socket()
host = socket.gethostname()
port = 12345

def main():

	thr1 = threading.Thread(target = receber)
	thr2 = threading.Thread(target = enviar)

	s.connect((host,port))

	thr1.start()
	thr2.start()

	thr1.join()
	thr2.join()

	pass

# FIM DA MAIN

def receber():
	global num_clients

	while True:
		num_clients = int(s.recv(4))
		print num_clients
		pass
	pass

# FIM receber()

def enviar():
	global num_clients
	i = 0
	while True:
		# todo: gerar payload de envio
		i += 1
	pass

# FIM enviar()

if __name__ == "__main__":
	main()
