
class HintGenerator:
	model_cache = {}
	model_loader = lambda x: x
	
	def __init__(self, model, logger, max_hint_number=None):
		self.model = self._load_model(model)
		self.logger = logger
		self.max_hint_number = max_hint_number
	
	def _load_model(self, model_name):
		if model_name not in self.model_cache:
			self.model_cache[model_name] = self.__class__.model_loader(model_name)
		return self.model_cache[model_name]
	
	def generateHints(self, positive_words, negative_words, neutral_words, assassin_words, previous_hints, n=20):
		""" To be implemented by classes inheriting from HintGenerator. """
		raise NotImplementedError
	
	def generateHint(self, game_id, positive_words, negative_words, neutral_words, assassin_words, previous_hints, n=20):
		with self.logger.openLog(game_id) as self.log:
			# keep generating hints until you find one that passes all the tests
			while True:
				potential_hints = self.generateHints(positive_words, negative_words, neutral_words, assassin_words, previous_hints, n=n)
				
				previous_words = [word for word, number in previous_hints]
				for hint, rating in potential_hints:
					if all(map(lambda word: self.hint_filter(hint, word), positive_words + negative_words + neutral_words + assassin_words + previous_words)):
						self.log.log('Generated hint \'{}\' with rating \'{}\''.format(hint, rating))
						return hint, None
				
				n += 20
				
				if n > 1000:
					raise StopIteration('No suitable hint could be found.')
	
	def calculate_number(self, positive_words, negative_words, neutral_words, assassin_words):
		highest_negative_rating = max(rating2 for _, rating2 in negative_words + neutral_words + assassin_words)
		number_of_better_scoring_positive_words = sum(1 for _, rating in positive_words if rating >= highest_negative_rating) # "better scoring" means equal to or higher than the highest negative word
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
			with open('logs/levenshtein.log', 'a', encoding='utf-8') as f:
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
