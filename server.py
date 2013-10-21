#!/usr/bin/env python

import sys
import random
import hashlib
import requests
import threading
import SocketServer
from Crypto.Cipher import AES

import logging
logging.basicConfig(format='%(levelname)-7s | %(asctime)-23s | %(name)-8s | %(message)s')
l = logging.getLogger("drm_server")
l.setLevel(logging.DEBUG)

class DRMHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		try:
			userkey = self.request.recv(16).strip()
			title = self.request.recv(1024).strip()
			l.debug("Got key of length %d" % len(userkey))
			titlehash = hashlib.md5("This is our secret watermark for " + title).hexdigest()
			contentkey = hashlib.md5("This is our key for " + title).hexdigest()

			if titlehash in [ h.strip() for h in open("done_hashes").readlines() ]:
				self.request.send("Sorry, this book has already been streamed. Try another!")
				return

			l.info("TITLE(%s) HASH(%s)" % (title, titlehash))

			source = random.choice([ "holygrail", "futurama", "doctorwho", "arresteddevelopment", "dexter", "simpsons", "starwars" ])
			lines = requests.get("http://api.chrisvalleskey.com/fillerama/get.php?count=100&format=json&show="+source).json()

			headers = [ h['header'] for h in lines['headers'] ]
			quotes = [ h['quote'] for h in lines['db'] ]

			intro = " ".join(random.sample(quotes, 4))
			sub1 = random.choice(headers)
			sub2 = random.choice(headers)
			text1 = " ".join(random.sample(quotes, 10))
			text2 = " ".join(random.sample(quotes, 10))

			plaintext = "<html>\n<head><title>%s</title></head>\n<body>\n\t<h1>%s</h1>\n\t%s\n\t<h2>%s</h2>\n\t%s<h2>%s</h2>\n\t%s\n<!--%s--></body>\n</html>" % (title, title, intro, sub1, text1, sub2, text2, titlehash)
			plaintext += " " * ((16 - (len(plaintext) % 16)) % 16)
			l.debug("Plaintext length: %d" % len(plaintext))
			cyphertext = AES.new(contentkey).encrypt(plaintext)
			cryptedkey = AES.new(userkey).encrypt(contentkey)

			self.request.send(cryptedkey)
			self.request.send(cyphertext)
			self.request.close()
		except Exception:
			l.warning("Exception in connection handler", exc_info=True)
			self.request.send("Something went wrong. Bug Kyle!")


class DRMServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass

if __name__ == "__main__":
	port = int(sys.argv[1])

	server = DRMServer(("0.0.0.0", port), DRMHandler)
	server.serve_forever()
