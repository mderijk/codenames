
import datetime
import os
import sys

import modules
from start_servers import launchPythonProcess, pollServers

class Application(modules.Games, modules.HallOfFame):
	def route(self, request):
		# make sure all the relevant data directories exist
		os.makedirs(self.config.games_archive_directory, exist_ok=True)
		os.makedirs(self.config.games_history_directory, exist_ok=True)
		os.makedirs(self.config.scores_directory, exist_ok=True)
		os.makedirs(self.config.sessions_directory, exist_ok=True)
		os.makedirs(self.config.users_directory, exist_ok=True)
		
		# perform basic authentication checks
		if not self._require(request, 'action'):
			response = self.missing('action')
		elif request['action'] == 'new_session':
			# make sure username and language contain valid information
			if not self._require(request, 'username'):
				response = self.missing('username')
				return response
			
			if not self._require(request, 'language'):
				response = self.missing('language')
				return response
			
			if request['language'] not in self.config.LANGUAGES:
				self.error('Invalid \'language\'')
				return response
			
			username = request['username']
			
			# restrict usernames to alphabetical characters, numbers and underscores
			if any(map(lambda char: not (char.isalnum() or char == '_'), username)):
				response = {
					'status': 'invalid',
					'invalid': 'username',
				}
				return response
			
			# perform lowercasing so Admin and admin aren't two completely different users
			username = username.lower()
			
			if self.config.autostart:
				# launch hint servers (if they weren't online already)
				process = launchPythonProcess('start_servers.py')
				process.wait() # wait until all servers have been launched
			
			# create a new session and return the session id
			session = self.createSession(username, request['language'])
			
			response = {
				'status': 'success',
				'session_id': session.id,
			}
		elif not self._require(request, 'session_id'):
			response = self.missing('session_id')
		else:
			last_seen = datetime.datetime.now() # get a timestamp BEFORE the servers are polled and refreshed, so that we can guarantee that the server timeouts always happen after the user session times out
			session = self.getSession(request['session_id'])
			if not session:
				response = self.error('Invalid \'session_id\'')
				return response
			
			# check if the session has timed out
			if self.config.session_timeout and session.last_seen + datetime.timedelta(seconds=self.config.session_timeout) < datetime.datetime.now():
				response = self.error('Session timed out')
				return response
			
			# poll the hint servers to see if they are up and runnning and refresh their internal server timeouts in the process
			status, message = pollServers(self.config.SERVERS.keys())
			if not status:
				response = self.error('Hint servers could not be reached. (Internal Server Error)')
				print('Hint server could not be reached:', message, file=sys.stderr)
				return response
			
			# handle request
			response = self.handleRequest(request, session)
			
			# update last seen date
			session.last_seen = last_seen
			
			# save session
			self.saveSession(session)
		
		return response
	
	def handleRequest(self, request, session):
		if session.game is not None:
			response = self.handleGameRequest(request, session)
			if response:
				return response
		
		response = self.error('Unsupported action')
		
		if request['action'] == 'new_game':
			if session.game is not None:
				response = self.error('You are already in a game')
				return response
			
			# create new game
			game = self.createNewGame(session)
			session.game = game
			
			# return the board state of the new game
			response = self.getBoard(session)
		elif request['action'] == 'change_settings':
			if session.game is not None:
				response = self.error('You cannot change your settings while in game')
				return response
			
			if not self._require(request, 'language'):
				response = self.missing('language')
				return response
			
			if request['language'] not in self.config.LANGUAGES:
				response = self.error('Invalid \'language\'')
				return response
			
			session.language = request['language']
			response = {
				'status': 'success',
			}
		elif request['action'] == 'get_hall_of_fame':
			hall_of_fame = self.assembleHallOfFame()
			
			# convert generator_names to their current AI names with language in brackets
			# convert the whole thing to a list to make it JSON friendly
			hall_of_fame = [
				(self.config.AI_NAMES[generator_name] + ' ({})'.format(self.getLanguageFromGeneratorName(generator_name)), scores)
				for generator_name, scores in hall_of_fame.items()
			]
			hall_of_fame.sort()
			
			response = {
				'status': 'success',
				'hall_of_fame': hall_of_fame,
			}
		
		return response
	
	def handleGameRequest(self, request, session):
		response = None
		
		if session.game.ended:
			response = self.error('Game has already ended')
			return response
		
		if request['action'] == 'get_board':
			response = self.getBoard(session)
		elif request['action'] == 'flip':
			if not self._require(request, 'card_id'):
				response = self.missing('card_id')
				return response
			
			# check if card_id is a valid card id
			try:
				card = session.game.cards[request['card_id']]
			except IndexError:
				response = self.error('Invalid \'card_id\''),
				return response
			
			if card.flipped:
				response = self.error('Card already flipped'),
				return response
			
			turn_ended = session.game.flipCard(card)
			response = {
				'status': 'success',
				'card': {
					'id': card.id,
					'type': card.type,
				},
			}
			
			self.endTurn(session, response, turn_ended)
		elif False and request['action'] == 'turn_info': # not used
			enemy_turn = self.getEnemyTurnInfo(session, False)
			response = {
				'status': 'success',
				'enemy_turn': enemy_turn,
			}
		elif request['action'] == 'end_turn':
			# end the user's turn
			session.game.endTurn()
			
			response = {
				'status': 'success',
			}
			
			self.endTurn(session, response, True)
		
		return response
	
	def getEnemyTurnInfo(self, session, turn_ended):
		users_team = session.game.users.index(session.user_id)
		if session.game.ended and turn_ended and session.game.initiative == users_team: # If there was no enemy turn, return None
			return None
		
		enemy_turn = {key: item for key, item in session.game.last_enemy_turn.items()}
		enemy_turn['flipped'] = [
			{
				'id': card.id,
				'type': card.type,
			}
			for card in enemy_turn['flipped']
		]
		
		return enemy_turn
	
	def getBoard(self, session):
		users_team = session.game.users.index(session.user_id)
		response = {
			'status': 'success',
			'ai': self.config.AI_NAMES[session.game.teams[users_team].spymaster.name],
			'board': {
				'cards': [],
			},
			'hints': [(hint, len(target_words)) for hint, target_words in session.game.hints[users_team]],
			'score': session.game.getScoreByTeam(users_team),
			'cards_left': session.game.getCardsLeftByTeam(users_team),
			'turn': session.game.turn,
		}
		for card in session.game.cards:
			card_dict = {
				'id': card.id,
				'word': card.word,
				'flipped': card.flipped,
			}
			if card_dict['flipped']:
				card_dict['type'] = card.type
			response['board']['cards'].append(card_dict)
		
		return response
	
	def endTurn(self, session, response, turn_ended):
		if turn_ended:
			if not session.game.ended:
				hint, target_words = session.game.hint
				response['hint'] = (hint, len(target_words)) # the new hint that was generated
			
			# info about the enemy's turn
			enemy_turn = self.getEnemyTurnInfo(session, turn_ended)
			response['enemy_turn'] = enemy_turn
		
		users_team = session.game.users.index(session.user_id)
		response['score'] = session.game.getScoreByTeam(users_team)
		response['cards_left'] = session.game.getCardsLeftByTeam(users_team)
		response['turn'] = session.game.turn
		if session.game.ended:
			# return all the cards that were not flipped over
			response['cards'] = []
			for card in session.game.cards:
				if not card.flipped:
					card_dict = {
						'id': card.id,
						'type': card.type,
					}
					response['cards'].append(card_dict)
			
			# return the winner of the game
			response['winner'] = session.game.winner
			
			# return all the hints along with the words that each hint targeted
			hints = []
			for hint, target_words in session.game.hints[users_team]:
				# convert target words to card dictionaries
				target_words_with_card_dicts = []
				for word, score in target_words:
					card = session.game.getCardByWord(word)
					target_card_dict = {
						'id': card.id,
						'type': card.type,
						'flipped': card.flipped,
					}
					target_words_with_card_dicts.append((target_card_dict, score))
				
				hints.append((hint, target_words_with_card_dicts))
			response['hints'] = hints
			
			# disassociate game from session
			game = session.game
			session.game = None
			
			# archive game
			self.archiveGame(game)
	
	def getLanguageFromGeneratorName(self, generator_name):
		for language in self.config.LANGUAGES:
			if '_{}_'.format(language) in generator_name:
				return language	
