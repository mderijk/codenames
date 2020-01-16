
from collections import defaultdict
import os

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle as Rectangle
import matplotlib.ticker as mtick

from parse_game_files import get_games

BUCKETS = {
	'baseline': [
		'game_start',
		'random',
	],
	'first_czech': [
		'baseline',
		'collocations_combined_max_score_cz_v1.0',
		'dependency_based_collocations_combined_max_score_cz_v1.0',
		'dependency_based_collocations_mean_difference_cz_v1.0',
		'word2vec_simple_cz_v1.0',
		'word2vec_weighted_combined_max_score_cz_v1.0',
	],
	'first_english': [
		'baseline',
		'collocations_combined_max_score_en_v1.0',
		'dependency_based_collocations_combined_max_score_en_v1.0',
		'dependency_based_collocations_mean_difference_en_v1.0',
		'word2vec_simple_en_v1.0',
		'word2vec_weighted_combined_max_score_en_v1.0',
	],
	'improved_dep_czech': [
		'baseline',
		'dependency_based_collocations_top_1_cz_v1.0',
		'dependency_based_collocations_top_2_cz_v1.0',
		'dependency_based_collocations_top_3_cz_v1.0',
	],
	'improved_dep_english': [
		'baseline',
		'dependency_based_collocations_top_1_en_v1.0',
		'dependency_based_collocations_top_2_en_v1.0',
		'dependency_based_collocations_top_3_en_v1.0',
	],
	'improved_we_czech': [
		'baseline',
		'word2vec_weighted_top_1_cz_v1.0',
		'word2vec_weighted_top_2_cz_v1.0',
		'word2vec_weighted_top_3_cz_v1.0',
	],
	'improved_we_english': [
		'baseline',
		'word2vec_weighted_top_1_en_v1.0',
		'word2vec_weighted_top_2_en_v1.0',
		'word2vec_weighted_top_3_en_v1.0',
	],
	'top_n': [
		'baseline',
		'dependency_based_collocations_top_combined_cz_v1.0',
		'dependency_based_collocations_top_combined_en_v1.0',
		'word2vec_weighted_top_combined_cz_v1.0',
		'word2vec_weighted_top_combined_en_v1.0',
	],
	'final': [
		'baseline',
		'dep_col_and_word_embeddings_combined_cz_v1.0',
		'dep_col_and_word_embeddings_combined_en_v1.0',
	],
}

FILE_NAMES = {
	'baseline': 'game-data_decisions_baseline.pdf',
	'first_czech': 'game-data_decisions_initial_models_czech.pdf',
	'first_english': 'game-data_decisions_initial_models_english.pdf',
	'improved_dep_czech': 'game-data_decisions_improved_dependency_models_czech.pdf',
	'improved_dep_english': 'game-data_decisions_improved_dependency_models_english.pdf',
	'improved_we_czech': 'game-data_decisions_improved_word_embedding_models_czech.pdf',
	'improved_we_english': 'game-data_decisions_improved_word_embedding_models_english.pdf',
	'top_n': 'game-data_decisions_top_n_models.pdf',
	'final': 'game-data_decisions_final_models.pdf',
	'collocations_combined_max_score_cz_v1.0': 'game-data_decisions_sent_col_cms_cz.pdf',
	'collocations_combined_max_score_en_v1.0': 'game-data_decisions_sent_col_cms_en.pdf',
	'dep_col_and_word_embeddings_combined_cz_v1.0': 'game-data_decisions_dep_col_we_combined_cz.pdf',
	'dep_col_and_word_embeddings_combined_en_v1.0': 'game-data_decisions_dep_col_we_combined_en.pdf',
	'dependency_based_collocations_combined_max_score_cz_v1.0': 'game-data_decisions_dep_col_cms_cz.pdf',
	'dependency_based_collocations_combined_max_score_en_v1.0': 'game-data_decisions_dep_col_cms_en.pdf',
	'dependency_based_collocations_mean_difference_cz_v1.0': 'game-data_decisions_dep_col_md_cz.pdf',
	'dependency_based_collocations_mean_difference_en_v1.0': 'game-data_decisions_dep_col_md_en.pdf',
	'dependency_based_collocations_top_1_cz_v1.0': 'game-data_decisions_dep_col_top_1_cz.pdf',
	'dependency_based_collocations_top_1_en_v1.0': 'game-data_decisions_dep_col_top_1_en.pdf',
	'dependency_based_collocations_top_2_cz_v1.0': 'game-data_decisions_dep_col_top_2_cz.pdf',
	'dependency_based_collocations_top_2_en_v1.0': 'game-data_decisions_dep_col_top_2_en.pdf',
	'dependency_based_collocations_top_3_cz_v1.0': 'game-data_decisions_dep_col_top_3_cz.pdf',
	'dependency_based_collocations_top_3_en_v1.0': 'game-data_decisions_dep_col_top_3_en.pdf',
	'dependency_based_collocations_top_combined_cz_v1.0': 'game-data_decisions_dep_col_top_n_cz.pdf',
	'dependency_based_collocations_top_combined_en_v1.0': 'game-data_decisions_dep_col_top_n_en.pdf',
	'word2vec_simple_cz_v1.0': 'game-data_decisions_we_most_similar_cz.pdf',
	'word2vec_simple_en_v1.0': 'game-data_decisions_we_most_similar_en.pdf',
	'word2vec_weighted_combined_max_score_cz_v1.0': 'game-data_decisions_we_cms_cz.pdf',
	'word2vec_weighted_combined_max_score_en_v1.0': 'game-data_decisions_we_cms_en.pdf',
	'word2vec_weighted_top_1_cz_v1.0': 'game-data_decisions_we_top_1_cz.pdf',
	'word2vec_weighted_top_1_en_v1.0': 'game-data_decisions_we_top_1_en.pdf',
	'word2vec_weighted_top_2_cz_v1.0': 'game-data_decisions_we_top_2_cz.pdf',
	'word2vec_weighted_top_2_en_v1.0': 'game-data_decisions_we_top_2_en.pdf',
	'word2vec_weighted_top_3_cz_v1.0': 'game-data_decisions_we_top_3_cz.pdf',
	'word2vec_weighted_top_3_en_v1.0': 'game-data_decisions_we_top_3_en.pdf',
	'word2vec_weighted_top_combined_cz_v1.0': 'game-data_decisions_we_top_combined_cz.pdf',
	'word2vec_weighted_top_combined_en_v1.0': 'game-data_decisions_we_top_combined_en.pdf',
}

