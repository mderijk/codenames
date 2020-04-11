
import contextlib
import io
import json
import os
import sys

import codenames.config as config

def server():
	from application import Application # import locally so we can capture error messages
	
	# configure application
	application = Application(config)
	
	# load request and generate response
	proper_stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8') # reopen stdin with the correct encoding (in python 3.7 and above you can use sys.stdin.reconfigure('utf-8') instead)
	try:
		request = json.load(proper_stdin)
	except json.JSONDecodeError:
		response = {
			'status': 'error',
			'error': 'Incorrect input format, please provide JSON.',
		}
	else:
		response = application.route(request)
		response = json.dumps(response, ensure_ascii=False)
	
	# output response
	proper_stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
	print(response, file=proper_stdout) # similarly, use sys.stdout.reconfigure('utf-8') in Python 3.7 and above instead.

def main():
	# make sure the logs directory exists
	os.makedirs(config.logs_directory, exist_ok=True)
	
	log_file = os.path.join(config.logs_directory, 'webserver.log')
	with open(log_file, 'a', encoding='utf-8') as stderr, contextlib.redirect_stderr(stderr):
		try:
			server()
		except:
			# log error
			import traceback
			e = traceback.format_exc()
			print(e, file=sys.stderr)
			
			# send back generic error message
			response = {
				'status': 'error',
				'error': 'Internal Server Error',
			}
			response = json.dumps(response, ensure_ascii=False)
			print(response)
			
			# reraise exception
			raise

if __name__ == '__main__':
	main()

# FUTURE: allow multiple people to be in the same game and (possibly) let people spectate games. Test whether a session_id/user_id is participating in the game and whether it is their turn.
