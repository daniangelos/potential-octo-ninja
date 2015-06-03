#!/usr/bin/env python
# encoding: utf-8

import socket

def main():
	s = socket.socket()
	host = socket.gethostname()
	port = 12345
	i = 0

	s.connect((host,port))
	while True:
		print s.recv(1024)
		i+=1

if __name__ == "__main__":
	main()
