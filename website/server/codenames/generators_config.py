

from . import servers

word2vec_embeddings_model_cz = 'data/wiki.cs/wiki-czeng-filtered-top-10000.cs.vec'
collocations_model_cz = 'data/collocations/sentence_level_collocations_filtered_cz_v1.0.col'
dependency_based_collocations_model_cz = 'data/collocations/dependency_level_collocations_filtered_cz_v1.0.col'

word2vec_embeddings_model_en = 'data/wiki.en/wiki-czeng-filtered-top-10000.en.vec'
collocations_model_en = 'data/collocations/sentence_level_collocations_filtered_en_v1.0.col'
dependency_based_collocations_model_en = 'data/collocations/dependency_level_collocations_filtered_en_v1.0.col'

GENERATORS = {
	# fourth test run
	'dependency_based_collocations_top_combined_cz_v1.0': {
		'class': servers.collocations.SuperHintGenerator,
		'model': tuple(
			('dependency_based_collocations_top_3_cz_v1.0', 10),
			('dependency_based_collocations_top_2_cz_v1.0', 8),
			('dependency_based_collocations_top_1_cz_v1.0', None), # default to this method if none of the thresholds are met
		),
	},
	'dependency_based_collocations_top_combined_en_v1.0': {
		'class': servers.collocations.SuperHintGenerator,
		'model': tuple(
			('dependency_based_collocations_top_3_en_v1.0', 10),
			('dependency_based_collocations_top_2_en_v1.0', 8),
			('dependency_based_collocations_top_1_en_v1.0', None), # default to this method if none of the thresholds are met
		),
	},
	
	# third test run
	'word2vec_weighted_top_1_cz_v1.0': {
		'class': servers.word2vec.WeightedWord2vecHintGenerator,
		'model': word2vec_embeddings_model_cz,
		'weighting_method': servers.weighting.top_1,
		'weights': (1, 1.2, 1, 2),
	},
	'word2vec_weighted_top_2_cz_v1.0': {
		'class': servers.word2vec.WeightedWord2vecHintGenerator,
		'model': word2vec_embeddings_model_cz,
		'weighting_method': servers.weighting.top_2,
		'weights': (1, 1.2, 1, 2),
	},
	'word2vec_weighted_top_3_cz_v1.0': {
		'class': servers.word2vec.WeightedWord2vecHintGenerator,
		'model': word2vec_embeddings_model_cz,
		'weighting_method': servers.weighting.top_3,
		'weights': (1, 1.2, 1, 2),
	},
	'word2vec_weighted_top_1_en_v1.0': {
		'class': servers.word2vec.WeightedWord2vecHintGenerator,
		'model': word2vec_embeddings_model_en,
		'weighting_method': servers.weighting.top_1,
		'weights': (1, 1.2, 1, 2),
	},
	'word2vec_weighted_top_2_en_v1.0': {
		'class': servers.word2vec.WeightedWord2vecHintGenerator,
		'model': word2vec_embeddings_model_en,
		'weighting_method': servers.weighting.top_2,
		'weights': (1, 1.2, 1, 2),
	},
	'word2vec_weighted_top_3_en_v1.0': {
		'class': servers.word2vec.WeightedWord2vecHintGenerator,
		'model': word2vec_embeddings_model_en,
		'weighting_method': servers.weighting.top_3,
		'weights': (1, 1.2, 1, 2),
	},
	
	# second test run
	'dependency_based_collocations_top_1_cz_v1.0': {
		'class': servers.collocations.DependencyBasedCollocationsHintGenerator,
		'model': dependency_based_collocations_model_cz,
		'frequency_cutoff': 1000,
		'weighting_method': servers.weighting.top_1,
		'weights': (1, 1.2, 1, 2),
	},
	'dependency_based_collocations_top_2_cz_v1.0': {
		'class': servers.collocations.DependencyBasedCollocationsHintGenerator,
		'model': dependency_based_collocations_model_cz,
		'frequency_cutoff': 1000,
		'weighting_method': servers.weighting.top_2,
		'weights': (1, 1.2, 1, 2),
	},
	'dependency_based_collocations_top_3_cz_v1.0': {
		'class': servers.collocations.DependencyBasedCollocationsHintGenerator,
		'model': dependency_based_collocations_model_cz,
		'frequency_cutoff': 1000,
		'weighting_method': servers.weighting.top_3,
		'weights': (1, 1.2, 1, 2),
	},
	'dependency_based_collocations_top_1_en_v1.0': {
		'class': servers.collocations.DependencyBasedCollocationsHintGenerator,
		'model': dependency_based_collocations_model_en,
		'frequency_cutoff': 1000,
		'weighting_method': servers.weighting.top_1,
		'weights': (1, 1.2, 1, 2),
	},
	'dependency_based_collocations_top_2_en_v1.0': {
		'class': servers.collocations.DependencyBasedCollocationsHintGenerator,
		'model': dependency_based_collocations_model_en,
		'frequency_cutoff': 1000,
		'weighting_method': servers.weighting.top_2,
		'weights': (1, 1.2, 1, 2),
	},
	'dependency_based_collocations_top_3_en_v1.0': {
		'class': servers.collocations.DependencyBasedCollocationsHintGenerator,
		'model': dependency_based_collocations_model_en,
		'frequency_cutoff': 1000, # top ~16000
		'weighting_method': servers.weighting.top_3,
		'weights': (1, 1.2, 1, 2),
	},
	
	# first test run
	'word2vec_simple_cz_v1.0': {
		'class': servers.word2vec.Word2vecHintGenerator,
		'model': word2vec_embeddings_model_cz,
	},
	'word2vec_weighted_combined_max_score_cz_v1.0': {
		'class': servers.word2vec.WeightedWord2vecHintGenerator,
		'model': word2vec_embeddings_model_cz,
		'weighting_method': servers.weighting.combined_max_score,
		'weights': (1, 1.2, 1, 2),
	},
	'collocations_combined_max_score_cz_v1.0': {
		'class': servers.collocations.CollocationsHintGenerator,
		'model': collocations_model_cz,
		'frequency_cutoff': 1000,
		'weighting_method': servers.weighting.combined_max_score,
		'weights': (1, 1.2, 1, 2),
	},
	'dependency_based_collocations_mean_difference_cz_v1.0': {
		'class': servers.collocations.DependencyBasedCollocationsHintGenerator,
		'model': dependency_based_collocations_model_cz,
		'frequency_cutoff': 1000,
		'weighting_method': servers.weighting.mean_difference,
		'weights': (1, 1.2, 1, 2),
	},
	'dependency_based_collocations_combined_max_score_cz_v1.0': {
		'class': servers.collocations.DependencyBasedCollocationsHintGenerator,
		'model': dependency_based_collocations_model_cz,
		'frequency_cutoff': 1000,
		'weighting_method': servers.weighting.combined_max_score,
		'weights': (1, 1.2, 1, 2),
	},
	'word2vec_simple_en_v1.0': {
		'class': servers.word2vec.Word2vecHintGenerator,
		'model': word2vec_embeddings_model_en,
	},
	'word2vec_weighted_combined_max_score_en_v1.0': {
		'class': servers.word2vec.WeightedWord2vecHintGenerator,
		'model': word2vec_embeddings_model_en,
		'weighting_method': servers.weighting.combined_max_score,
		'weights': (1, 1.2, 1, 2),
	},
	'collocations_combined_max_score_en_v1.0': {
		'class': servers.collocations.CollocationsHintGenerator,
		'model': collocations_model_en,
		'frequency_cutoff': 1000,
		'weighting_method': servers.weighting.combined_max_score,
		'weights': (1, 1.2, 1, 2),
	},
	'dependency_based_collocations_mean_difference_en_v1.0': {
		'class': servers.collocations.DependencyBasedCollocationsHintGenerator,
		'model': dependency_based_collocations_model_en,
		'frequency_cutoff': 1000,
		'weighting_method': servers.weighting.mean_difference,
		'weights': (1, 1.2, 1, 2),
	},
	'dependency_based_collocations_combined_max_score_en_v1.0': {
		'class': servers.collocations.DependencyBasedCollocationsHintGenerator,
		'model': dependency_based_collocations_model_en,
		'frequency_cutoff': 1000,
		'weighting_method': servers.weighting.combined_max_score,
		'weights': (1, 1.2, 1, 2),
	},
}
