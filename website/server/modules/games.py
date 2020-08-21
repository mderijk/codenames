
import os
import pickle
import random

from codenames import SinglePlayerGame
from . import sessions

__all__ = ['Games']

class Games(sessions.Sessions):
	def getWeightedOptions(self, generator_names, k=10):
		weighted_options = []
		for generator_name in generator_names:
			generator_log_directory = os.path.join(self.config.hints_log_directory, generator_name)
			number_of_games_played = 0
			for _ in os.listdir(generator_log_directory):
				number_of_games_played += 1
			
			if number_of_games_played < k:
				for _ in range(k - number_of_games_played):
					weighted_options.append(generator_name)
		
		if not weighted_options: # if we have enough games for every AI, just choose any random AI
			return generator_names
		
		return weighted_options
	
	def createNewGame(self, session):
		words = []
		word_list_filename = os.path.join(self.config.lexicons_directory, 'original_trimmed_{}.txt'.format(session.language))
		with open(word_list_filename, encoding='utf-8') as f:
			for line in f:
				word = line.strip()
				if word:
					words.append(word)
		
		users = [session.user_id, None]
		generator_names_by_language = self.config.GENERATOR_NAMES_BY_LANGUAGE[session.language]
		weighted_options = self.getWeightedOptions(generator_names_by_language, k=10) # Make sure an equal amount of games get played for all models up to a certain threshold k
		ai_name = random.choice(weighted_options) # Make sure an equal amount of games gets played for all models up to a certain threshold k
#		ai_name = random.choice(generator_names_by_language)
		game = SinglePlayerGame(users, words, games_directory=self.config.games_directory, generator_sockets=self.config.GENERATOR_SOCKETS, ai_name=ai_name)
		return game
	
	def getGame(self, game_file):
		with open(game_file, 'rb') as f:
			game = pickle.load(f)
		
		# tack on the new GENERATOR_SOCKETS (in case the server config was changed during the game)
		game.generator_sockets = self.config.GENERATOR_SOCKETS
		
		return game

	def saveGame(self, game):
		game_file = os.path.join(self.config.games_directory, '{}.pickle'.format(game.id))
		with open(game_file, 'wb') as f:
			pickle.dump(game, f)
		
		return game_file

	def archiveGame(self, game):
		game_file = self.saveGame(game)
		archive_file = os.path.join(self.config.games_archive_directory, '{}.pickle'.format(game.id))
		os.rename(game_file, archive_file)
		
		# archive history as well
		history_file = os.path.join(self.config.games_history_directory, '{}.log'.format(game.id))
		with open(history_file, 'w', encoding='utf-8') as f:
			for event in game.history:
				try:
					print(*event, sep='\t', file=f)
				except TypeError:
					print(event, sep='\t', file=f)
		
		# archive score for the user
		for user_id in game.users:
			if user_id is not None:
				users_team = game.users.index(user_id)
				score = game.getScoreByTeam(users_team)
				
				score_file = os.path.join(self.config.scores_directory, '{}'.format(user_id))
				with open(score_file, 'a', encoding='utf-8') as f:
					users_team = game.users.index(user_id)
					generator_name = game.teams[users_team].spymaster.name
					print(game.id, generator_name, score, sep='\t', file=f)
	
	# overwrite Sessions.getSession because the game requires special handling
	def getSession(self, session_id):
		# get session object
		session = super().getSession(session_id)
		
		# get related game object and hook it up to the session object
		if session.game is not None:
			game_file = os.path.join(self.config.games_directory, '{}.pickle'.format(session.game))
			game = self.getGame(game_file)
			session.game = game
		
		return session
	
	# overwrite Sessions.saveSession because the game object requires special handling
	def saveSession(self, session):
		# save game object to disk separately
		if session.game is not None:
			self.saveGame(session.game)
			
			game = session.game
			session.game = session.game.id
		
		# save session object
		super().saveSession(session)
		
		# reattach game object to the session object
		if session.game is not None:
			session.game = game
