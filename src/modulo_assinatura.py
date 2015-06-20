#!/usr/bin/env python

import md5
import sha
import math
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
	dados = bin(dados)[2:]#.zfill(32)
	if(len(dados)==1):
		qtd_paridade = 2
	elif(len(dados)>1 and len(dados)<5):
		qtd_paridade = 3
	elif(len(dados)>4 and len(dados)<12):
		qtd_paridade = 4
	elif(len(dados)>11 and len(dados)<27):
		qtd_paridade = 5
	elif(len(dados)>26 and len(dados)<58):
		qtd_paridade = 6
	#qtd_paridade = int(math.ceil(math.log(len(dados)+1,2)))
	hamming = (qtd_paridade+len(dados))*[0]##32 bits de dados + 6 bits de paridade
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

def generate_crc8(payload):
	binario = bin(payload)[2:].zfill(32)
	resto = "00000000"
	quociente = binario + resto
	# polinomio: x^8 + x^7 + x^4 + x^3 + x + 1
	polinomio = "110011011"

	i = 0
	so_zero = bin(0)[2:].zfill(32)
	while(quociente[0:32] != so_zero):
		x = i
		for j in range(0, 9):
			x2 = ord(quociente[x]) 
			j2 = ord(polinomio[j]) 
			aux = (x2 ^ j2) + 48
			quociente = quociente[:x] + chr(aux) + quociente[x+1:]

			x+=1
		while( (quociente[i] == '0') & (i < 32) ):
			i+=1
	resto = quociente[32:40]

	return resto

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
                check = generate_hamming(1)
                print ''.join(map(str,check))
		#generate_crc8(102)

if __name__ == "__main__":
	main()
