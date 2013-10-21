#!/usr/bin/env python
'''This is the core of the publishers' DRM technology. Distributed in bytecode format, it can never be reverse-engineered by pirates!'''

import os
import hashlib
import datetime
import weasyprint

from Crypto.Cipher import AES

def get_userkey():
	'''Returns a userkey that can be used in the DRM protocol.'''
	return hashlib.md5(os.uname()[1]).hexdigest()[:16]

def decrypt_drm_book(cyphertext, userkey):
	'''Decrypts and decodes the ebook, giving the user an authorized way to read books! Completely uncrackable since it relies on top-grade encryption.'''
	cryptedkey = cyphertext[:32]
	cypherbook = cyphertext[32:]
	contentkey = AES.new(userkey).decrypt(cryptedkey)
	plainbook = AES.new(contentkey).decrypt(cypherbook)
	png = weasyprint.HTML(string=plainbook).write_png()
	return png
