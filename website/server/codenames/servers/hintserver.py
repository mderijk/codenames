
import os
import sys

from . import lg
from .. import generators_config

class HintServer:
	def __init__(self, generators, log_directory):
		self.generators = {}
		self.log_directory = log_directory
		self.model_cache = {}
		
		# create generator instances with appropriate logging mechanisms
		for name in generators:
			kwargs = generators_config.GENERATORS[name]
			class_ = kwargs['class']
			del kwargs['class']
			
			generator_log_directory = os.path.join(log_directory, name)
			os.makedirs(generator_log_directory, exist_ok=True)
			logger = lg.Logger(generator_log_directory)
			self.generators[name] = class_(**kwargs, logger=logger)
	
	def handleRequest(self, request):
		if 'action' in request and request['action'] == 'hint':
			generator_name = request['generator']
			generator = self.generators[generator_name]
			positive_words, negative_words, neutral_words, assassin_words = request['positive_words'], request['negative_words'], request['neutral_words'], request['assassin_words']
			previous_hints = request['previous_hints']
			game_id = request['game_id']
			word, number = generator.generateHint(game_id, positive_words, negative_words, neutral_words, assassin_words, previous_hints)
			response = {
				'status': 'success',
				'word': word,
				'number': number,
			}
			return response
		else:
			print('{} got a request without action or action was not \'hint\'. ({})'.format(request['generator'], repr(request)), file=sys.stderr)
