
import importlib
import os

from .. import config

def load_function_from_string(function_string):
	module_name, function_name = function_string.rsplit('.', 1)
	module_name = '.' + module_name
	current_package = __loader__.name.rsplit('.', 1)[0]
	module = importlib.import_module(module_name, current_package)
	function = getattr(module, function_name)
	return function

class HintGenerator:
	model_cache = {}
	model_loader = lambda x: x
	
	def __init__(self, model, logger, include_number=False, include_target_words=False, max_hint_number=None):
		self.model = self._load_model(model)
		self.logger = logger
		self.include_number = include_number
		self.include_target_words = include_target_words
		self.max_hint_number = max_hint_number
		self.scores = None
	
	def _load_model(self, model_name):
		if model_name not in self.model_cache:
			self.model_cache[model_name] = self.__class__.model_loader(model_name)
		return self.model_cache[model_name]
	
	def generateHints(self, positive_words, negative_words, neutral_words, assassin_words, previous_hints):
		""" To be implemented by classes inheriting from HintGenerator. """
		raise NotImplementedError
	
	def generateHint(self, game_id, positive_words, negative_words, neutral_words, assassin_words, previous_hints):
		with self.logger.openLog(game_id) as self.log:
			# keep generating hints until you find one that passes all the tests
			potential_hints = self.generateHints(positive_words, negative_words, neutral_words, assassin_words, previous_hints)
			
			previous_words = [word for word, number in previous_hints]
			for hint, rating in potential_hints:
				if all(map(lambda word: self.hint_filter(hint, word), positive_words + negative_words + neutral_words + assassin_words + previous_words)):
					self.log.log('Generated hint \'{}\' with rating \'{}\''.format(hint, rating))
					if self.include_number or self.include_target_words:
						scores = self.scores[hint]
						scores_and_words = tuple(list(zip(group_words, group_scores)) for group_scores, group_words in zip(scores, (positive_words, negative_words, neutral_words, assassin_words)))
						target_words = self.get_target_words(*scores_and_words)
					else:
						target_words = None
					
					return hint, target_words
			
			raise StopIteration('No suitable hint could be found.')
	
	def get_target_words(self, positive_words_and_scores, negative_words_and_scores, neutral_words_and_scores, assassin_words_and_scores):
		highest_negative_rating = max(rating2 for _, rating2 in negative_words_and_scores + neutral_words_and_scores + assassin_words_and_scores)
		better_scoring_positive_words = [(word, rating) for word, rating in positive_words_and_scores if rating >= highest_negative_rating] # "better scoring" means equal to or higher than the highest negative word
		if self.max_hint_number is not None:
			better_scoring_positive_words = better_scoring_positive_words[:self.max_hint_number]
		return better_scoring_positive_words
	
	def calculate_number(self, positive_scores, negative_scores, neutral_scores, assassin_scores):
		highest_negative_rating = max(rating2 for rating2 in negative_scores + neutral_scores + assassin_scores)
		number_of_better_scoring_positive_words = sum(1 for rating in positive_scores if rating >= highest_negative_rating) # "better scoring" means equal to or higher than the highest negative word
		if self.max_hint_number is not None:
			number_of_better_scoring_positive_words = min(self.max_hint_number, number_of_better_scoring_positive_words)
		return number_of_better_scoring_positive_words
	
	@classmethod
	def hint_filter(cls, hint, word):
		# substring filter
		if hint in word or word in hint:
			return False
		
		# length filter
		if len(hint) < 3:
			return False
		
		# levenshtein distance filter
		distance = cls.levenshtein_distance(hint, word)
		max_distance = max(len(hint), len(word))
		relative_distance = distance / max_distance
		if relative_distance <= 0.5:
			levenshtein_log_file = os.path.join(config.logs_directory, 'levenshtein.log')
			with open(levenshtein_log_file, 'a', encoding='utf-8') as f:
				print('Excluding hint \'{}\' as candidate for word \'{}\' (LEVENSHTEIN = {}/{})'.format(hint, word, distance, max_distance), file=f)
			return False
		
		return True
	
	@classmethod
	def levenshtein_distance(cls, word1, word2, insertion_cost=1, deletion_cost=1, substitution_cost=1):
		"""If padding is True, the end of the shortest word is padded. Padded characters allow for free substitution.
		For example, if l1 is the length of the shortest word, we take (l2 - l1) + 1 slices of word2 and take the minimum levenshtein distance between these slices and word1.
		The padded words (should) give the same behaviour.
		"""
		l1 = len(word1)
		l2 = len(word2)
		
		distance_matrix = [[0 for _ in range(l2 + 1)] for _ in range(l1 + 1)]
		
		for j in range(1, l2 + 1):
			distance_matrix[0][j] = j * deletion_cost
		
		for i in range(1, l1 + 1):
			distance_matrix[i][0] = i * insertion_cost
		
		for i in range(1, l1 + 1):
			for j in range(1, l2 + 1):
				subs = 0 if word1[i-1] == word2[j-1] else substitution_cost
				distance_matrix[i][j] = min(distance_matrix[i-1][j-1] + subs, distance_matrix[i-1][j] + insertion_cost, distance_matrix[i][j-1] + deletion_cost)
		
		return distance_matrix[l1][l2]

class WeightedHintGenerator(HintGenerator):
	def __init__(self, *args, weighting_method='weighting.t_score', weights=None, **kwargs):
		super().__init__(*args, **kwargs)
		self.weighting_method = load_function_from_string(weighting_method) # lookup function indicated by weighting_method and replace it
		self.weights = weights

class ThresholdWeightedHintGenerator(HintGenerator):
	def __init__(self, *args, weighting_methods=None, **kwargs):
		super().__init__(*args, **kwargs)
		self.weighting_methods = tuple(
			(load_function_from_string(weighting_method), top_n, threshold)
			for weighting_method, top_n, threshold in weighting_methods
		)
