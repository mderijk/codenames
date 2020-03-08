
import importlib
import os
import sys

from . import lg
from .. import config
from .super import SuperHintGenerator

class HintServer:
	def __init__(self, generators, log_directory):
		self.generators = {}
		self.log_directory = log_directory
		self.model_cache = {}
		
		# create generator instances with appropriate logging mechanisms
		for name in generators:
			kwargs = config.GENERATORS[name]
			module_name, class_name = kwargs['class'].rsplit('.', 1)
			module_name = '.' + module_name
			current_package = __loader__.name.rsplit('.', 1)[0]
			module = importlib.import_module(module_name, current_package)
			class_ = getattr(module, class_name)
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

class SuperHintServer(HintServer):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		# do a bit of monkey patching and replace the generator names in SuperHintGenerator.generators with a dict of references to the actual generator objects
		for generator in self.generators.values():
			if isinstance(generator, SuperHintGenerator):
				generator.model = {gen_name: self.generators[gen_name] for gen_name in generator.model}
