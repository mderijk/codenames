
from collections import defaultdict
import itertools
import math

import gensim
import numpy as np

from .hintgenerator import HintGenerator
from . import weighting

class Word2vecHintGenerator(HintGenerator):
	model_loader = gensim.models.KeyedVectors.load_word2vec_format
	
	def __init__(self, model, *args, weights=None, **kwargs):
		super().__init__(model, *args, **kwargs)
		self.weights = weights
	
	def generateHints(self, positive_words, negative_words, neutral_words, assassin_words, previous_hints, n=20):
		if self.weights:
			positive_words = list(map(lambda x: (x, self.weights[0]), positive_words))
			assassin_words = list(map(lambda x: (x, self.weights[3]), assassin_words))
		similar_words = self.model.most_similar(positive=positive_words, negative=assassin_words, topn=n)
		return similar_words
	
	def generateHint(self, game_id, positive_words, negative_words, neutral_words, assassin_words, previous_hints, n=20):
		hint = super().generateHint(game_id, positive_words, negative_words, neutral_words, assassin_words, previous_hints, n=n)
		
		with self.logger.openLog(game_id) as self.log:
			cosine_similarities = [[(word, self.model.similarity(hint, word)) for word in words] for words in [positive_words, negative_words, neutral_words, assassin_words]]
			self.log.log('Cosine similarities for', hint, *cosine_similarities)
		
		return hint

class AveragedWord2vecHintGenerator(Word2vecHintGenerator):
	def generateHints(self, positive_words, negative_words, neutral_words, assassin_words, previous_hints, n=20):
		self.potential_hint_combinations = defaultdict(dict)
		potential_hints = defaultdict(list)
		for combinations in [itertools.combinations(positive_words, 1), itertools.combinations(positive_words, 2), itertools.combinations(positive_words, 3), itertools.combinations(positive_words, 4)]:
			for combination in combinations:
				similar_words = self.model.most_similar(positive=combination, negative=assassin_words, topn=n)
				for hint, rating in similar_words:
					potential_hints[hint].append(rating ** 2)
					self.potential_hint_combinations[hint][combination] = rating
		
		if not potential_hints or (len(previous_hints) > len(potential_hints) and len(set(potential_hints.keys()) - set(previous_hints)) == 0):
			return [('error', 1.0)] # TODO: return proper error
		
		potential_hints = {hint: sum(ratings) / len(ratings) for hint, ratings in potential_hints.items()} # take the average of all ratings
		potential_hints = list(sorted(potential_hints.items(), key=lambda x: x[1], reverse=True))
		return potential_hints
	
	def generateHint(self, game_id, positive_words, negative_words, neutral_words, assassin_words, previous_hints, n=20):
		hint = super().generateHint(game_id, positive_words, negative_words, neutral_words, assassin_words, previous_hints, n=n)
		
		with self.logger.openLog(game_id) as self.log:
			self.log.warning((hint, len(set(item for combination in self.potential_hint_combinations[hint] for item in combination)), self.potential_hint_combinations[hint]))
		
		self.potential_hint_combinations = None
		
		return hint

class WeightedWord2vecHintGenerator(Word2vecHintGenerator):
	def __init__(self, *args, weighting_method=weighting.combined_max_score, weights=None, **kwargs):
		super().__init__(*args, **kwargs)
		self.weighting_method = weighting_method
		self.weights = weights
	
	def generateHints(self, positive_words, negative_words, neutral_words, assassin_words, previous_hints, n=20):
		words_grouped = [positive_words, negative_words, neutral_words, assassin_words]
		all_words = set()
		word_dists = []
		for words in words_grouped:
			word_dists.append([])
			for word in words:
				assert word in self.model.vocab, 'Word \'{}\', taken from the lexicon, does not occur in the vocabulary of the word embeddings.'.format(word) # word is assumed to be in self.model.vocab
				all_words.add(self.model.vocab[word].index)
				vector = self.model.word_vec(word)
				dists = self.model.cosine_similarities(vector, self.model.vectors)
				word_dists[-1].append(dists)
		word_dists = list(map(np.array, word_dists))
		
		# combine distances for each hint
		weighting_method = weighting.for_all(self.weighting_method)
		if self.weights is None:
			combined_dists = weighting_method(*word_dists)
		else:
			combined_dists = weighting_method(*word_dists, weights=self.weights)
		
		best = gensim.matutils.argsort(combined_dists, topn=n + len(all_words), reverse=True)
		potential_hints = {self.model.index2word[sim]: float(combined_dists[sim]) for sim in best if not sim in all_words}
		self.potential_hint_combinations = {self.model.index2word[sim]: [(word, float(dists[sim])) for words_group, word_dists_group in zip(words_grouped, word_dists) for word, dists in zip(words_group, word_dists_group)] for sim in best if not sim in all_words}
		
		potential_hints = list(sorted(potential_hints.items(), key=lambda x: x[1], reverse=True))
		return potential_hints
	
	def generateHint(self, game_id, positive_words, negative_words, neutral_words, assassin_words, previous_hints, n=20):
		hint = super().generateHint(game_id, positive_words, negative_words, neutral_words, assassin_words, previous_hints, n=n)
		
		with self.logger.openLog(game_id) as self.log:
			self.log.warning(hint, len(self.potential_hint_combinations[hint]), self.potential_hint_combinations[hint])
		
		self.potential_hint_combinations = None
		
		return hint
