
# Ladies and gentlemen, may I present to you, the Super Generator! *hesitant applause*
# 
# A SuperHintGenerator accepts a list of generators and thresholds as its model, which tells the super generator which other generators to call and which generator answer to accept if it passes the threshold.
# NOTE: the models used by any SuperHintGenerator must be run on a separate server, otherwise that server instance will block when the SuperHintGenerator is queried.

import os
import re

from ..ai import AI
from .hintgenerator import HintGenerator

class SuperHintGenerator(HintGenerator):
	def generateHint(self, game_id, positive_words, negative_words, neutral_words, assassin_words, previous_hints, n=20):
		with self.logger.openLog(game_id) as self.log:
			for generator_name, top_n, threshold in self.model:
				# create connection with AI
				ai = AI(generator_name)
				
				# ask for hint
				hint_word, hint_number = ai.generateHint(game_id, positive_words, negative_words, neutral_words, assassin_words, n=n, previous_hints=previous_hints)
				
				# prevent crashes
				if not hint_word:
					return None
				
				# inspect generator log file and steal ratings
				hints_log_directory = os.path.join(self.logger.log_directory, '..', ai.name)
				hints_log = os.path.join(hints_log_directory, '{}.log'.format(game_id))
				overall_rating, board_ratings = extract_hint_rating_and_board(hints_log, hint_word)
				own_card_ratings = board_ratings[0]
				
				# make decision
				ratings = [rating for word, rating in own_card_ratings[:top_n]]
				rating = ratings[-1]
				if threshold is None or rating >= threshold:
					self.log.log('Generated hint \'{}\' with rating \'{}\''.format(hint_word, overall_rating))
					self.log.log('Used model \'{}\' and crossed threshold \'{}\''.format(generator_name, threshold))
					self.log.log('Weighted scores from', ai.name, 'for', hint_word, *board_ratings)
					return hint_word, hint_number

def parse_card_rating_string(string):
	cards = zip([match.group(1) for match in re.finditer('\'(\w+)\'', string)], [float(match.group()) for match in re.finditer('\d+(\.\d+)?', string)])
	cards = list(sorted(cards, key=lambda x: x[1], reverse=True))
	return cards

def extract_hint_rating_and_board(hints_log, target_hint):
	board = []
	is_target_hint = False
	with open(hints_log, encoding='utf-8') as f:
		for line in f:
			line = line.strip()
			if 'Generated hint' in line:
				hint = line.split(' ')[3][1:-1]
				if hint == target_hint:
					is_target_hint = True
					rating = float(line.split(' ')[6][1:-1])
			elif 'Cosine similarities' in line or 'PMI scores' in line:
				if is_target_hint:
					board_string = '['.join(line.split('[')[1:]) # remove text before the board string
					own_cards, enemy_cards, neutral_cards, assassin_cards = map(parse_card_rating_string, board_string.split('] ['))
					board = (own_cards, enemy_cards, neutral_cards, assassin_cards)
					break
	
	return rating, board