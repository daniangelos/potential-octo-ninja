#!/usr/bin/env python

import md5

def generate_md5(payload):
	m = md5.new()
	m.update(payload)
	return m.digest()
	pass

