
import argparse
import os
import sys

from collocator import CollocationFinder, DependencyBasedCollocationFinder, SentenceLevelCollocationFinder, SyntacticCollocationFinder

def load_lexicon(filename):
	lexicon = set()
	with open(filename, encoding='utf-8') as f:
		for line in f:
			word = line.strip()
			word = word.lower()
			if word:
				lexicon.add(word)
	
	return lexicon

def get_sentences(language, keep_dependencies=False, keep_parts_of_speech=False):
	if language in ('en', 'cz'):
		import czeng
		corpus_directory = os.path.join('data', 'çzeng')
		sentences = czeng.open_filtered_files(corpus_directory, language, keep_dependencies=keep_dependencies, keep_parts_of_speech=keep_parts_of_speech, verbose=True)
	else:
		raise Exception('Unknown language \'{}\'.'.format(language))
	
	return sentences

def get_collocation_finder(language, sentence_level=False, dependency_level=False, syntactic=False):
	os.makedirs('data/collocations', exist_ok=True)
	
	col_filename = 'collocations_' + language + '.col'
	Collocator = CollocationFinder
	kwargs = {}
	if sentence_level:
		Collocator = SentenceLevelCollocationFinder
		col_filename = 'sentence_level_' + col_filename
	elif dependency_level:
		Collocator = DependencyLevelCollocationFinder
		col_filename = 'dependency_level_' + col_filename
	elif syntactic:
		Collocator = SyntacticCollocationFinder
		col_filename = 'syntactic_' + col_filename
		if language == 'cz': # czech and english have different morphological/syntactic tags :(
			kwargs['allowed_pos_tags'] = ('N', 'V', 'A')
		elif language == 'en':
			kwargs['allowed_pos_tags'] = ('N', 'V', 'J')
	
	collocations_filename = os.path.join('data', 'collocations', col_filename)
	if os.path.isfile(collocations_filename):
		collocator = Collocator.load(collocations_filename)
	else:
		sentences = get_sentences(language, keep_dependencies=dependency_level, keep_parts_of_speech=syntactic)
		lexicon_filename = os.path.join('data', 'lexicons', 'original_trimmed_' + language + '.txt')
		lexicon = load_lexicon(lexicon_filename)
		collocator = Collocator(sentences, lexicon, verbose=True, **kwargs)
		collocator.save(collocations_filename)
	
	return collocator

def generate_collocations(model, own_team_words, enemy_team_words, neutral_words, assassin_words, frequency_cutoff=100):
	collocation_scores = {} # {word: ([<own_team_score>], [<enemy_team_score>], [<neutral_score>], [<assassin_score>])}
	unigrams_cutoff = (unigram for unigram, frequency in model.unigram_frequencies.items() if frequency >= frequency_cutoff)
	for word2 in unigrams_cutoff:
		collocation_scores[word2] = ([], [], [], [])
		for group_index, words in enumerate((own_team_words, enemy_team_words, neutral_words, assassin_words)):
			for word in words:
				score = model.calculate_pointwise_mutual_information(word, word2)
				collocation_scores[word2][group_index].append(score)
	
	return collocation_scores

def score_collocations(collocation_scores, n=20, weighting_method=None, weights=None):
	if weighting_method is None:
		import weighting
		weighting_method = weighting.t_score
	
	matches = [] # [(score, word)]
	for word, scores in collocation_scores.items():
		own_team_scores, enemy_team_scores, neutral_scores, assassin_scores = scores
		if weights is None:
			weighted_score = weighting_method(own_team_scores, enemy_team_scores, neutral_scores, assassin_scores)
		else:
			weighted_score = weighting_method(own_team_scores, enemy_team_scores, neutral_scores, assassin_scores, weights=weights)
		matches.append((weighted_score, word, scores))
	
	return list(sorted(matches, reverse=True)[:n])

def test(args):
	language = args.language
	model = get_collocation_finder(language, sentence_level=args.sentence_level, dependency_level=args.dependency_level, syntactic=args.syntactic)
	own_team_words = ['pan', 'ivory', 'compound', 'organ', 'buck', 'bear', 'root', 'laser', 'drill']
	enemy_team_words = ['spell', 'alps', 'fan', 'cell', 'unicorn', 'jack', 'cotton', 'soul']
	neutral_words = ['conductor', 'card', 'slug', 'cover', 'carrot', 'code', 'knight']
	assassin_words = ['war']
	collocation_scores = generate_collocations(model, own_team_words, enemy_team_words, neutral_words, assassin_words, frequency_cutoff=1000)
	collocations = score_collocations(collocation_scores, weights=(1, 1.2, 1, 2))
	for weighted_score, word, individual_scores in collocations:
		print('{:.3f}'.format(weighted_score), word)
		for words, scores in zip((own_team_words, enemy_team_words, neutral_words, assassin_words), individual_scores):
			word_scores = sorted(zip(words, map('{:.3f}'.format, scores)), key=lambda x: float(x[1]), reverse=True)
			print('', ' '.join(map(' '.join, word_scores)), sep='\t')

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('language', choices=('cz', 'en'), help='Language.')
	parser.add_argument('-s', '--sentence-level', action='store_true', help='Enable sentence-level collocations.')
	parser.add_argument('-x', '--syntactic', action='store_true', help='Enable syntactic collocations.')
	parser.add_argument('-d', '--dependency-level', action='store_true', help='Enable dependency-level collocations.')
	args = parser.parse_args()
	
	test(args)
