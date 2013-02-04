#!/usr/local/bin/python2.7

import daemon
import lockfile

from wms import wms_main_program

fout = open('/var/lib/wertmarke/fout', 'w+')
ferr = open('/var/lib/wertmarke/ferr', 'w+')


with daemon.DaemonContext(working_directory='/var/lib/wertmarke',
			  uid=509,
			  gid=509,
			  stdout=fout,
			  stderr=ferr,
			  pidfile=lockfile.FileLock('/var/lib/wertmarke/wertmarke.pid'),
			  umask=0o700):
	wms_main_program()
