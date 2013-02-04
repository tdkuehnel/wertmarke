#!/usr/local/bin/python2.7

import BaseHTTPServer
import SimpleHTTPServer
import urllib
import urlparse
import cgi
import shutil
import mimetypes
from StringIO import StringIO
import pg
import ssl
import sys
import urlparse
import socket

def run(server_class=BaseHTTPServer.HTTPServer,
        handler_class=BaseHTTPServer.BaseHTTPRequestHandler):
        server_address = ('', 8282)
        httpd = server_class(server_address, handler_class)
        httpd.serve_forever()

class WertmarkeHTTPServer(BaseHTTPServer.HTTPServer):
	def get_request(self):
		newsocket, fromaddr = self.socket.accept()
		print "connection request.."
		connstream = ssl.wrap_socket(newsocket,
					     server_side=True,
					     ca_certs="/etc/pki/wertmarke/CA/private/cacert.pem",
					     certfile="/etc/pki/wertmarke/wertmarke-ssl.crt",
					     keyfile="/etc/pki/wertmarke/wertmarke-ssl.key",
					     cert_reqs=ssl.CERT_REQUIRED,
					     ssl_version=ssl.PROTOCOL_TLSv1)
		peercert = connstream.getpeercert()
		print connstream.cipher()
		print peercert
		print "connected"
		return connstream, fromaddr, peercert

	def _handle_request_noblock(self):
		"""Handle one request, without blocking.
		
		I assume that select.select has returned that the socket is
		readable before this function was called, so there should be
		no risk of blocking in get_request().
		"""
		try:
			request, client_address, client_cert = self.get_request()
		except socket.error:
			return
		if self.verify_request(request, client_address):
			try:
				self.process_request(request, client_address, client_cert)
			except:
				self.handle_error(request, client_address)
				self.shutdown_request(request)

	def finish_request(self, request, client_address, client_cert):
		"""Finish one request by instantiating RequestHandlerClass."""
		self.RequestHandlerClass(request, client_address, client_cert, self)


	def process_request(self, request, client_address, client_cert):
		"""Call finish_request.

		Overridden by ForkingMixIn and ThreadingMixIn.

		"""
		self.finish_request(request, client_address, client_cert)
		self.shutdown_request(request)


		

class WertmarkeHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	""" class """
	def __init__(self, request, client_address, client_cert, server):		
		self.client_cert = client_cert
		self.pg = None
		SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self, request, client_address, server)

	def handle(self):
		"""Handle multiple requests if necessary."""
		self.close_connection = 1

		self.handle_one_request()
		while not self.close_connection:
			self.handle_one_request()

	def open_pg(self):
		try:
			self.pg = pg.connect("wertmarke","localhost",5432,None,None,"rudiwurm")
		except:
			return False
		return True

	def do_CREATE(self):
		if self.pg is None:
			self.open_pg()
		
		if self.pg is not None:
			dn_name = 'unknown'
			for t in self.client_cert['subject']:
				if len(t) > 0:
					if len(t[0]) > 1:
						if t[0][0] == 'organizationalUnitName':
							dn_name = t[0][1]
			print dn_name
			print urlparse.parse_qs(urlparse.urlsplit(self.path).query)
			try:
				count = int(urlparse.parse_qs(urlparse.urlsplit(self.path).query)['count'][0])
			except:
				count = 1
			if count > 20:
				self.send_response(400)
				self.end_headers()
				return
			#			print self.client_cert['subject'][3][0][1]
			#			s = 'insert into wertmarke default values returning marke;'
			#			s = "insert into wertmarke (erzeuger) values (uuid_generate_v5(uuid_ns_x500(),'"+self.client_cert['subject'][3][0][1]+"')) returning marke;"
			l = []
			f = StringIO()
			for i in range(count):
				s = "insert into wertmarke (erzeuger) values (uuid_generate_v5(uuid_ns_x500(),'"+dn_name+"')) returning marke;"
				r = self.pg.query(s)
				l.append( r.getresult()[0][0])
			f.write(l)
#			f.write()
			length = f.tell()
			f.seek(0)
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.send_header("Content-Length", str(length))
			self.end_headers()
			self.copyfile(f, self.wfile)
			f.close()
		else:
			self.send_response(500)
			self.end_headers()

	def do_GET(self):
		if self.pg is None:
			self.open_pg()

		s = "Wertmarkenserver up and running."
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.send_header("Content-Length", str(len(s)))
		self.wfile.write(s)
		self.end_headers()
		
	def send_head(self):
		"""Common code for GET and HEAD commands.
		just send two bytes
		
		"""

		ctype = "plain/text"
		f = StringIO()
		f.write("Ok")
		length = f.tell()
		f.seek(0)
	
		self.send_response(200)
		self.send_header("Content-type", ctype)
		self.send_header("Content-Length", str(length))
		self.end_headers()
		return f


def wms_main_program():
    """ main program loop """
    try:
	run(handler_class=WertmarkeHTTPRequestHandler, server_class=WertmarkeHTTPServer)
    except KeyboardInterrupt: 
	sys.exit()
        
