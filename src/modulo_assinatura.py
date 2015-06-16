#!/usr/bin/env python

import md5
import sha

def generate_md5(payload):
	m = md5.new()
	m.update(payload)
	return m.digest()
	pass

def generate_sha1(payload):
        m = sha.new();
        m.update(payload);
        return m.digest();
        pass

