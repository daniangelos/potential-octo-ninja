#!/usr/bin/env python
# encoding: utf-8

import socket
import sys
import threading
import json
import struct
import time

num_clients = 0
my_id = int()
destino = int()

s = socket.socket()
host = socket.gethostname()
port = 12345

def main():
	global destino
	destino = sys.argv[1]
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
	global my_id
	
	while True:
		data = str(s.recv(1024))
		data_loaded = json.loads(data)
		print str(data_loaded)
		pass
	pass

# FIM receber()
def enviar():
	global num_clients
	global destino
	i = 0
	while True:
		data = {'source': my_id, 'dest': destino, 'payload': i}
		data_string = json.dumps(data) # serialize data para mandar por socket
		n = len(data_string)
		sz_buf = struct.pack("@i", n)
		
		time.sleep(0.5)
		
		s.send(sz_buf)
		s.send(data_string)
		# todo: gerar payload de envio
		i += 1
	pass

# FIM enviar()

if __name__ == "__main__":
	main()
