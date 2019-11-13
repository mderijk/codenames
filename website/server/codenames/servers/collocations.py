
from .. import collocations
from .hintgenerator import HintGenerator
from . import weighting

class CollocationsHintGenerator(HintGenerator):
	model_loader = collocations.CollocationFinder.load
	
	def __init__(self, model, *args, frequency_cutoff=100, include_number=True, weighting_method=weighting.t_score, weights=None, **kwargs):
		super().__init__(model, *args, **kwargs)
		self.frequency_cutoff = frequency_cutoff
		self.include_number = include_number
		self.weighting_method = weighting_method
		self.weights = weights
	
	def _generateCollocations(self, own_team_words, enemy_team_words, neutral_words, assassin_words, n=20):
		collocation_scores = {} # {word: ([<own_team_score>], [<enemy_team_score>], [<neutral_score>], [<assassin_score>])}
		unigrams_cutoff = (unigram for unigram, frequency in self.model.unigram_frequencies.items() if frequency >= self.frequency_cutoff)
		for word2 in unigrams_cutoff:
			collocation_scores[word2] = ([], [], [], [])
			for group_index, words in enumerate((own_team_words, enemy_team_words, neutral_words, assassin_words)):
				for word in words:
					score = self.model.calculate_pointwise_mutual_information(word, word2)
					collocation_scores[word2][group_index].append(score)
		
		matches = [] # [(score, word)]
		for word, scores in collocation_scores.items():
			own_team_scores, enemy_team_scores, neutral_scores, assassin_scores = scores
			if self.weights is None:
				weighted_score = self.weighting_method(own_team_scores, enemy_team_scores, neutral_scores, assassin_scores)
			else:
				weighted_score = self.weighting_method(own_team_scores, enemy_team_scores, neutral_scores, assassin_scores, weights=self.weights)
			matches.append((weighted_score, word, scores))
		
		return list(sorted(matches, reverse=True)[:n])
	
	def generateHints(self, positive_words, negative_words, neutral_words, assassin_words, previous_hints, n=20):
		collocations = self._generateCollocations(positive_words, negative_words, neutral_words, assassin_words, n=n)
		weighted_scores, words, individual_scores_list = zip(*collocations)
		self.individual_scores_dict = dict(zip(words, individual_scores_list))
		return zip(words, weighted_scores)
	
	def generateHint(self, game_id, positive_words, negative_words, neutral_words, assassin_words, previous_hints, n=20):
		hint, number = super().generateHint(game_id, positive_words, negative_words, neutral_words, assassin_words, previous_hints, n=n)
		pmi_scores = [[(word, score) for word, score in zip(word_group, scores)] for word_group, scores in zip([positive_words, negative_words, neutral_words, assassin_words], self.individual_scores_dict[hint])]
		if self.include_number:
			number = self.calculate_number(*pmi_scores)
		
		with self.logger.openLog(game_id) as self.log:
			self.log.log('PMI scores for', hint, *pmi_scores)
		
		self.individual_scores_dict = None
		
		return hint, number

class DependencyBasedCollocationsHintGenerator(CollocationsHintGenerator):
	model_loader = collocations.DependencyBasedCollocationFinder.load
