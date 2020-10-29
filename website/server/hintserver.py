
import contextlib
import sys
import os

import config

def server(name):
	# imports are placed here so that any errors will be written to a log file
	from codenames.generators.connector import Connector
	from codenames.generators.hintserver import SuperHintServer
	
	server = config.SERVERS[name]
	socket = server['socket']
	server_config = server['config']
	with Connector(socket, config.logs_directory) as connector:
		hint_server = SuperHintServer(**server_config, generator_configs=config.GENERATORS)
		
		# event loop
		while True:
			timeout = config.server_timeout if config.autostart else None
			request = connector.receive(timeout=timeout)
			
			# if nothing has been received for timeout seconds, we shut down the server
			if not request:
				break
			
			# check if we should quit
			if request['action'] == 'exit':
				connector.send('quit successfully')
				break
			
			response = hint_server.handleRequest(request)
			connector.send(response)

def main(argv):
	# make sure the logs directory exists
	os.makedirs(config.logs_directory, exist_ok=True)
	
	log_file = os.path.join(config.logs_directory, 'hintserver.log')
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
