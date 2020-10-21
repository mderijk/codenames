
# Config file for Codenames

import os

## where to store logs and error messages:
logs_directory = 'logs'

## where to store user data:
data_directory = 'data'

hints_log_directory = os.path.join(data_directory, 'hints')
games_directory = os.path.join(data_directory, 'games')
games_archive_directory = os.path.join(games_directory, 'archive')
games_history_directory = os.path.join(games_directory, 'history')
lexicons_directory = os.path.join(data_directory, 'lexicons')
scores_directory = os.path.join(data_directory, 'scores')
sessions_directory = os.path.join(data_directory, 'sessions')
users_directory = os.path.join(data_directory, 'users')

## which languages you want to support:
LANGUAGES = ['cz', 'en']

## automatically boot the hint servers when a user logs in:
autostart = False

## ask users to log in again after a certain amount of time so we can shut down the servers when no active sessions exist:
session_timeout = 30 * 60 # seconds
server_timeout = session_timeout # if <autostart> is True, hint generation servers automatically shutdown after not being queried for <server_timeout> seconds

## load balancing for when you want to test multiple hint generation algorithms at the same time:
### Each server represents a separate python process. The idea is that when, for example a CZ and an EN player in different games ask for a hint, they don't have to wait for the other person's hint to be generated.
SERVERS = {
	'word2vec_cz': {
		'socket': ('localhost', 3063),
		'config': {
			'generators': [
#				'word2vec_simple_cz_v1.0',
#				'word2vec_weighted_combined_max_score_cz_v1.0',
#				'word2vec_weighted_top_1_cz_v1.0',
#				'word2vec_weighted_top_2_cz_v1.0',
#				'word2vec_weighted_top_3_cz_v1.0',
#				'word2vec_weighted_top_1_cz_v1.1',
#				'word2vec_weighted_top_2_cz_v1.1',
#				'word2vec_weighted_top_3_cz_v1.1',
#				'word2vec_weighted_top_combined_cz_v1.0',
#				'word2vec_weighted_top_combined_cz_v1.1',
			],
			'logs_directory': hints_log_directory,
		},
	},
	'word2vec_en': {
		'socket': ('localhost', 3163),
		'config': {
			'generators': [
#				'word2vec_simple_en_v1.0',
#				'word2vec_weighted_combined_max_score_en_v1.0',
#				'word2vec_weighted_top_1_en_v1.0',
#				'word2vec_weighted_top_2_en_v1.0',
#				'word2vec_weighted_top_3_en_v1.0',
#				'word2vec_weighted_top_combined_en_v1.0',
#				'word2vec_weighted_top_combined_en_v1.1',
			],
			'logs_directory': hints_log_directory,
		},
	},
	'collocations_cz': {
		'socket': ('localhost', 3064),
		'config': {
			'generators': [
#				'collocations_combined_max_score_cz_v1.0',
#				'syntactic_collocations_combined_top_3_cz_v1.0',
			],
			'logs_directory': hints_log_directory,
		},
	},
	'collocations_en': {
		'socket': ('localhost', 3164),
		'config': {
			'generators': [
#				'collocations_combined_max_score_en_v1.0',
#				'syntactic_collocations_combined_top_3_en_v1.0',
			],
			'logs_directory': hints_log_directory,
		},
	},
	'dependency_based_collocations_cz': {
		'socket': ('localhost', 3065),
		'config': {
			'generators': [
#				'dependency_based_collocations_combined_max_score_cz_v1.0',
#				'dependency_based_collocations_mean_difference_cz_v1.0',
#				'dependency_based_collocations_top_1_cz_v1.0',
#				'dependency_based_collocations_top_2_cz_v1.0',
#				'dependency_based_collocations_top_3_cz_v1.0',
#				'dependency_based_collocations_top_combined_cz_v1.0',
#				'dependency_based_collocations_top_combined_cz_v1.1',
			],
			'logs_directory': hints_log_directory,
		},
	},
	'dependency_based_collocations_en': {
		'socket': ('localhost', 3165),
		'config': {
			'generators': [
#				'dependency_based_collocations_combined_max_score_en_v1.0',
#				'dependency_based_collocations_mean_difference_en_v1.0',
#				'dependency_based_collocations_top_1_en_v1.0',
#				'dependency_based_collocations_top_2_en_v1.0',
#				'dependency_based_collocations_top_3_en_v1.0',
#				'dependency_based_collocations_top_combined_en_v1.0',
#				'dependency_based_collocations_top_combined_en_v1.1',
			],
			'logs_directory': hints_log_directory,
		},
	},
	'super_cz': {
		'socket': ('localhost', 3066),
		'config': {
			'generators': [
				'word2vec_weighted_top_combined_cz_v1.0',
#				'dependency_based_collocations_top_combined_cz_v1.0',
#				'dep_col_and_word_embeddings_combined_cz_v1.0',
#				'dep_col_and_word_embeddings_combined_threshold_cz_v1.0',
			],
			'logs_directory': hints_log_directory,
		},
	},
	'super_en': {
		'socket': ('localhost', 3166),
		'config': {
			'generators': [
				'word2vec_weighted_top_combined_en_v1.0',
#				'dependency_based_collocations_top_combined_en_v1.0',
#				'dep_col_and_word_embeddings_combined_en_v1.0',
#				'dep_col_and_word_embeddings_combined_threshold_en_v1.0',
			],
			'logs_directory': hints_log_directory,
		},
	},
}

## active hint generation models (AI) and their names as shown to the user:
### (un)comment a line to enable/disable an AI.
AI_NAMES = {
	'word2vec_weighted_top_combined_cz_v1.0': 'AI 0',
#	'dependency_based_collocations_top_combined_cz_v1.0': 'AI 1',
#	'dep_col_and_word_embeddings_combined_cz_v1.0': 'AI 2',
#	'dep_col_and_word_embeddings_combined_threshold_cz_v1.0': 'AI 3',
	
	'word2vec_weighted_top_combined_en_v1.0': 'AI 0',
#	'dependency_based_collocations_top_combined_en_v1.0': 'AI 1',
#	'dep_col_and_word_embeddings_combined_en_v1.0': 'AI 2',
#	'dep_col_and_word_embeddings_combined_threshold_en_v1.0': 'AI 3',
}
