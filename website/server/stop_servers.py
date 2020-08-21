#!/usr/bin/env python3

import sys
import os
import time
import json
from multiprocessing.connection import Client

from config import SERVERS

def stopServer(server_name, socket):
	# establish communications
	connection = None
	try:
		connection = Client(socket)
	except ConnectionRefusedError as e:
		print('Application {} is not running.'.format(server_name))
		return
	
	# ask the active server process to exit
	request = {
		'action': 'exit',
	}
	connection.send(request)
	
	# close connection and print server response
	response = connection.recv()
	connection.close()
	print(response)

def main(socket=('localhost', 3063)):
	# make sure errors are written to a log file
	scriptdir = os.path.dirname(__file__)
	logdir = os.path.join(scriptdir, 'logs')
	os.makedirs(logdir, exist_ok=True)
	logfile = os.path.join(logdir, 'client.log')
	sys.stderr = open(logfile, 'a')
	
	for server_name, server_config in SERVERS.items():
		stopServer(server_name, server_config['socket'])

if __name__ == '__main__':
	main()
