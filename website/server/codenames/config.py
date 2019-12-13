
# Config file

hints_log_directory = 'data/hints'

LANGUAGES = ['cz', 'en']

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
				'word2vec_weighted_top_1_cz_v1.1',
				'word2vec_weighted_top_2_cz_v1.1',
				'word2vec_weighted_top_3_cz_v1.1',
#				'word2vec_weighted_top_combined_cz_v1.0',
				'word2vec_weighted_top_combined_cz_v1.1',
			],
			'log_directory': hints_log_directory,
		},
	},
	'word2vec_en': {
		'socket': ('localhost', 3163),
		'config': {
			'generators': [
#				'word2vec_simple_en_v1.0',
#				'word2vec_weighted_combined_max_score_en_v1.0',
				'word2vec_weighted_top_1_en_v1.0',
				'word2vec_weighted_top_2_en_v1.0',
				'word2vec_weighted_top_3_en_v1.0',
				'word2vec_weighted_top_combined_en_v1.0',
#				'word2vec_weighted_top_combined_en_v1.1',
			],
			'log_directory': hints_log_directory,
		},
	},
	'collocations_cz': {
		'socket': ('localhost', 3064),
		'config': {
			'generators': [
#				'collocations_combined_max_score_cz_v1.0',
			],
			'log_directory': hints_log_directory,
		},
	},
	'collocations_en': {
		'socket': ('localhost', 3164),
		'config': {
			'generators': [
#				'collocations_combined_max_score_en_v1.0',
			],
			'log_directory': hints_log_directory,
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
			'log_directory': hints_log_directory,
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
			'log_directory': hints_log_directory,
		},
	},
	'super_cz': {
		'socket': ('localhost', 3066),
		'config': {
			'generators': [
#				'word2vec_weighted_top_combined_cz_v1.0',
#				'dependency_based_collocations_top_combined_cz_v1.0',
#				'dep_col_and_word_embeddings_combined_cz_v1.0',
#				'dep_col_and_word_embeddings_combined_threshold_cz_v1.0',
			],
			'log_directory': hints_log_directory,
		},
	},
	'super_en': {
		'socket': ('localhost', 3166),
		'config': {
			'generators': [
#				'word2vec_weighted_top_combined_en_v1.0',
#				'dependency_based_collocations_top_combined_en_v1.0',
#				'dep_col_and_word_embeddings_combined_en_v1.0',
#				'dep_col_and_word_embeddings_combined_threshold_en_v1.0',
			],
			'log_directory': hints_log_directory,
		},
	},
}

# active AI
AI_NAMES = {
	'word2vec_weighted_top_1_cz_v1.1': 'AI 0',
	'word2vec_weighted_top_2_cz_v1.1': 'AI 1',
	'word2vec_weighted_top_3_cz_v1.1': 'AI 2',
	'word2vec_weighted_top_combined_cz_v1.1': 'AI 3',
	
	'word2vec_weighted_top_1_en_v1.0': 'AI 0',
	'word2vec_weighted_top_2_en_v1.0': 'AI 1',
	'word2vec_weighted_top_3_en_v1.0': 'AI 2',
	'word2vec_weighted_top_combined_en_v1.0': 'AI 3',
}

#AI_NAMES = {
#	'dep_col_and_word_embeddings_combined_cz_v1.0': 'AI 0',
#	'dependency_based_collocations_top_1_cz_v1.0': 'AI 1',
#	'dependency_based_collocations_top_3_cz_v1.0': 'AI 2',
#	'dependency_based_collocations_top_combined_cz_v1.0': 'AI 3',
#	'word2vec_weighted_top_1_cz_v1.0': 'AI 4',
#	'word2vec_weighted_top_combined_cz_v1.0': 'AI 5',
#	
#	'dependency_based_collocations_top_1_en_v1.0': 'AI 0',
#	'dependency_based_collocations_top_2_en_v1.0': 'AI 1',
#	'dependency_based_collocations_top_3_en_v1.0': 'AI 2',
#	'dependency_based_collocations_top_combined_en_v1.0': 'AI 3',
#	'word2vec_weighted_top_combined_en_v1.0': 'AI 4',
#}


#AI_NAMES = {
#	'dependency_based_collocations_top_combined_cz_v1.0': 'AI 0',
#	'word2vec_weighted_top_combined_cz_v1.1': 'AI 1',
#	'dep_col_and_word_embeddings_combined_cz_v1.0': 'AI 2',
#	'dep_col_and_word_embeddings_combined_threshold_cz_v1.0': 'AI 3',
	
#	'dependency_based_collocations_top_combined_en_v1.0': 'AI 0',
#	'word2vec_weighted_top_combined_en_v1.1': 'AI 1',
#	'dep_col_and_word_embeddings_combined_en_v1.0': 'AI 2',
#	'dep_col_and_word_embeddings_combined_threshold_en_v1.0': 'AI 3',
#}

GENERATOR_NAMES = [generator_name for _, server_data in SERVERS.items() for generator_name in server_data['config']['generators'] if generator_name in AI_NAMES]
GENERATOR_NAMES_BY_LANGUAGE = {
	language: [generator_name for generator_name in GENERATOR_NAMES if '_{}_'.format(language) in generator_name]
	for language in LANGUAGES
}

GENERATOR_SOCKETS = {
	generator_name: server_data['socket']
	for name, server_data in SERVERS.items() for generator_name in server_data['config']['generators']
}
