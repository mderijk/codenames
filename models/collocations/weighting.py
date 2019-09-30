
import math

# example weighting method
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
