#!/usr/bin/env python3

import inspect
import os
import subprocess
import sys
from multiprocessing.connection import Listener

from codenames.config import SERVERS

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
			subprocess.Popen([PYTHON_PATH, 'hintserver.py', server_name], cwd=cwd, creationflags=DETACHED_PROCESS) # NOTE: DETACHED_PROCESS is Windows only
		else:
			subprocess.Popen(['nohup', PYTHON_PATH, 'hintserver.py', server_name], cwd=cwd) # although not the same, nohup is the replacement for DETACHED_PROCESS

def main():
	# make sure errors are written to a log file
	scriptdir = os.path.dirname(__file__)
	logdir = os.path.join(scriptdir, 'logs')
	os.makedirs(logdir, exist_ok=True)
	logfile = os.path.join(logdir, 'client.log')
	sys.stderr = open(logfile, 'a')
	
	for server_name, server_config in SERVERS.items():
		launchServer(server_name, server_config['socket'])

if __name__ == '__main__':
	main()
