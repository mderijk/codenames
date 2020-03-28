
from multiprocessing.connection import Client
import sys

from .. import config

class AI:
	def __init__(self, name):
		self.name = name
		self.socket = config.GENERATOR_SOCKETS[name]
	
	def generateHint(self, game_id, positive_words, negative_words, neutral_words, assassin_words, n=20, previous_hints=None):
		if previous_hints is None:
			previous_hints = []
		
		request = {
			'action': 'hint',
			'game_id': game_id,
			'generator': self.name,
			'positive_words': positive_words,
			'negative_words': negative_words,
			'neutral_words': neutral_words,
			'assassin_words': assassin_words,
			'previous_hints': previous_hints,
		}
		
		# connect to the hint generation server
		connection = None
		try:
			connection = Client(self.socket)
		except ConnectionRefusedError as e:
			print('{} server is being queried, but not running.'.format(self.name), file=sys.stderr)
			return None
		
		# ask the server to generate a hint
		connection.send(request)
		
		# close connection and return server response
		try:
			response = connection.recv()
			if response['status'] == 'success':
				response = (response['word'], response['target_words'])
			else:
				response = ('A significant error occurred while generating hints. Please contact the author. (Internal Server Error)', None)
		except EOFError:
			response = ('A significant error occurred while generating hints. Please contact the author. (Internal Server Error)', None)
		except ConnectionResetError:
			response = ('The server was reset while processing your request. (Internal Server Error)', None)
		connection.close()
		
		return response

class DummyAI(AI):
	def __init__(self, name='dummy_ai'):
		self.name = name
	
	def generateHint(self, *args, **kwargs):
		return (False, None)

def main(argv):
	if len(argv) > 2:
		ai = AI(argv[1])
		hint = ai.generateHint('command_line', argv[2:], [], [], [])
		print(hint)
	else:
		print('USAGE: {} <name of AI> [<any number of target words>]'.format(argv[0]), file=sys.stderr)

if __name__ == '__main__':
	main(sys.argv)
