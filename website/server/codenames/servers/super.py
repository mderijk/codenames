
# Ladies and gentlemen, may I present to you, the Super Generator! *hesitant applause*
# 
# A SuperHintGenerator accepts a list of generators and thresholds as its model, which tells the super generator which other generators to call and which generator answer to accept if it passes the threshold.
# NOTE: the models used by any SuperHintGenerator must run on the same server.

from collections import defaultdict
import os
import re

from ..ai import AI
from .hintgenerator import HintGenerator

class SuperHintGenerator(HintGenerator):
	def __init__(self, model, top_n, *args, include_number=True, **kwargs):
		super().__init__(model, *args, include_number=include_number, **kwargs)
		self.top_n = top_n
	
	def generateHints(self, positive_words, negative_words, neutral_words, assassin_words, previous_hints):
		generated_hints = []
		for generator in self.model.values():
			# ask for self.top_n hints
			hints = generator.generateHints(positive_words, negative_words, neutral_words, assassin_words, previous_hints=previous_hints, verbose=False)
			generated_hints.append((hints, generator))
		
		# search until we find an overlapping hint
		hint_counts = defaultdict(dict)
		max_numbers = defaultdict(int)
		weighted_scores = defaultdict(dict)
		hint_scores = {}
		number_of_methods = len(self.model)
		for tries in range(self.top_n):
			candidates = [(next(hints_), generator) for hints_, generator in generated_hints]
			for index, ((candidate, weighted_score), generator) in enumerate(candidates):
				self.log.log(generator.__class__, candidate, weighted_score)
				
				number = generator.calculate_number(*generator.scores[candidate])
				if number > max_numbers[candidate]:
					max_numbers[candidate] = number
					weighted_scores[candidate][index] = weighted_score
					hint_scores[candidate] = generator.scores
				
				hint_counts[candidate][index] = True
				if len(hint_counts[candidate]) == number_of_methods:
					self.scores = hint_scores[candidate]
					self.log.log('Found candidate hint \'{}\' in {} tries with scores {}'.format(candidate, tries + 1, [weighted_score for index, weighted_score in sorted(weighted_scores[candidate].items())]))
					yield candidate, max_numbers[candidate] # the number of words the hint relates to becomes the "weighted score"
		
		self.log.log('FAILURE: NO BEST HINT FOUND after', self.top_n, 'tries')
