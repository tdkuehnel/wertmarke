#!/usr/local/bin/python2.7

import socket, ssl, pprint
import httplib, sys

class wertmarkeHTTPSConnection(httplib.HTTPConnection):
        def connect(self):
            "Connect to a host on a given (SSL) port."

            sock = socket.create_connection((self.host, self.port),
                                            self.timeout, self.source_address)
            self.sock = ssl.wrap_socket(sock,
			   server_side=false,
                           ca_certs="/etc/pki/wertmarke/CA/private/cacert.pem",
                           certfile="/etc/pki/wertmarke/wertmarkenerzeuger-1-ssl.pem",
                           keyfile= "/etc/pki/wertmarke/wertmarkenerzeuger-1-ssl.key",
                           cert_reqs=ssl.CERT_REQUIRED,
			   ssl_version=ssl.PROTOCOL_TLSv1)
	    print self.sock.cipher()
	    print self.sock.getpeercert()
	    
conn = wertmarkeHTTPSConnection('datentaeter.org',
				8800)

print ssl.OPENSSL_VERSION
#print type(conn)

conn.request('CREATE','/?count=1')
r1=conn.getresponse()
print r1.status, r1.reason
data1=r1.read()

print data1

sys.exit()



