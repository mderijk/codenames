

from ... import generators

word2vec_embeddings_model_cz = 'data/wiki.cs/wiki-czeng-filtered-top-10000.cs.vec'
word2vec_embeddings_model_cz_v2 = 'data/wiki.cs/wiki-czeng-filtered-similar-top-1000-frequency-top-10000.cs.vec'
collocations_model_cz = 'data/collocations/sentence_level_collocations_filtered_cz_v1.0.col'
dependency_based_collocations_model_cz = 'data/collocations/dependency_level_collocations_filtered_cz_v1.0.col'
syntactic_collocations_model_cz = 'data/collocations/syntactic_collocations_filtered_cz_v1.0.col'

word2vec_embeddings_model_en = 'data/wiki.en/wiki-czeng-filtered-top-10000.en.vec'
word2vec_embeddings_model_en_v2 = 'data/wiki.en/wiki-czeng-filtered-similar-top-1000-frequency-top-10000.en.vec'
collocations_model_en = 'data/collocations/sentence_level_collocations_filtered_en_v1.0.col'
dependency_based_collocations_model_en = 'data/collocations/dependency_level_collocations_filtered_en_v1.0.col'
syntactic_collocations_model_en = 'data/collocations/syntactic_collocations_filtered_en_v1.0.col'

