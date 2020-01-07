
# Find good thresholds for dependency collocations

import argparse
from collections import Counter, defaultdict
import os
import pickle

from parse_game_files import get_games

def analyze_dep_rel_labels(args, version='v1.0'):
	language = args.language
	method = args.method
	decision_cards_index = {
		'own': 0,
		'enemy': 1,
		'neutral': 2,
		'assassin': 3,
	}
	
	games = get_games('data')
	decision_ratings_by_ai = defaultdict(list)
	number_of_games_by_ai = Counter()
	for game in games:
		ai_name = game['ai_name']
		if version in ai_name and '_{}_'.format(language) in ai_name and method in ai_name and 'top_combined' in ai_name:
			number_of_games_by_ai[ai_name] += 1
			
			hinted_at = set()
			for index, ((hint, overall_rating), number, decisions, board) in enumerate(zip(game['hints'], game['numbers'], game['decisions'], game['hints_board'])):
				# filter suitable decisions (decisions where the player selected the most related own card, i.e. the card that the AI was referring to the most with the hint it gave)
				highest_negative_rating = max(rating2 for _, rating2 in board[1] + board[2] + board[3])
				top_n = number
				turn_words = set(word for word, rating in board[0][:top_n] if rating >= highest_negative_rating)
#				hinted_at.update(turn_words)
				
				for index, (decision_word, decision) in enumerate(decisions):
#					if turn_words and index < top_n:
					decision_word = decision_word.lower()
					cards = board[decision_cards_index[decision]]
					hinted_at = decision_word in turn_words # hinted at this turn
					
					correct = (2 if hinted_at else 1) if decision == 'own' else 0
#						ratings = [rating for word, rating in board[0][:top_n] if word in turn_words]
					rating = [rating for word, rating in cards if word == decision_word][0]
#						rating = tuple(card for card in board[0] if card[0] in turn_words)[0][1]
#						rating = overall_rating
#						bad_cards = board[1] + board[2] + board[3]
#						rating = sum(rating for _, rating in board[0]) / len(board[0]) - sum(rating for _, rating in bad_cards) / len(bad_cards)
					
					decision_ratings_by_ai[ai_name].append((rating, correct))
#						if decision_word not in hinted_at:
#							decision_ratings_by_ai[ai_name].append((rating, 0))
#						else:
#							decision_ratings_by_ai[ai_name].append((rating, 1))
					
#						if decision_word in turn_words:
#							turn_words.remove(decision_word)
	
	for ai_name, decision_ratings in decision_ratings_by_ai.items():
		print(ai_name, number_of_games_by_ai[ai_name], sep='\t')
		for rating, correct in sorted(decision_ratings):
			print(correct, rating)

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('language', choices=('cz', 'en'), help='Language.')
	parser.add_argument('method', choices=('dependency', 'word2vec'), help='Language.')
	args = parser.parse_args()
	
	analyze_dep_rel_labels(args)

if __name__ == '__main__':
	main()
