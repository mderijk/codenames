
import math

import numpy as np

# for_all takes a weighting_method and generates a function that applies that weighting method to all hint scores passed to it, instead of just one hint (used by word2vec models)
def for_all(weighting_method):
	def calculate_weights(*word_dists, **kwargs):
		""" Calculates weights for all hints using <weighting_method>. """
		original_lengths = list(map(len, word_dists))
		word_dists = list(map(np.transpose, word_dists))
		word_dists = np.concatenate(word_dists, axis=1)
		l1, l2, l3, l4 = sum(original_lengths[:1]), sum(original_lengths[:2]), sum(original_lengths[:3]), sum(original_lengths[:4])
		weighted_scores = np.array(list(map(lambda args: weighting_method(args[:l1], args[l1:l2], args[l2:l3], args[l3:l4], **kwargs), word_dists))) # map weighting_method over all hints
		return weighted_scores
	
	return calculate_weights

def weighted_average(*word_dists, weights=(1, -1, -0.5, -2)):
	word_dists_flat = [(dists, weight) for group, weight in zip(word_dists, weights) for dists in group]
	dists_sum = word_dists_flat[0][0] * word_dists_flat[0][1]
	for dists, weight in word_dists_flat[1:]:
		dists *= weight
		dists_sum = dists_sum + dists
	combined_dists = dists_sum / len(word_dists)
	return combined_dists

def max_score(own_team_scores, enemy_team_scores, neutral_scores, assassin_scores, weights=(1, 1, 1, 1)):
	own_team_scores, enemy_team_scores, neutral_scores, assassin_scores = \
			(map(lambda x: x * weight, scores) for weight, scores in zip(weights, [own_team_scores, enemy_team_scores, neutral_scores, assassin_scores]))
	own_team_max = max(own_team_scores)
	enemy_team_max = max(enemy_team_scores)
	neutral_max = max(neutral_scores)
	assassin_max = max(assassin_scores)
	
	# return the max score if it belongs to own team
	if own_team_max > enemy_team_max and own_team_max > neutral_max and own_team_max > assassin_max:
		return own_team_max
	
	# otherwise return a negative score, which is the negation of the most positive score
	return -max(enemy_team_max, neutral_max, assassin_max)

def combined_max_score(own_team_scores, enemy_team_scores, neutral_scores, assassin_scores, weights=(1, 1, 1, 1)):
	own_team_scores, enemy_team_scores, neutral_scores, assassin_scores = \
			(list(map(lambda x: x * weight, scores)) for weight, scores in zip(weights, [own_team_scores, enemy_team_scores, neutral_scores, assassin_scores]))
	own_team_scores = [(0, score) for score in own_team_scores]
	enemy_team_scores = [(1, score) for score in enemy_team_scores]
	neutral_scores = [(2, score) for score in neutral_scores]
	assassin_scores = [(3, score) for score in assassin_scores]
	scores = own_team_scores + enemy_team_scores + neutral_scores + assassin_scores
	
	# rank the list by score
	scores.sort(key=lambda x: x[1], reverse=True)
	
	# add each score at the top of the list to the combined score, until we see a high score that does not belong to a word in own team
	combined_max_score = 0
	for group_index, score in scores:
		if group_index != 0:
			break
		
		combined_max_score += score
	
	return combined_max_score

def top_n(own_team_scores, enemy_team_scores, neutral_scores, assassin_scores, n=1, weights=(1, 1, 1, 1)):
	own_team_scores, enemy_team_scores, neutral_scores, assassin_scores = \
			(list(map(lambda x: x * weight, scores)) for weight, scores in zip(weights, [own_team_scores, enemy_team_scores, neutral_scores, assassin_scores]))
	
	# find highest negative scoring word
	threshold = max(enemy_team_scores + neutral_scores + assassin_scores)
	
	# rank the list by score (descendingly)
	own_team_scores.sort(reverse=True)
	
	# sum the top-n highest scoring own words that are equal to or above the threshold
	combined_max_score = 0
	for score in own_team_scores[:n]:
		if score >= threshold:
			combined_max_score += score
	
	return combined_max_score

def top_1(own_team_scores, enemy_team_scores, neutral_scores, assassin_scores, weights=(1, 1, 1, 1)):
	return top_n(own_team_scores, enemy_team_scores, neutral_scores, assassin_scores, n=1, weights=weights)

def top_2(own_team_scores, enemy_team_scores, neutral_scores, assassin_scores, weights=(1, 1, 1, 1)):
	return top_n(own_team_scores, enemy_team_scores, neutral_scores, assassin_scores, n=2, weights=weights)

def top_3(own_team_scores, enemy_team_scores, neutral_scores, assassin_scores, weights=(1, 1, 1, 1)):
	return top_n(own_team_scores, enemy_team_scores, neutral_scores, assassin_scores, n=3, weights=weights)

