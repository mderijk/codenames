
GENERATORS = {
	# 'dep_col_and_word_embeddings_combined_threshold_cz_v1.0': {
		# 'class': 'super.ThresholdSuperHintGenerator',
		# 'model': (
			# 'dependency_based_collocations_top_combined_cz_v1.0',
			# 'word2vec_weighted_top_combined_cz_v1.0',
		# ),
		# 'ranges': (
			# (0, 55),
			# (0.0, 3.0),
		# ),
		# 'max_hint_number': 3,
	# },
	# 'dep_col_and_word_embeddings_combined_threshold_en_v1.0': {
		# 'class': 'super.ThresholdSuperHintGenerator',
		# 'model': (
			# 'dependency_based_collocations_top_combined_en_v1.0',
			# 'word2vec_weighted_top_combined_en_v1.0',
		# ),
		# 'ranges': (
			# (0, 55),
			# (0.0, 3.0),
		# ),
		# 'max_hint_number': 3,
	# },
	
	# fifth test run
	# NOTE: the 'generators used by' any SuperHintGenerator must be run on the same server.
	#		Additionally, it is your responsibility to enable the 'generators that it' depends on in the normal config.
	'dep_col_and_word_embeddings_combined_cz_v1.0': {
		'class': 'super.SuperHintGenerator',
		'model': (
			'dependency_based_collocations_top_combined_cz_v1.0',
			'word2vec_weighted_top_combined_cz_v1.0',
		),
		'top_n': 500,
		'max_hint_number': 3,
	},
	'dep_col_and_word_embeddings_combined_en_v1.0': {
		'class': 'super.SuperHintGenerator',
		'model': (
			'dependency_based_collocations_top_combined_en_v1.0',
			'word2vec_weighted_top_combined_en_v1.0',
		),
		'top_n': 500,
		'max_hint_number': 3,
	},
}
