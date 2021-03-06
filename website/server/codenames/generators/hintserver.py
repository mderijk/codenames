
import importlib
import os
import sys

from . import lg
from .super import SuperHintGenerator

def load_class_from_string(class_string):
	module_name, class_name = class_string.rsplit('.', 1)
	module_name = '.' + module_name
	current_package = __loader__.name.rsplit('.', 1)[0]
	module = importlib.import_module(module_name, current_package)
	class_ = getattr(module, class_name)
	return class_

class HintServer:
	def __init__(self, generators, logs_directory, generator_configs):
		self.generators = {}
		self.logs_directory = logs_directory
		self.model_cache = {}
		
		# create generator instances with appropriate logging mechanisms
		for name in generators:
			kwargs = generator_configs[name]
			
			# lookup class indicated by kwargs['class'] and replace it
			class_ = load_class_from_string(kwargs['class'])
			del kwargs['class']
			
			generator_log_directory = os.path.join(logs_directory, name)
			os.makedirs(generator_log_directory, exist_ok=True)
			logger = lg.Logger(generator_log_directory)
			self.generators[name] = class_(**kwargs, logger=logger, logs_directory=logs_directory)
	
	def handleRequest(self, request):
		if 'action' in request and request['action'] == 'poll':
			response = {
				'status': 'success',
			}
		elif 'action' in request and request['action'] == 'hint':
			generator_name = request['generator']
			generator = self.generators[generator_name]
			positive_words, negative_words, neutral_words, assassin_words = request['positive_words'], request['negative_words'], request['neutral_words'], request['assassin_words']
			previous_hints = request['previous_hints']
			game_id = request['game_id']
			word, target_words = generator.generateHint(game_id, positive_words, negative_words, neutral_words, assassin_words, previous_hints)
			response = {
				'status': 'success',
				'word': word,
				'target_words': target_words,
			}
		else:
			print('{} got a request without action or action was not \'hint\'. ({})'.format(request['generator'], repr(request)), file=sys.stderr)
			response = {
				'status': 'error',
			}
		
		return response

class SuperHintServer(HintServer):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		# do a bit of monkey patching and replace the generator names in SuperHintGenerator.generators with a dict of references to the actual generator objects
		for generator in self.generators.values():
			if isinstance(generator, SuperHintGenerator):
				generator.model = {gen_name: self.generators[gen_name] for gen_name in generator.model}