def t_score(own_team_scores, enemy_team_scores, neutral_scores, assassin_scores, weights=(1, 1, 1, 1)):
	"""
	Performs an independent two-sample t-test on own_team_scores and the combination of enemy_team_scores, neutral_scores and assassin_scores.
	The formula used accounts for the fact that the sample sizes of the two samples can be unequal.
	Equal variance in both samples is assumed, because they are pointwise mutual information scores from the same data set.
	"""
	good_scores = [score * weights[0] for score in own_team_scores]
	bad_scores = [score * weights[1] for score in enemy_team_scores] + [score * weights[2] for score in neutral_scores] + [score * weights[3] for score in assassin_scores]
	
	mean_good_scores = sum(good_scores) / len(good_scores)
	mean_bad_scores = sum(bad_scores) / len(bad_scores)
	
	# in case good_scores and bad_scores don't contain at least 2 elements, we cannot perform a t-test, so we take the mean difference instead
	if len(good_scores) < 2 or len(bad_scores) < 2:
		return mean_good_scores - mean_bad_scores
	
	unbiased_estimator_of_variance_good_scores = (1 / (len(good_scores) - 1)) * sum((score - mean_good_scores) ** 2 for score in good_scores)
	unbiased_estimator_of_variance_bad_scores = (1 / (len(bad_scores) - 1)) * sum((score - mean_bad_scores) ** 2 for score in bad_scores)
	pooled_standard_deviation = math.sqrt(
			((len(good_scores) - 1) * unbiased_estimator_of_variance_good_scores
			+ (len(bad_scores) - 1) * unbiased_estimator_of_variance_bad_scores)
		/
			(len(good_scores) + len(bad_scores) - 2)
	)
	
	# if there is no standard deviation in either of the samples, we take the mean difference instead (although it is unlikely that this will be a high score at this point)
	if pooled_standard_deviation == 0:
		return mean_good_scores - mean_bad_scores
	
	t_score = (mean_good_scores - mean_bad_scores) / (pooled_standard_deviation * math.sqrt((1 / len(good_scores)) + (1 / len(bad_scores))))
	
	return t_score

def non_zero_t_score(own_team_scores, enemy_team_scores, neutral_scores, assassin_scores, weights=(1, 1, 1, 1)):
	"""
	Performs an independent two-sample t-test on own_team_scores and the combination of enemy_team_scores, neutral_scores and assassin_scores.
	The formula used accounts for the fact that the sample sizes of the two samples can be unequal.
	Equal variance in both samples is assumed, because they are pointwise mutual information scores from the same data set.
	"""
	good_scores = [score * weights[0] for score in own_team_scores if score * weights[0] != 0]
	bad_scores = [score for score in [score * weights[1] for score in enemy_team_scores] + [score * weights[2] for score in neutral_scores] + [score * weights[3] for score in assassin_scores] if score != 0]
	
	if len(good_scores) < 1 or len(bad_scores) < 1:
		return 0
	
	mean_good_scores = sum(good_scores) / len(good_scores)
	mean_bad_scores = sum(bad_scores) / len(bad_scores)
	
	# in case good_scores and bad_scores don't contain at least 2 elements, we cannot perform a t-test, so we take the mean difference instead
	if len(good_scores) < 2 or len(bad_scores) < 2:
		return mean_good_scores - mean_bad_scores
	
	unbiased_estimator_of_variance_good_scores = (1 / (len(good_scores) - 1)) * sum((score - mean_good_scores) ** 2 for score in good_scores)
	unbiased_estimator_of_variance_bad_scores = (1 / (len(bad_scores) - 1)) * sum((score - mean_bad_scores) ** 2 for score in bad_scores)
	pooled_standard_deviation = math.sqrt(
			((len(good_scores) - 1) * unbiased_estimator_of_variance_good_scores
			+ (len(bad_scores) - 1) * unbiased_estimator_of_variance_bad_scores)
		/
			(len(good_scores) + len(bad_scores) - 2)
	)
	
	# if there is no standard deviation in either of the samples, we take the mean difference instead (although it is unlikely that this will be a high score at this point)
	if pooled_standard_deviation == 0:
		return mean_good_scores - mean_bad_scores
	
	t_score = (mean_good_scores - mean_bad_scores) / (pooled_standard_deviation * math.sqrt((1 / len(good_scores)) + (1 / len(bad_scores))))
	
	return t_score

def mean_difference(own_team_scores, enemy_team_scores, neutral_scores, assassin_scores, weights=(1, 1, 1, 1)):
	""" Calculates the difference between the mean of own_team_scores and the mean of the combination of enemy_team_scores, neutral_scores and assassin_scores. """
	own_team_scores, enemy_team_scores, neutral_scores, assassin_scores = \
			(list(map(lambda x: x * weight, scores)) for weight, scores in zip(weights, [own_team_scores, enemy_team_scores, neutral_scores, assassin_scores]))
	good_scores = own_team_scores
	bad_scores = enemy_team_scores + neutral_scores + assassin_scores # FUTURE: it's possible to weight these beforehand, either by dividing by or multiplying by certain weights. (i.e. weight >1 or <1 makes a big difference)
	
	mean_good_scores = sum(good_scores) / len(good_scores)
	mean_bad_scores = sum(bad_scores) / len(bad_scores)
	mean_difference = mean_good_scores - mean_bad_scores
	
	return mean_difference

def non_zero_mean_difference(own_team_scores, enemy_team_scores, neutral_scores, assassin_scores, weights=(1, 1, 1, 1)):
	""" Calculates the difference between the mean of own_team_scores and the mean of the combination of enemy_team_scores, neutral_scores and assassin_scores. """
	own_team_scores, enemy_team_scores, neutral_scores, assassin_scores = \
			(list(map(lambda x: x * weight, scores)) for weight, scores in zip(weights, [own_team_scores, enemy_team_scores, neutral_scores, assassin_scores]))
	good_scores = [score for score in own_team_scores if score != 0]
	bad_scores = [score for score in enemy_team_scores + neutral_scores + assassin_scores if score != 0] # FUTURE: it's possible to weight these beforehand, either by dividing by or multiplying by certain weights. (i.e. weight >1 or <1 makes a big difference)
	
	mean_good_scores = sum(good_scores) / len(good_scores) if len(good_scores) > 0 else 0
	mean_bad_scores = sum(bad_scores) / len(bad_scores) if len(bad_scores) > 0 else 0
	mean_difference = mean_good_scores - mean_bad_scores
	
	return mean_difference
