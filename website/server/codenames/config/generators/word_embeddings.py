
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
	# sixth test run
	'word2vec_weighted_top_1_cz_v1.1': {
		'class': 'word2vec.WeightedWord2vecHintGenerator',
		'model': word2vec_embeddings_model_cz,
		'include_number': True,
		'max_hint_number': 1,
		'weighting_method': 'weighting.top_1',
		'weights': (1, 1.2, 1, 2),
	},
	'word2vec_weighted_top_2_cz_v1.1': {
		'class': 'word2vec.WeightedWord2vecHintGenerator',
		'model': word2vec_embeddings_model_cz,
		'include_number': True,
		'max_hint_number': 2,
		'weighting_method': 'weighting.top_2',
		'weights': (1, 1.2, 1, 2),
	},
	'word2vec_weighted_top_3_cz_v1.1': {
		'class': 'word2vec.WeightedWord2vecHintGenerator',
		'model': word2vec_embeddings_model_cz,
		'include_number': True,
		'max_hint_number': 3,
		'weighting_method': 'weighting.top_3',
		'weights': (1, 1.2, 1, 2),
	},
	'word2vec_weighted_top_combined_cz_v1.1': {
		'class': 'word2vec.ThresholdWeightedWord2vecHintGenerator',
		'model': word2vec_embeddings_model_cz,
		'weighting_methods': (
			('weighting.top_3', 3, 0.28209114),
			('weighting.top_2', 2, 0.38748214),
			('weighting.top_1', 1, None), # default to this method if none of the thresholds are met
		),
		'weights': (1, 1.2, 1, 2),
	},
	
	# fourth test run
	'word2vec_weighted_top_combined_cz_v1.0': {
		'class': 'word2vec.ThresholdWeightedWord2vecHintGenerator',
		'model': word2vec_embeddings_model_cz,
		'weighting_methods': (
			('weighting.top_3', 3, 0.28209114),
			('weighting.top_2', 2, 0.38748214),
			('weighting.top_1', 1, None), # default to this method if none of the thresholds are met
		),
		'weights': (1, 1.2, 1, 2),
	},
	'word2vec_weighted_top_combined_en_v1.0': {
		'class': 'word2vec.ThresholdWeightedWord2vecHintGenerator',
		'model': word2vec_embeddings_model_en,
		'weighting_methods': (
			('weighting.top_3', 3, 0.34984735),
			('weighting.top_2', 2, 0.37125748),
			('weighting.top_1', 1, None), # default to this method if none of the thresholds are met
		),
		'weights': (1, 1.2, 1, 2),
	},
	
	# third test run
	'word2vec_weighted_top_1_cz_v1.0': {
		'class': 'word2vec.WeightedWord2vecHintGenerator',
		'model': word2vec_embeddings_model_cz,
		'include_number': False,
		'max_hint_number': 1,
		'weighting_method': 'weighting.top_1',
		'weights': (1, 1.2, 1, 2),
	},
	'word2vec_weighted_top_2_cz_v1.0': {
		'class': 'word2vec.WeightedWord2vecHintGenerator',
		'model': word2vec_embeddings_model_cz,
		'include_number': False,
		'max_hint_number': 2,
		'weighting_method': 'weighting.top_2',
		'weights': (1, 1.2, 1, 2),
	},
	'word2vec_weighted_top_3_cz_v1.0': {
		'class': 'word2vec.WeightedWord2vecHintGenerator',
		'model': word2vec_embeddings_model_cz,
		'include_number': False,
		'max_hint_number': 3,
		'weighting_method': 'weighting.top_3',
		'weights': (1, 1.2, 1, 2),
	},
	'word2vec_weighted_top_1_en_v1.0': {
		'class': 'word2vec.WeightedWord2vecHintGenerator',
		'model': word2vec_embeddings_model_en,
		'include_number': True,
		'max_hint_number': 1,
		'weighting_method': 'weighting.top_1',
		'weights': (1, 1.2, 1, 2),
	},
	'word2vec_weighted_top_2_en_v1.0': {
		'class': 'word2vec.WeightedWord2vecHintGenerator',
		'model': word2vec_embeddings_model_en,
		'include_number': True,
		'max_hint_number': 2,
		'weighting_method': 'weighting.top_2',
		'weights': (1, 1.2, 1, 2),
	},
	'word2vec_weighted_top_3_en_v1.0': {
		'class': 'word2vec.WeightedWord2vecHintGenerator',
		'model': word2vec_embeddings_model_en,
		'include_number': True,
		'max_hint_number': 3,
		'weighting_method': 'weighting.top_3',
		'weights': (1, 1.2, 1, 2),
	},
	
	# first test run
	'word2vec_simple_cz_v1.0': {
		'class': 'word2vec.Word2vecHintGenerator',
		'model': word2vec_embeddings_model_cz,
	},
	'word2vec_weighted_combined_max_score_cz_v1.0': {
		'class': 'word2vec.WeightedWord2vecHintGenerator',
		'model': word2vec_embeddings_model_cz,
		'include_number': False,
		'weighting_method': 'weighting.combined_max_score',
		'weights': (1, 1.2, 1, 2),
	},
	'word2vec_simple_en_v1.0': {
		'class': 'word2vec.Word2vecHintGenerator',
		'model': word2vec_embeddings_model_en,
	},
	'word2vec_weighted_combined_max_score_en_v1.0': {
		'class': 'word2vec.WeightedWord2vecHintGenerator',
		'model': word2vec_embeddings_model_en,
		'include_number': False,
		'weighting_method': 'weighting.combined_max_score',
		'weights': (1, 1.2, 1, 2),
	},
}
