
from collections import Counter
import math

class CollocationFinder:
	def __init__(self, sentences, lexicon, verbose=False):
		self.unigram_frequencies = Counter()
		self.bigram_frequencies = Counter()
		
		if verbose:
			print('Counting unigrams and bigrams..')
		
		multi_word_expressions_in_lexicon = any(' ' in word for word in lexicon)
		
		for sentence in sentences:
			self.unigram_frequencies.update(sentence)
			
			relevant_words = (word for word in sentence if word in lexicon)
			
			if multi_word_expressions_in_lexicon:
				# make sure that unigrams and bigrams for words with spaces (e.g. 'ice cream') are generated as well (only as word1, because the hint (word2) should always be a single word, i.e. should not contain spaces)
				grouped_words = map(' '.join, zip(sentence, sentence[1:]))
				for word_group in grouped_words:
					if word_group in lexicon:
						relevant_words = list(relevant_words)
						self.unigram_frequencies[word_group] += 1
						relevant_words.append(word_group)
			
			# add bigrams
			for word1 in relevant_words:
				for word2 in sentence:
					if word1 != word2: # avoid duplicates because we are not allowed to use the word itself as a hint anyway
						bigram = (word1, word2)
						self.bigram_frequencies[bigram] += 1
		
		if verbose:
			print('Calculating probabilities..')
		
		self.calculate_probabilities()
	
	def calculate_probabilities(self):
		total_unigram_count = sum(self.unigram_frequencies.values())
		self.unigram_probabilities = {unigram: frequency / total_unigram_count for unigram, frequency in self.unigram_frequencies.items()}
		
		total_bigram_count = sum(self.bigram_frequencies.values())
		self.bigram_probabilities = {bigram: frequency / total_bigram_count for bigram, frequency in self.bigram_frequencies.items()}
	
	def _calculate_pointwise_mutual_information(self, word1_probability, word2_probability, bigram_probability):
		pmi = math.log2(
			bigram_probability /
			(word1_probability * word2_probability)
		)
		return pmi
	
	def calculate_pointwise_mutual_information(self, word1, word2):
		bigram = (word1, word2)
		if bigram in self.bigram_probabilities:
			word1_probability = self.unigram_probabilities[word1]
			word2_probability = self.unigram_probabilities[word2]
			bigram_probability = self.bigram_probabilities[bigram]
			score = self._calculate_pointwise_mutual_information(word1_probability, word2_probability, bigram_probability)
			return score
		
		return 0
	
	def find_best_collocations(self, word1, n=10, frequency_cutoff=10):
		matches = []
		unigrams_cutoff = (unigram for unigram, frequency in self.unigram_frequencies.items() if frequency >= frequency_cutoff)
		for word2 in unigrams_cutoff:
			score = self.calculate_pointwise_mutual_information(word1, word2)
			matches.append((score, word2))
		
		return sorted(matches, reverse=True)[:n]
	
	def save(self, filename):
		with open(filename, 'w', encoding='utf-8') as f:
			for unigram, frequency in self.unigram_frequencies.items():
				print('unigram', unigram, frequency, sep='\t', file=f)
			
			for bigram, frequency in self.bigram_frequencies.items():
				print('bigram', bigram[0], bigram[1], frequency, sep='\t', file=f)
	
	@classmethod
	def load(cls, filename):
		collocator = cls([], [])
		unigram_frequencies = {}
		bigram_frequencies = {}
		with open(filename, encoding='utf-8') as f:
			for line in f:
				line = line.strip()
				if line.startswith('unigram'):
					unigram, frequency = line.split('\t')[1:]
					collocator.unigram_frequencies[unigram] = int(frequency)
				elif line.startswith('bigram'):
					word1, word2, frequency = line.split('\t')[1:]
					bigram = (word1, word2)
					collocator.bigram_frequencies[bigram] = int(frequency)
		
		collocator.calculate_probabilities()
		
		return collocator


class DependencyBasedCollocationFinder(CollocationFinder):
	def __init__(self, sentences, lexicon, verbose=False):
		self.unigram_frequencies = Counter()
		self.bigram_frequencies = Counter()
		
		if verbose:
			print('Counting unigrams and bigrams..')
		
		for sentence, dependencies in sentences:
			self.unigram_frequencies.update(sentence)
			
			# get relevant dependency-based bigrams
			relevant_bigrams = []
			for index, word1 in enumerate(sentence):
				index_of_governor = dependencies[index]
				if index_of_governor != 0:
					word2 = sentence[index_of_governor - 1]
					if not word1.startswith('#') and not word2.startswith('#'): # filter out function words that start with a #
						if word1 in lexicon:
							relevant_bigrams.append((word1, word2))
						if word2 in lexicon:
							relevant_bigrams.append((word2, word1))
			
			# add bigrams
			for word1, word2 in relevant_bigrams:
				if word1 != word2: # avoid duplicates because we are not allowed to use the word itself as a hint anyway
					bigram = (word1, word2)
					self.bigram_frequencies[bigram] += 1
		
		if verbose:
			print('Calculating probabilities..')
		
		self.calculate_probabilities()
