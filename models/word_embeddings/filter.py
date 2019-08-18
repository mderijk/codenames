
import os
import pickle
import sys

import czeng

# Applies Czeng lemma filtering on the given word embeddings file
# - iterate through czeng corpus and get the set of unique lemmas (czeng.get_lemmas)
# - remove all word embeddings from the file for which the word is not in the set of unique lemmas
# Removes words that do not contain only alphabetic characters
# Takes only the first N embeddings that pass through the filter (the input embeddings file is expected to have been sorted by frequency)

def load_lexicon(filename):
	lexicon = set()
	with open(filename, encoding='utf-8') as f:
		for line in f:
			word = line.strip()
			word = word.lower()
			if word:
				lexicon.add(word)
	
	return lexicon

def get_czeng_lemmas(language):
	czeng_lemmas_filename = os.path.join(os.path.dirname(__file__), 'czeng_lemmas_{}.pickle'.format(language))
	if os.path.isfile(czeng_lemmas_filename):
		with open(czeng_lemmas_filename, 'rb') as f:
			lemmas = pickle.load(f)
	else:
		lemmas = czeng.get_lemmas(language)
		with open(czeng_lemmas_filename, 'wb') as f:
			pickle.dump(lemmas, f)
	
	return lemmas

def filter(filename, new_filename, language, lexicon, vector_count):
	# get lemmas in the czeng corpus
	lemmas = get_czeng_lemmas(language)
	
	print('Scanning word embeddings file...')
	lexicon_included = set()
	with open(filename, encoding='utf-8') as source:
		number_of_vectors, vector_length = source.readline().rstrip().split()
		vector_length = int(vector_length)
		
		for index, line in enumerate(source):
			line = line.rstrip()
			
			elements = line.split(' ')
			word = ' '.join(elements[:-vector_length])
			
			word = word.lower()
			if word in lexicon:
				lexicon_included.add(word)
	
	lexicon_diff = lexicon - lexicon_included
	if len(lexicon_diff) > 0:
		print('WARNING: Did not encounter word embeddings for {} words that are in the lexicon:'.format(len(lexicon_diff)))
		for word in lexicon_diff:
			print(word)
		
		trimmed_lexicon_file = os.path.join('data', 'lexicons', 'original_trimmed_' + language + '.txt')
		print('Writing trimmed lexicon to file', trimmed_lexicon_file)
		with open(trimmed_lexicon_file, 'w', encoding='utf-8') as f:
			for word in sorted(lexicon_included):
				print(word, file=f)
		
		# change the lexicon to the lexicon that includes only words for which we have word embeddings
		lexicon = lexicon_included
	
	print('Assembling new word embeddings file...')
	# write all word embeddings to the new file that have a lemma in the czeng corpus
	with open(filename, encoding='utf-8') as source, open(new_filename, 'w', encoding='utf-8') as target:
		number_of_vectors, vector_length = source.readline().rstrip().split()
		number_of_vectors = vector_count
		print(number_of_vectors, vector_length, file=target)
		vector_length = int(vector_length)
		
		number_of_vectors_written = 0
		number_of_lexicon_words_to_go = len(lexicon)
		
		if number_of_lexicon_words_to_go > number_of_vectors:
			print('WARNING: More words in lexicon ({}) than the number of word embeddings you requested ({}).'.format(number_of_lexicon_words_to_go, number_of_vectors))
		
		for index, line in enumerate(source):
			line = line.rstrip()
			
			elements = line.split(' ')
			word = ' '.join(elements[:-vector_length])
			
			# filter: word is lemma in czeng corpus, lemma occurs 50 times or more and lemma is alphabetic
			word = word.lower()
			if (word in lemmas and lemmas[word] >= 50 and word.isalpha()) or word in lexicon:
				if number_of_vectors_written + number_of_lexicon_words_to_go >= number_of_vectors and word not in lexicon: # if there are any lexicon words that you did not include yet, skip other candidates until you find the word embeddings for the lexicon words.
					continue
				
				print(line, file=target)
				number_of_vectors_written += 1
				if word in lexicon:
					number_of_lexicon_words_to_go -= 1
			
			if number_of_vectors_written >= number_of_vectors:
				break
		else:
			print('WARNING: Not enough word embeddings pass the filter to take {} word embeddings. Took {} word embeddings instead.'.format(number_of_vectors, number_of_vectors_written))

def main(argv):
	if len(argv) == 5:
		# load lexicon so we can check if there is any word that we should still include even if it has no equivalent lemma in czeng
		language = argv[3]
		lexicon_filename = os.path.join('data', 'lexicons', 'original_' + language + '.txt')
		lexicon = load_lexicon(lexicon_filename)
		
		# filter file
		filter(argv[1], argv[2], language, lexicon, int(argv[4]))
	else:
		print('USAGE: {} <filename> <new filename> <language> <amount of lines to copy>'.format(argv[0]), file=sys.stderr)

if __name__ == '__main__':
	main(sys.argv)
