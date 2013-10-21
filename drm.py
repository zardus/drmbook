#!/usr/bin/env python

import os
import hashlib
import datetime
import weasyprint

from Crypto.Cipher import AES

def get_userkey():
	return hashlib.md5(os.uname()[1]).hexdigest()[:16]

def decrypt_drm_book(cyphertext, userkey):
	cryptedkey = cyphertext[:32]
	cypherbook = cyphertext[32:]
	contentkey = AES.new(userkey).decrypt(cryptedkey)
	plainbook = AES.new(contentkey).decrypt(cypherbook)
	png = weasyprint.HTML(string=plainbook).write_png()
	return png
