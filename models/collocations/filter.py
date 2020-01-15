
import os
import sys

import collocations

def load_lexicon(filename):
	lexicon = set()
	with open(filename, encoding='utf-8') as f:
		for line in f:
			word = line.strip()
			word = word.lower()
			if word:
				lexicon.add(word)
	
	return lexicon

def filter_collocator(language, collocator_filename_format='collocations_filtered_{}.col', frequency_cutoff=0, sentence_level=False, dependency_level=False, syntactic=False):
	""" Load a collection of collocations and keep only those collocations (word1, word2) where:
	- the word1 is in the lexicon of that language
	- both word1 and word2 contain only alphabetic characters
	- the collocation count is equal to or higher than frequency_cutoff
	
	frequency_cutoff > 0 can be used to reduce the size of the resulting file.
	"""
	# load trimmed lexicon
	lexicon_filename = os.path.join('data', 'lexicons', 'original_trimmed_' + language + '.txt')
	lexicon = load_lexicon(lexicon_filename)
	
	# load collocator
	collocator = collocations.get_collocation_finder(language, sentence_level=sentence_level, dependency_level=dependency_level, syntactic=syntactic)
	
	# remove hints that contain non-alphabetic characters
	for unigram in list(collocator.unigram_frequencies.keys()):
		if not unigram.isalpha():
			del collocator.unigram_frequencies[unigram]
	for bigram in list(collocator.bigram_frequencies.keys()):
		if not bigram[1].isalpha():
			del collocator.bigram_frequencies[bigram]
	
	if frequency_cutoff:
		# collect and remove infrequent unigrams
		infrequent_unigrams = set()
		for unigram, count in list(collocator.unigram_frequencies.items()):
			if count < frequency_cutoff and unigram not in lexicon: # remove words that occur less often than <frequency_cutoff> and are not in the lexicon
				infrequent_unigrams.add(unigram)
				del collocator.unigram_frequencies[unigram]
		
		# remove bigrams containing infrequent unigrams as hints
		for bigram in list(collocator.bigram_frequencies.keys()):
			if bigram[1] in infrequent_unigrams:
				del collocator.bigram_frequencies[bigram]
	
	# save collocator
	collocator_filename = os.path.join('data', 'collocations', collocator_filename_format.format(language))
	collocator.save(collocator_filename)

def main(argv):
	if len(argv) == 2:
		filter_collocator(argv[1], collocator_filename_format='sentence_level_collocations_filtered_{}.col', frequency_cutoff=100, sentence_level=True)
		filter_collocator(argv[1], collocator_filename_format='dependency_level_collocations_filtered_{}.col', dependency_level=True)
		filter_collocator(argv[1], collocator_filename_format='syntactic_collocations_filtered_{}.col', syntactic=True)
	else:
		print('USAGE: {} <language>'.format(argv[0]), file=sys.stderr)

if __name__ == '__main__':
	main(sys.argv)
