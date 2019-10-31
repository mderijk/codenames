
# Ladies and gentlemen, may I present to you, the Super Generator! *hesitant applause*
# 
# A SuperHintGenerator accepts a list of generators and thresholds as its model, which tells the super generator which other generators to call and which generator answer to accept if it passes the threshold.

import re

from ..ai import AI
from .hintgenerator import HintGenerator

class SuperHintGenerator(HintGenerator):
	def generateHint(self, game_id, positive_words, negative_words, neutral_words, assassin_words, previous_hints, n=20):
		with self.logger.openLog(game_id) as self.log:
			for generator_name, threshold in self.model:
				# create connection with AI
				ai = AI(generator_name)
				
				# reset hints log before querying
				hints_log_directory = os.path.join(self.logger.log_directory, '..', ai.name)
				hints_log = os.path.join(hints_log_directory, 'superhintgenerator.log')
				open(hints_log, 'w', encoding='utf-8').close()
				
				# ask for hint
				hint = ai.generateHint('superhintgenerator', own_team_words, enemy_team_words, neutral_words, assassin_words)
				
				# prevent crashes
				if not hint:
					return None
				
				# inspect superhintgenerator.log and steal ratings
				overall_rating, board_ratings = extract_hint_rating_and_board(hints_log, hint)
				own_card_ratings = board_ratings[0]
				
				# make decision
				rating = own_card_ratings[0]
				if rating >= threshold or rating is None:
					self.log.log('Generated hint \'{}\' with rating \'{}\''.format(hint, overall_rating))
					self.log.log('Used model \'{}\' and crossed threshold \'{}\''.format(generator_name, threshold))
					return hint

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
