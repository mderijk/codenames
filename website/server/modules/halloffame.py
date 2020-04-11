
import os

from . import module

__all__ = ['HallOfFame']

class HallOfFame(module.Module):
	def assembleHallOfFame(self, top_n=10):
		# open users/users.txt and create a map from user_id => username
		# load file of users
		users_file = os.path.join(self.config.users_directory, 'users.txt')
		users = {}
		if os.path.isfile(users_file):
			with open(users_file, encoding='utf-8') as f:
				for line in f:
					line = line.rstrip('\n')
					user_id, user_username = line.split('\t', 1)
					users[user_id] = user_username
		
		scores_by_ai = {generator_name: [] for generator_name in self.config.GENERATOR_NAMES}
		
		# open everything in scores/{user_id}
		scores_dir = self.config.scores_directory
		for root, dirs, files in os.walk(scores_dir):
			for filename in files:
				user_id = filename
				score_file = os.path.join(root, user_id)
				if user_id in users: # make sure we have a username for this user
					username = users[user_id]
					with open(score_file, encoding='utf-8') as f:
						for line in f:
							line = line.strip()
							game_id, generator_name, score = line.split('\t')
							score = int(score)
							
							if generator_name in scores_by_ai:
								# add combination of username, score to the scores list
								scores_by_ai[generator_name].append((score, username))
		
		# take the top_n scores for each list of scores
		hall_of_fame = {
			generator_name: list(sorted(sorted(scores, key=lambda x: x[1]), reverse=True, key=lambda x: x[0]))[:top_n]
			for generator_name, scores in scores_by_ai.items()
		}
		
		return hall_of_fame
