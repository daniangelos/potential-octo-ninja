#!/usr/bin/env python

import md5
import sha
import sys
def is_paridade(index):
	lista = [1 if index==(2**t)-1 else 0 for t in range(0,6)] 
	return 1 in lista 

def junta(dados,hamming):
	i=0
	j=0
	while(i<len(hamming)):
		if(is_paridade(i)):
			i+=1
			continue
		hamming[i] = int(dados[j])
		i+=1
		j+=1
	return hamming
def get_list(binario):
	index = 0
	lista = []
	for elemento in reversed(binario):
		if(elemento=='1'):
			lista.append(2**index)
		index+=1
	return lista
def generate_hamming(payload):
	dados = payload
	dados = bin(dados)[2:].zfill(32)
	hamming = 38*[0]##32 bits de dados + 6 bits de paridade
	hamming = junta(dados,hamming)
	i=0
	while(i<len(hamming)):
		if(not is_paridade(i)):
			binario = bin(i+1)[2:].zfill(32)
			lista = get_list(binario)
			for elemento in lista:
				hamming[elemento-1] = hamming[elemento-1] ^ hamming[i]
		i+=1
	return hamming
def generate_md5(payload):
	aux = payload
	m = md5.new()
	m.update(str(aux))
	return m.hexdigest()
pass

def generate_sha1(payload):
	aux = payload
	m = sha.new()
	m.update(str(aux))
	return m.hexdigest()
pass

def main():
	#check = generate_md5(5)
	#print check
	#check = generate_sha1(5)
	#print check
		check = generate_hamming(10)
		print ''.join(map(str,check))

if __name__ == "__main__":
	main()
