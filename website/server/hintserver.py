
import contextlib
import sys
import os

import codenames.config as config
from codenames.servers.connector import Connector
from codenames.servers.hintserver import HintServer

def server(name):
	server = config.SERVERS[name]
	socket = server['socket']
	server_config = server['config']
	with Connector(socket) as connector:
		hint_server = HintServer(**server_config)
		
		# event loop
		while True:
			request = connector.receive()
			
			# check if we should quit
			if request['action'] == 'exit':
				connector.send('quit successfully')
				break
			
			response = hint_server.handleRequest(request)
			connector.send(response)

def main(argv):
	# make sure the logs directory exists
	os.makedirs('logs', exist_ok=True)
	
	log_file = os.path.join('logs', 'hintserver.log')
	with open(log_file, 'a') as stderr, contextlib.redirect_stderr(stderr):
		try:
			server(argv[1])
		except:
			# log error
			import traceback
			e = traceback.format_exc()
			print(e, file=sys.stderr)
			
			# reraise exception
			raise

if __name__ == '__main__':
	main(sys.argv)
