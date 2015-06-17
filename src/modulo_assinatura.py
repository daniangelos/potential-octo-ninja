#!/usr/bin/env python

import md5
import sha

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
	check = generate_md5(5)
	print check
	check = generate_sha1(5)
	print check
		
if __name__ == "__main__":
    main()
