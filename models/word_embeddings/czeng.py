
from collections import Counter
import lzma
import re
import os

from czeng_faulty_sections import faulty_sections

def filter_file(filename):
	with lzma.open(filename, mode='rt', encoding='utf-8') as f:
		for line in f:
			match = re.match(r'^[^-]+-b(\d+)-\d\d[tde]', line)
			
			if not match:
				raise ValueError('Incorrect line format')
			
			if match.group(1) not in faulty_sections:
				yield line

def filter_files(directory, verbose=False):
	""" Reads .xz files in (sub)directories of <directory>, returning line by line. """
	for root, dirs, filenames in os.walk(directory):
		for filename in filenames:
			if filename.endswith('.xz'):
				file_path = os.path.join(root, filename)
				if verbose:
					print('Reading sentences from file \'{}\''.format(file_path))
				yield from filter_file(file_path)

def extract_sentence_from_line(line, language):
	offset = 0
	if language == 'en':
		offset = 4
	
	line = line.strip()
	columns = line.split('\t')
#	domain_id, block_number, section, file_number, sentence_number = columns[0].split('-')
#	filter_score = float(columns[1])
#	czech_a_layer = columns[2]
#	for czech_token_information in czech_a_layer.split(' '):
#		czech_word_form, czech_lemma, czech_tag, czech_index_in_sentence, czech_index_of_governor, czech_syntactic_function = czech_token_information.split('|')
#		czech_words.append(czech_lemma)
#	czech_tectogrammatical_layer = columns[3]
#	czech_a_t_correspondence_content_words = columns[4]
#	czech_a_t_correspondence_auxiliary_words = columns[5]
#	english_a_layer = columns[6]
#	for english_token_information in english_a_layer.split(' '):
#		english_word_form, english_lemma, english_tag, english_index_in_sentence, english_index_of_governor, english_syntactic_function = english_token_information.split('|')
#		english_words.append(english_lemma)
#	english_tectogrammatical_layer = columns[7]
#	english_a_t_correspondence_content_words = columns[8]
#	english_a_t_correspondence_auxiliary_words = columns[9]
#	giza_alignments = columns[10]
#	giza_alignments = columns[11]
#	giza_alignments = columns[12]
#	giza_alignments = columns[13]
#	t_alignment_there = columns[14]
#	t_alignment_back = columns[15]
#	additional_rule_based_t_alignment = columns[16]
	
	a_layer = columns[2 + offset]
	sentence = []
	for token_information in a_layer.split(' '):
		word_form, lemma, tag, index_in_sentence, index_of_governor, syntactic_function = token_information.split('|')
		sentence.append(lemma.lower())
	
	return sentence

def open_filtered_files(directory, language, verbose=False):
	for line in filter_files(directory, verbose=verbose):
		yield extract_sentence_from_line(line, language)

def get_lemmas(language):
	if language in ('en', 'cz'):
		corpus_directory = os.path.join('data', 'czeng')
		lemmas = open_filtered_files(corpus_directory, language, verbose=True)
		lemmas = Counter(lemma for sentence_lemmas in lemmas for lemma in sentence_lemmas)
		
		if not lemmas:
			raise Exception('No .xz files found in directory \'{}\'.'.format(os.path.abspath(corpus_directory)))
	else:
		raise ValueError('Unknown language \'{}\'.'.format(language))
	
	return lemmas
