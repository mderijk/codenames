
collocations_model_cz = 'data/collocations/sentence_level_collocations_filtered_cz_v1.0.col'
dependency_based_collocations_model_cz = 'data/collocations/dependency_level_collocations_filtered_cz_v1.0.col'
syntactic_collocations_model_cz = 'data/collocations/syntactic_collocations_filtered_cz_v1.0.col'

collocations_model_en = 'data/collocations/sentence_level_collocations_filtered_en_v1.0.col'
dependency_based_collocations_model_en = 'data/collocations/dependency_level_collocations_filtered_en_v1.0.col'
syntactic_collocations_model_en = 'data/collocations/syntactic_collocations_filtered_en_v1.0.col'

GENERATORS = {
	# Models based on syntactic collocations seem to perform decently. They can sometimes give you a hint for 4 or 5 words and leave you amazed. Other times they don't even give you a good hint for one. It's a bit of both, and when inspecting the PMI values, the dependency ones seem to be more accurate, so we think those models have more of a future.
	'syntactic_collocations_combined_top_3_cz_v1.0': {
		'class': 'collocations.SyntacticCollocationsHintGenerator',
		'model': syntactic_collocations_model_cz,
		'frequency_cutoff': 1000,
		'weighting_method': 'weighting.top_3',
		'weights': (1, 1.2, 1, 2),
	},
	'syntactic_collocations_combined_top_3_en_v1.0': {
		'class': 'collocations.SyntacticCollocationsHintGenerator',
		'model': syntactic_collocations_model_en,
		'frequency_cutoff': 1000,
		'weighting_method': 'weighting.top_3',
		'weights': (1, 1.2, 1, 2),
	},
	
	# fourth test run
	'dependency_based_collocations_top_combined_cz_v1.0': {
		'class': 'collocations.ThresholdDependencyBasedCollocationsHintGenerator',
		'model': dependency_based_collocations_model_cz,
		'frequency_cutoff': 1000,
		'weighting_methods': (
			('weighting.top_3', 3, 9.299208329296569),
			('weighting.top_2', 2, 10.811084816565739),
			('weighting.top_1', 1, None), # default to this method if none of the thresholds are met
		),
		'weights': (1, 1.2, 1, 2),
	},
	'dependency_based_collocations_top_combined_en_v1.0': {
		'class': 'collocations.ThresholdDependencyBasedCollocationsHintGenerator',
		'model': dependency_based_collocations_model_en,
		'frequency_cutoff': 1000,
		'weighting_methods': (
			('weighting.top_3', 3, 6.945942848881148),
			('weighting.top_2', 2, 9.653435486873398),
			('weighting.top_1', 1, None), # default to this method if none of the thresholds are met
		),
		'weights': (1, 1.2, 1, 2),
	},
	
	# second test run
	'dependency_based_collocations_top_1_cz_v1.0': {
		'class': 'collocations.DependencyBasedCollocationsHintGenerator',
		'model': dependency_based_collocations_model_cz,
		'frequency_cutoff': 1000,
		'include_number': True,
		'max_hint_number': 1,
		'weighting_method': 'weighting.top_1',
		'weights': (1, 1.2, 1, 2),
	},
	'dependency_based_collocations_top_2_cz_v1.0': {
		'class': 'collocations.DependencyBasedCollocationsHintGenerator',
		'model': dependency_based_collocations_model_cz,
		'frequency_cutoff': 1000,
		'include_number': True,
		'max_hint_number': 2,
		'weighting_method': 'weighting.top_2',
		'weights': (1, 1.2, 1, 2),
	},
	'dependency_based_collocations_top_3_cz_v1.0': {
		'class': 'collocations.DependencyBasedCollocationsHintGenerator',
		'model': dependency_based_collocations_model_cz,
		'frequency_cutoff': 1000,
		'include_number': True,
		'max_hint_number': 3,
		'weighting_method': 'weighting.top_3',
		'weights': (1, 1.2, 1, 2),
	},
	'dependency_based_collocations_top_1_en_v1.0': {
		'class': 'collocations.DependencyBasedCollocationsHintGenerator',
		'model': dependency_based_collocations_model_en,
		'frequency_cutoff': 1000,
		'include_number': True,
		'max_hint_number': 1,
		'weighting_method': 'weighting.top_1',
		'weights': (1, 1.2, 1, 2),
	},
	'dependency_based_collocations_top_2_en_v1.0': {
		'class': 'collocations.DependencyBasedCollocationsHintGenerator',
		'model': dependency_based_collocations_model_en,
		'frequency_cutoff': 1000,
		'include_number': True,
		'max_hint_number': 2,
		'weighting_method': 'weighting.top_2',
		'weights': (1, 1.2, 1, 2),
	},
	'dependency_based_collocations_top_3_en_v1.0': {
		'class': 'collocations.DependencyBasedCollocationsHintGenerator',
		'model': dependency_based_collocations_model_en,
		'frequency_cutoff': 1000, # top ~16000
		'include_number': True,
		'max_hint_number': 3,
		'weighting_method': 'weighting.top_3',
		'weights': (1, 1.2, 1, 2),
	},
	
	# first test run
	'collocations_combined_max_score_cz_v1.0': {
		'class': 'collocations.CollocationsHintGenerator',
		'model': collocations_model_cz,
		'frequency_cutoff': 1000,
		'include_number': False,
		'weighting_method': 'weighting.combined_max_score',
		'weights': (1, 1.2, 1, 2),
	},
	'dependency_based_collocations_mean_difference_cz_v1.0': {
		'class': 'collocations.DependencyBasedCollocationsHintGenerator',
		'model': dependency_based_collocations_model_cz,
		'frequency_cutoff': 1000,
		'include_number': False,
		'weighting_method': 'weighting.mean_difference',
		'weights': (1, 1.2, 1, 2),
	},
	'dependency_based_collocations_combined_max_score_cz_v1.0': {
		'class': 'collocations.DependencyBasedCollocationsHintGenerator',
		'model': dependency_based_collocations_model_cz,
		'frequency_cutoff': 1000,
		'include_number': False,
		'weighting_method': 'weighting.combined_max_score',
		'weights': (1, 1.2, 1, 2),
	},
	'collocations_combined_max_score_en_v1.0': {
		'class': 'collocations.CollocationsHintGenerator',
		'model': collocations_model_en,
		'frequency_cutoff': 1000,
		'include_number': False,
		'weighting_method': 'weighting.combined_max_score',
		'weights': (1, 1.2, 1, 2),
	},
	'dependency_based_collocations_mean_difference_en_v1.0': {
		'class': 'collocations.DependencyBasedCollocationsHintGenerator',
		'model': dependency_based_collocations_model_en,
		'frequency_cutoff': 1000,
		'include_number': False,
		'weighting_method': 'weighting.mean_difference',
		'weights': (1, 1.2, 1, 2),
	},
	'dependency_based_collocations_combined_max_score_en_v1.0': {
		'class': 'collocations.DependencyBasedCollocationsHintGenerator',
		'model': dependency_based_collocations_model_en,
		'frequency_cutoff': 1000,
		'include_number': False,
		'weighting_method': 'weighting.combined_max_score',
		'weights': (1, 1.2, 1, 2),
	},
}
