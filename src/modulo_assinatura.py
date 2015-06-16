#!/usr/bin/env python

import md5
import sha

def generate_md5(payload):
	aux = payload
	m = md5.new()
	m.update(str(aux))
	return m.digest()
	pass

def generate_sha1(payload):
        m = sha.new();
        m.update(payload);
        return m.digest();
        pass

def main():
	check = generate_md5(5)
	print check
		
if __name__ == "__main__":
    main()