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

def launchPythonProcess(program_filepath, *args, cwd=None):
	if sys.platform == 'win32':
		process = subprocess.Popen([PYTHON_PATH, program_filepath, *args], cwd=cwd, creationflags=DETACHED_PROCESS) # NOTE: DETACHED_PROCESS is Windows only
	else:
		process = subprocess.Popen(['nohup', PYTHON_PATH, program_filepath, *args], cwd=cwd) # although not the same, nohup is the replacement for DETACHED_PROCESS
	
	return process

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
		process = launchPythonProcess('hintserver.py', server_name, cwd=cwd)
		
		return process

def pollServer(server_name):
	request = {
		'action': 'poll'
	}
	try:
		connection = Client(SERVERS[server_name]['socket'])
	except ConnectionRefusedError as e:
		return (False, 'Connection refused for server \'{}\''.format(server_name))
	
	# poll the server
	connection.send(request)
	
	# close connection and return server response
	try:
		response = connection.recv()
	except EOFError:
		return (False, 'Received unexpected end of file from server \'{}\' during polling'.format(server_name))
	except ConnectionResetError:
		return (False, 'The connection was reset during polling of server \'{}\''.format(server_name))
	else:
		if response['status'] == 'success':
			return (True, None)
		else:
			return (False, 'Received incorrect response from server \'{}\' during polling'.format(server_name))
	finally:
		connection.close()

def pollServers(server_names):
	for server_name in server_names:
		status, message = pollServer(server_name)
		if not status:
			return (False, message)
	
	return (True, None)

def main():
	MAX_POLL_COUNT = 5
	POLL_INTERVAL = 2 # seconds
	
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
	for i in range(MAX_POLL_COUNT):
		time.sleep(POLL_INTERVAL)
		
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
			status, message = pollServer(server_name)
			if status:
				booted_servers.append(server_name)
				print('Server \'{}\' booted successfully'.format(server_name))
			else:
#				terminated_servers.append(server_name)
				print(message)
		
		# remove servers from waiting list for which we know that they have been booted successfully or failed to boot
		for server_name in terminated_servers + booted_servers:
			del processes[server_name]
		
		# stop checking if all servers have been confirmed to be up and running
		if not processes:
			break
	else:
		print('Could not confirm whether the following servers are running:')
		for server_name in processes:
			print(server_name)

if __name__ == '__main__':
	main()
