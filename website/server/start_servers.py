#!/usr/bin/env python3

import inspect
import os
import subprocess
import sys
import time
from multiprocessing.connection import Client, Listener

from config import SERVERS

if sys.platform == 'win32': # windows
	PYTHON_PATH = 'venv\Scripts\python'
	DETACHED_PROCESS = 8 # REPLACES: from win32process import DETACHED_PROCESS
else:
	PYTHON_PATH = 'venv/bin/python'

def launchServer(server_name, socket):
	# try opening a listener and depending on whether it fails, open a new process
	try:
		listener = Listener(socket)
		listener.close()
	except OSError as e:
		print('Server \'{}\' already running'.format(server_name))
	else:
		# initiate and dispatch independent server processes
		cwd = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
		if sys.platform == 'win32':
			process = subprocess.Popen([PYTHON_PATH, 'hintserver.py', server_name], cwd=cwd, creationflags=DETACHED_PROCESS) # NOTE: DETACHED_PROCESS is Windows only
		else:
			process = subprocess.Popen(['nohup', PYTHON_PATH, 'hintserver.py', server_name], cwd=cwd) # although not the same, nohup is the replacement for DETACHED_PROCESS
		
		return process

def main():
	# make sure errors are written to a log file
	scriptdir = os.path.dirname(__file__)
	logdir = os.path.join(scriptdir, 'logs')
	os.makedirs(logdir, exist_ok=True)
	logfile = os.path.join(logdir, 'client.log')
	sys.stderr = open(logfile, 'a')
	
	# boot servers
	processes = {}
	for server_name, server_config in SERVERS.items():
		process = launchServer(server_name, server_config['socket'])
		if process:
			processes[server_name] = process
	
	# poll servers to make sure they booted correctly
	while processes:
		time.sleep(2)
		
		# send out a probe to each server
		terminated_servers = []
		booted_servers = []
		for server_name, process in processes.items():
			# make sure the process is still running
			try:
				if process.returncode is not None:
					print('Server \'{}\' failed to boot'.format(server_name))
					terminated_servers.append(server_name)
					continue
			except AttributeError as e:
				print(server_name)
				continue
			
			# try to make contact
			request = {
				'action': 'poll'
			}
			try:
				connection = Client(SERVERS[server_name]['socket'])
			except ConnectionRefusedError as e:
				terminated_servers.append(server_name)
				continue
			
			# poll the server
			connection.send(request)
			
			# close connection and return server response
			try:
				response = connection.recv()
				if response['status'] == 'success':
					print('Server \'{}\' booted successfully'.format(server_name))
					booted_servers.append(server_name)
				else:
					print('Received incorrect response from server \'{}\' during polling'.format(server_name))
					terminated_servers.append(server_name)
			except EOFError:
				print('Received unexpected end of file from server \'{}\' during polling'.format(server_name))
				terminated_servers.append(server_name)
			except ConnectionResetError:
				print('The connection was reset during polling of server \'{}\''.format(server_name))
				terminated_servers.append(server_name)
			connection.close()
		
		# remove servers from waiting list for which we know that they have been booted successfully or failed to boot
		for server_name in terminated_servers + booted_servers:
			del processes[server_name]

if __name__ == '__main__':
	main()