GENERATORS = {
	# Models based on syntactic collocations seem to perform decently. They can sometimes give you a hint for 4 or 5 words and leave you amazed. Other times they don't even give you a good hint for one. It's a bit of both, and when inspecting the PMI values, the dependency ones seem to be more accurate, so we think those models have more of a future.
	'syntactic_collocations_combined_top_3_cz_v1.0': {
		'class': generators.collocations.SyntacticCollocationsHintGenerator,
		'model': syntactic_collocations_model_cz,
		'frequency_cutoff': 1000,
		'weighting_method': generators.weighting.top_3,
		'weights': (1, 1.2, 1, 2),
	},
	'syntactic_collocations_combined_top_3_en_v1.0': {
		'class': generators.collocations.SyntacticCollocationsHintGenerator,
		'model': syntactic_collocations_model_en,
		'frequency_cutoff': 1000,
		'weighting_method': generators.weighting.top_3,
		'weights': (1, 1.2, 1, 2),
	},
	
	# sixth test run
	'word2vec_weighted_top_1_cz_v1.1': {
		'class': generators.word2vec.WeightedWord2vecHintGenerator,
		'model': word2vec_embeddings_model_cz,
		'include_number': True,
		'max_hint_number': 1,
		'weighting_method': generators.weighting.top_1,
		'weights': (1, 1.2, 1, 2),
	},
	'word2vec_weighted_top_2_cz_v1.1': {
		'class': generators.word2vec.WeightedWord2vecHintGenerator,
		'model': word2vec_embeddings_model_cz,
		'include_number': True,
		'max_hint_number': 2,
		'weighting_method': generators.weighting.top_2,
		'weights': (1, 1.2, 1, 2),
	},
	'word2vec_weighted_top_3_cz_v1.1': {
		'class': generators.word2vec.WeightedWord2vecHintGenerator,
		'model': word2vec_embeddings_model_cz,
		'include_number': True,
		'max_hint_number': 3,
		'weighting_method': generators.weighting.top_3,
		'weights': (1, 1.2, 1, 2),
	},
	'word2vec_weighted_top_combined_cz_v1.1': {
		'class': generators.word2vec.ThresholdWeightedWord2vecHintGenerator,
		'model': word2vec_embeddings_model_cz,
		'weighting_methods': (
			(generators.weighting.top_3, 3, 0.28209114),
			(generators.weighting.top_2, 2, 0.38748214),
			(generators.weighting.top_1, 1, None), # default to this method if none of the thresholds are met
		),
		'weights': (1, 1.2, 1, 2),
	},
	
	# cancelled test run (linear threshold competition (if the numbers are equal of course))
	# 'dep_col_and_word_embeddings_combined_threshold_cz_v1.0': {
		# 'class': generators.super.ThresholdSuperHintGenerator,
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
		# 'class': generators.super.ThresholdSuperHintGenerator,
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
	# NOTE: the generators used by any SuperHintGenerator must be run on the same server.
	#		Additionally, it is your responsibility to enable the generators that it depends on in the normal config.
	'dep_col_and_word_embeddings_combined_cz_v1.0': {
		'class': generators.super.SuperHintGenerator,
		'model': (
			'dependency_based_collocations_top_combined_cz_v1.0',
			'word2vec_weighted_top_combined_cz_v1.0',
		),
		'top_n': 500,
		'max_hint_number': 3,
	},
	'dep_col_and_word_embeddings_combined_en_v1.0': {
		'class': generators.super.SuperHintGenerator,
		'model': (
			'dependency_based_collocations_top_combined_en_v1.0',
			'word2vec_weighted_top_combined_en_v1.0',
		),
		'top_n': 500,
		'max_hint_number': 3,
	},
	
	# 4.5th test run
	# 'word2vec_weighted_top_combined_cz_v1.1': {
		# 'class': generators.word2vec.ThresholdWeightedWord2vecHintGenerator,
		# 'model': word2vec_embeddings_model_cz_v2,
		# 'weighting_methods': (
			# (generators.weighting.top_3, 3, 0.28209114),
			# (generators.weighting.top_2, 2, 0.38748214),
			# (generators.weighting.top_1, 1, None), # default to this method if none of the thresholds are met
		# ),
		# 'weights': (1, 1.2, 1, 2),
	# },
	# 'word2vec_weighted_top_combined_en_v1.1': {
		# 'class': generators.word2vec.ThresholdWeightedWord2vecHintGenerator,
		# 'model': word2vec_embeddings_model_en_v2,
		# 'weighting_methods': (
			# (generators.weighting.top_3, 3, 0.34984735),
			# (generators.weighting.top_2, 2, 0.37125748),
			# (generators.weighting.top_1, 1, None), # default to this method if none of the thresholds are met
		# ),
		# 'weights': (1, 1.2, 1, 2),
	# },
	
	# fourth test run
	'dependency_based_collocations_top_combined_cz_v1.0': {
		'class': generators.collocations.ThresholdDependencyBasedCollocationsHintGenerator,
		'model': dependency_based_collocations_model_cz,
		'frequency_cutoff': 1000,
		'weighting_methods': (
			(generators.weighting.top_3, 3, 9.299208329296569),
			(generators.weighting.top_2, 2, 10.811084816565739),
			(generators.weighting.top_1, 1, None), # default to this method if none of the thresholds are met
		),
		'weights': (1, 1.2, 1, 2),
	},
	'dependency_based_collocations_top_combined_en_v1.0': {
		'class': generators.collocations.ThresholdDependencyBasedCollocationsHintGenerator,
		'model': dependency_based_collocations_model_en,
		'frequency_cutoff': 1000,
		'weighting_methods': (
			(generators.weighting.top_3, 3, 6.945942848881148),
			(generators.weighting.top_2, 2, 9.653435486873398),
			(generators.weighting.top_1, 1, None), # default to this method if none of the thresholds are met
		),
		'weights': (1, 1.2, 1, 2),
	},
	'word2vec_weighted_top_combined_cz_v1.0': {
		'class': generators.word2vec.ThresholdWeightedWord2vecHintGenerator,
		'model': word2vec_embeddings_model_cz,
		'weighting_methods': (
			(generators.weighting.top_3, 3, 0.28209114),
			(generators.weighting.top_2, 2, 0.38748214),
			(generators.weighting.top_1, 1, None), # default to this method if none of the thresholds are met
		),
		'weights': (1, 1.2, 1, 2),
	},
	'word2vec_weighted_top_combined_en_v1.0': {
		'class': generators.word2vec.ThresholdWeightedWord2vecHintGenerator,
		'model': word2vec_embeddings_model_en,
		'weighting_methods': (
			(generators.weighting.top_3, 3, 0.34984735),
			(generators.weighting.top_2, 2, 0.37125748),
			(generators.weighting.top_1, 1, None), # default to this method if none of the thresholds are met
		),
		'weights': (1, 1.2, 1, 2),
	},
	
	# third test run
	'word2vec_weighted_top_1_cz_v1.0': {
		'class': generators.word2vec.WeightedWord2vecHintGenerator,
		'model': word2vec_embeddings_model_cz,
		'include_number': False,
		'max_hint_number': 1,
		'weighting_method': generators.weighting.top_1,
		'weights': (1, 1.2, 1, 2),
	},
	'word2vec_weighted_top_2_cz_v1.0': {
		'class': generators.word2vec.WeightedWord2vecHintGenerator,
		'model': word2vec_embeddings_model_cz,
		'include_number': False,
		'max_hint_number': 2,
		'weighting_method': generators.weighting.top_2,
		'weights': (1, 1.2, 1, 2),
	},
	'word2vec_weighted_top_3_cz_v1.0': {
		'class': generators.word2vec.WeightedWord2vecHintGenerator,
		'model': word2vec_embeddings_model_cz,
		'include_number': False,
		'max_hint_number': 3,
		'weighting_method': generators.weighting.top_3,
		'weights': (1, 1.2, 1, 2),
	},
	'word2vec_weighted_top_1_en_v1.0': {
		'class': generators.word2vec.WeightedWord2vecHintGenerator,
		'model': word2vec_embeddings_model_en,
		'include_number': True,
		'max_hint_number': 1,
		'weighting_method': generators.weighting.top_1,
		'weights': (1, 1.2, 1, 2),
	},
	'word2vec_weighted_top_2_en_v1.0': {
		'class': generators.word2vec.WeightedWord2vecHintGenerator,
		'model': word2vec_embeddings_model_en,
		'include_number': True,
		'max_hint_number': 2,
		'weighting_method': generators.weighting.top_2,
		'weights': (1, 1.2, 1, 2),
	},
	'word2vec_weighted_top_3_en_v1.0': {
		'class': generators.word2vec.WeightedWord2vecHintGenerator,
		'model': word2vec_embeddings_model_en,
		'include_number': True,
		'max_hint_number': 3,
		'weighting_method': generators.weighting.top_3,
		'weights': (1, 1.2, 1, 2),
	},
	
	# second test run
	'dependency_based_collocations_top_1_cz_v1.0': {
		'class': generators.collocations.DependencyBasedCollocationsHintGenerator,
		'model': dependency_based_collocations_model_cz,
		'frequency_cutoff': 1000,
		'include_number': True,
		'max_hint_number': 1,
		'weighting_method': generators.weighting.top_1,
		'weights': (1, 1.2, 1, 2),
	},
	'dependency_based_collocations_top_2_cz_v1.0': {
		'class': generators.collocations.DependencyBasedCollocationsHintGenerator,
		'model': dependency_based_collocations_model_cz,
		'frequency_cutoff': 1000,
		'include_number': True,
		'max_hint_number': 2,
		'weighting_method': generators.weighting.top_2,
		'weights': (1, 1.2, 1, 2),
	},
	'dependency_based_collocations_top_3_cz_v1.0': {
		'class': generators.collocations.DependencyBasedCollocationsHintGenerator,
		'model': dependency_based_collocations_model_cz,
		'frequency_cutoff': 1000,
		'include_number': True,
		'max_hint_number': 3,
		'weighting_method': generators.weighting.top_3,
		'weights': (1, 1.2, 1, 2),
	},
	'dependency_based_collocations_top_1_en_v1.0': {
		'class': generators.collocations.DependencyBasedCollocationsHintGenerator,
		'model': dependency_based_collocations_model_en,
		'frequency_cutoff': 1000,
		'include_number': True,
		'max_hint_number': 1,
		'weighting_method': generators.weighting.top_1,
		'weights': (1, 1.2, 1, 2),
	},
	'dependency_based_collocations_top_2_en_v1.0': {
		'class': generators.collocations.DependencyBasedCollocationsHintGenerator,
		'model': dependency_based_collocations_model_en,
		'frequency_cutoff': 1000,
		'include_number': True,
		'max_hint_number': 2,
		'weighting_method': generators.weighting.top_2,
		'weights': (1, 1.2, 1, 2),
	},
	'dependency_based_collocations_top_3_en_v1.0': {
		'class': generators.collocations.DependencyBasedCollocationsHintGenerator,
		'model': dependency_based_collocations_model_en,
		'frequency_cutoff': 1000, # top ~16000
		'include_number': True,
		'max_hint_number': 3,
		'weighting_method': generators.weighting.top_3,
		'weights': (1, 1.2, 1, 2),
	},
	
	# first test run
	'word2vec_simple_cz_v1.0': {
		'class': generators.word2vec.Word2vecHintGenerator,
		'model': word2vec_embeddings_model_cz,
	},
	'word2vec_weighted_combined_max_score_cz_v1.0': {
		'class': generators.word2vec.WeightedWord2vecHintGenerator,
		'model': word2vec_embeddings_model_cz,
		'include_number': False,
		'weighting_method': generators.weighting.combined_max_score,
		'weights': (1, 1.2, 1, 2),
	},
	'collocations_combined_max_score_cz_v1.0': {
		'class': generators.collocations.CollocationsHintGenerator,
		'model': collocations_model_cz,
		'frequency_cutoff': 1000,
		'include_number': False,
		'weighting_method': generators.weighting.combined_max_score,
		'weights': (1, 1.2, 1, 2),
	},
	'dependency_based_collocations_mean_difference_cz_v1.0': {
		'class': generators.collocations.DependencyBasedCollocationsHintGenerator,
		'model': dependency_based_collocations_model_cz,
		'frequency_cutoff': 1000,
		'include_number': False,
		'weighting_method': generators.weighting.mean_difference,
		'weights': (1, 1.2, 1, 2),
	},
	'dependency_based_collocations_combined_max_score_cz_v1.0': {
		'class': generators.collocations.DependencyBasedCollocationsHintGenerator,
		'model': dependency_based_collocations_model_cz,
		'frequency_cutoff': 1000,
		'include_number': False,
		'weighting_method': generators.weighting.combined_max_score,
		'weights': (1, 1.2, 1, 2),
	},
	'word2vec_simple_en_v1.0': {
		'class': generators.word2vec.Word2vecHintGenerator,
		'model': word2vec_embeddings_model_en,
	},
	'word2vec_weighted_combined_max_score_en_v1.0': {
		'class': generators.word2vec.WeightedWord2vecHintGenerator,
		'model': word2vec_embeddings_model_en,
		'include_number': False,
		'weighting_method': generators.weighting.combined_max_score,
		'weights': (1, 1.2, 1, 2),
	},
	'collocations_combined_max_score_en_v1.0': {
		'class': generators.collocations.CollocationsHintGenerator,
		'model': collocations_model_en,
		'frequency_cutoff': 1000,
		'include_number': False,
		'weighting_method': generators.weighting.combined_max_score,
		'weights': (1, 1.2, 1, 2),
	},
	'dependency_based_collocations_mean_difference_en_v1.0': {
		'class': generators.collocations.DependencyBasedCollocationsHintGenerator,
		'model': dependency_based_collocations_model_en,
		'frequency_cutoff': 1000,
		'include_number': False,
		'weighting_method': generators.weighting.mean_difference,
		'weights': (1, 1.2, 1, 2),
	},
	'dependency_based_collocations_combined_max_score_en_v1.0': {
		'class': generators.collocations.DependencyBasedCollocationsHintGenerator,
		'model': dependency_based_collocations_model_en,
		'frequency_cutoff': 1000,
		'include_number': False,
		'weighting_method': generators.weighting.combined_max_score,
		'weights': (1, 1.2, 1, 2),
	},
}