LABEL_NAMES = {
	'game_start': 'Game start',
	'random': 'Random',
	'baseline': 'Baseline',
	'collocations_combined_max_score_cz_v1.0': 'Sentence\nCM',
	'collocations_combined_max_score_en_v1.0': 'Sentence\nCM',
	'dep_col_and_word_embeddings_combined_cz_v1.0': 'Czech',
	'dep_col_and_word_embeddings_combined_en_v1.0': 'English',
	'dependency_based_collocations_combined_max_score_cz_v1.0': 'Dependency\nCM',
	'dependency_based_collocations_combined_max_score_en_v1.0': 'Dependency\nCM',
	'dependency_based_collocations_mean_difference_cz_v1.0': 'Dependency\nMeanDiff',
	'dependency_based_collocations_mean_difference_en_v1.0': 'Dependency\nMeanDiff',
	'dependency_based_collocations_top_1_cz_v1.0': 'Top1',
	'dependency_based_collocations_top_1_en_v1.0': 'Top1',
	'dependency_based_collocations_top_2_cz_v1.0': 'Top2',
	'dependency_based_collocations_top_2_en_v1.0': 'Top2',
	'dependency_based_collocations_top_3_cz_v1.0': 'Top3',
	'dependency_based_collocations_top_3_en_v1.0': 'Top3',
	'dependency_based_collocations_top_combined_cz_v1.0': 'Dependency\nCzech',
	'dependency_based_collocations_top_combined_en_v1.0': 'Dependency\nEnglish',
	'word2vec_simple_cz_v1.0': 'WE\nMost similar',
	'word2vec_simple_en_v1.0': 'WE\nMost similar',
	'word2vec_weighted_combined_max_score_cz_v1.0': 'WE\nCM',
	'word2vec_weighted_combined_max_score_en_v1.0': 'WE\nCM',
	'word2vec_weighted_top_1_cz_v1.0': 'Top1',
	'word2vec_weighted_top_1_en_v1.0': 'Top1',
	'word2vec_weighted_top_2_cz_v1.0': 'Top2',
	'word2vec_weighted_top_2_en_v1.0': 'Top2',
	'word2vec_weighted_top_3_cz_v1.0': 'Top3',
	'word2vec_weighted_top_3_en_v1.0': 'Top3',
	'word2vec_weighted_top_combined_cz_v1.0': 'WE Czech',
	'word2vec_weighted_top_combined_en_v1.0': 'WE English',
}

