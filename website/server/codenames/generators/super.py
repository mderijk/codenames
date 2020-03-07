
# Ladies and gentlemen, may I present to you, the Super Generator! *hesitant applause*
# 
# A SuperHintGenerator accepts a list of generators and thresholds as its model, which tells the super generator which other generators to call and which generator answer to accept if it passes the threshold.
# NOTE: the models used by any SuperHintGenerator must run on the same server.

from collections import defaultdict
import os
import re

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
		
		self.log.warning('FAILURE: NO BEST HINT FOUND after', self.top_n, 'tries')

class ThresholdSuperHintGenerator(SuperHintGenerator):
	def __init__(self, model, ranges, *args, **kwargs):
		super().__init__(model, *args, top_n=None, **kwargs)
		self.ranges = ranges
	
	def generateHints(self, positive_words, negative_words, neutral_words, assassin_words, previous_hints):
		options = []
		
		for index, generator in enumerate(self.model.values()):
			range_start, range_end = self.ranges[index]
			# ask for hints
			hints = generator.generateHints(positive_words, negative_words, neutral_words, assassin_words, previous_hints=previous_hints, verbose=False)
			hint, weighted_score = next(hints)
			number = generator.calculate_number(*generator.scores[hint])
			normalized_weighted_score = weighted_score / (range_end - range_start) # score between 0 and 1
			options.append((number, normalized_weighted_score, hint, generator, hints, range_start, range_end))
		
		try:
			while True:
				options.sort(reverse=True)
				
				number, normalized_weighted_score, hint, generator, hints, range_start, range_end = options[0]
				self.scores = generator.scores
				self.log.log('Used model', generator.__class__, 'for hint', hint)
				yield hint, normalized_weighted_score
				
				# if the hint was rejected or we need to generate another hint, let's get another hint from the generator from which was the hint that was rejected
				options = options[1:]
				
				hint, weighted_score = next(hints)
				number = generator.calculate_number(*generator.scores[hint])
				normalized_weighted_score = weighted_score / (range_end - range_start) # score between 0 and 1
				options.append((number, normalized_weighted_score, hint, generator, hints, range_start, range_end))
		except StopIteration:
			print('Ran out of valid hints with model', self.model, file=sys.stderr)
		
		self.log.warning('FAILURE: NO VALID HINT FOUND')