def calculate_decision_counts(games):
	decision_cards_index = {
		'own': 0,
		'enemy': 1,
		'neutral': 2,
		'assassin': 3,
	}
	decision_counts = {decision: 0 for decision in decision_cards_index}
	
	# tally decision counts for each AI
	for game in games:
		for decisions in game['decisions']:
			for _, decision in decisions:
				decision_counts[decision] += 1
	
	return decision_counts

def plot(data_directory, **kwargs):
	games = get_games(data_directory)
	
	# gather ai_names
	ai_names = set()
	for game in games:
		ai_names.add(game['ai_name'])
	
	# group games by ai
	games_by_ai = {ai_name: [] for ai_name in ai_names}
	for game in games:
		games_by_ai[game['ai_name']].append(game)
	
	# calculate decision counts for each AI
	decision_counts_by_ai = {}
	for ai_name, games in games_by_ai.items():
		# calculate decision counts for this AI
		decision_counts_by_ai[ai_name] = calculate_decision_counts(games)
	
	# add game start
	decision_counts_by_ai['game_start'] = {
		'own': 9,
		'enemy': 8,
		'neutral': 7,
		'assassin': 1,
	}
	
	# add baseline
	random = {
		'own': 30514319,
		'enemy': 18737374,
		'neutral': 24544662,
		'assassin': 4542184,
	}
	decision_counts_by_ai['random'] = random
	decision_counts_by_ai['baseline'] = random
	
	# sort into buckets based on first five characters
	buckets = defaultdict(dict)
	for bucket_name, bucket in BUCKETS.items():
		for ai_name in bucket:
			buckets[bucket_name][ai_name] = decision_counts_by_ai[ai_name]
	
	# graph decision counts for each AI
	decision_cards_index = {
		'own': 0,
		'enemy': 1,
		'neutral': 2,
		'assassin': 3,
	}
	COLORS = {
		0: plt.rcParams['axes.prop_cycle'].by_key()['color'][0],
		1: plt.rcParams['axes.prop_cycle'].by_key()['color'][3],
		2: plt.rcParams['axes.prop_cycle'].by_key()['color'][1],
		3: plt.rcParams['axes.prop_cycle'].by_key()['color'][4],
	}
	
	for bucket_name, decision_counts_by_ai in sorted(buckets.items()):
		samples = {}
		for ai_name, decision_counts in sorted(decision_counts_by_ai.items()):
			print(ai_name)
			
			# normalize decision counts
			total_decision_count = sum(decision_counts.values())
			renamed_decision_counts = {decision_cards_index[decision]: decision_count for decision, decision_count in decision_counts.items()}
			labels, normalized_decision_counts = zip(*[(decision, decision_count / total_decision_count) for decision, decision_count in sorted(renamed_decision_counts.items())])
			decision_percentages = [normalized_decision_count * 100 for normalized_decision_count in normalized_decision_counts]
			sample = pd.Series(decision_percentages)
			print(*decision_percentages)
			samples[LABEL_NAMES[ai_name]] = sample
		
		# graph decision counts for this AI
#		colors = [COLORS[label] for label in labels] * len(samples)
		indices, values = zip(*sorted(samples.items()))
		own, enemy, neutral, assassin = zip(*values)
		df = pd.DataFrame({'Own': own, 'Enemy': enemy, 'Neutral': neutral, 'Assassin': assassin}, index=indices)
		ax = df.plot(color=[color for _, color in sorted(COLORS.items())], **kwargs)
		ax.set(ylabel='Percentage of decisions') # percentage of decisions taken per method
		ax.yaxis.set_major_formatter(mtick.PercentFormatter())
#		ax.get_xaxis().set_visible(False)
#		if is_dep:
#			ax.set_ylim((0, 20))
#		elif is_we:
#			ax.set_ylim((0, 1))
#		own = Rectangle((0, 0), 20, 20, color=COLORS[0])
#		enemy = Rectangle((0, 0), 20, 20, color=COLORS[1])
#		neutral = Rectangle((0, 0), 20, 20, color=COLORS[2])
#		assassin = Rectangle((0, 0), 20, 20, color=COLORS[3])
		ax.legend(loc='upper right') # loc='best'
		fig = ax.get_figure()
		if bucket_name != 'baseline':
			plt.rcParams.update({'font.size': 16})
			width = fig.get_figwidth()
			fig.set_figwidth(width * len(indices) / 3)
		else:
			plt.rcParams.update({'font.size': 14})
		os.makedirs('images', exist_ok=True)
		fig.savefig('images/' + FILE_NAMES[bucket_name], bbox_inches='tight')
#		plt.show()

def main():
	plot('data', kind='bar', rot=0)

if __name__ == '__main__':
	main()
