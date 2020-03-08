
import contextlib
import io
import json
import os
import pickle
import random
import sys
import uuid

import codenames
import codenames.config as config

class Session:
	def __init__(self, user_id, username, language, game=None):
		self.id = self._generateId()
		self.user_id = user_id
		self.username = username
		self.language = language
		self.game = game
	
	def _generateId(self):
		# create session id and make sure it doesn't exist yet
		while True:
			id = str(uuid.uuid4())
			game_file = os.path.join(config.sessions_directory, '{}.pickle'.format(id))
			
			if not os.path.isfile(game_file):
				break
		
		return id

class User:
	@classmethod
	def _generateId(cls):
		# create user id and make sure it doesn't exist yet
		while True:
			id = str(uuid.uuid4())
			user_file = os.path.join(config.users_directory, '{}'.format(id))
			
			if not os.path.isfile(user_file):
				break
		
		return id


def getWeightedOptions(generator_names, k=10):
	weighted_options = []
	for generator_name in generator_names:
		generator_log_directory = os.path.join(config.hints_log_directory, generator_name)
		number_of_games_played = 0
		for _ in os.listdir(generator_log_directory):
			number_of_games_played += 1
		
		if number_of_games_played < k:
			for _ in range(k - number_of_games_played):
				weighted_options.append(generator_name)
	
	if not weighted_options: # if we have enough games for every AI, just choose any random AI
		return generator_names
	
	return weighted_options

def createNewGame(session):
	words = []
	word_list_filename = os.path.join(config.lexicons_directory, 'original_trimmed_{}.txt'.format(session.language))
	with open(word_list_filename, encoding='utf-8') as f:
		for line in f:
			word = line.strip()
			if word:
				words.append(word)
	
	users = [session.user_id, None]
	generator_names_by_language = config.GENERATOR_NAMES_BY_LANGUAGE[session.language]
	weighted_options = getWeightedOptions(generator_names_by_language, k=10) # Make sure an equal amount of games gets played for all models up to a certain threshold k
	ai_name = random.choice(weighted_options) # Make sure an equal amount of games gets played for all models up to a certain threshold k
#	ai_name = random.choice(generator_names_by_language)
	game = codenames.SinglePlayerGame(users, words, ai_name=ai_name)
	return game

def getGame(game_file):
	with open(game_file, 'rb') as f:
		game = pickle.load(f)
	
	return game

def saveGame(game):
	game_file = os.path.join(config.games_directory, '{}.pickle'.format(game.id))
	with open(game_file, 'wb') as f:
		pickle.dump(game, f)
	
	return game_file

def archiveGame(game):
	game_file = saveGame(game)
	archive_file = os.path.join(config.games_archive_directory, '{}.pickle'.format(game.id))
	os.rename(game_file, archive_file)
	
	# archive history as well
	history_file = os.path.join(config.games_history_directory, '{}.log'.format(game.id))
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
			
			score_file = os.path.join(config.scores_directory, '{}'.format(user_id))
			with open(score_file, 'a', encoding='utf-8') as f:
				users_team = game.users.index(user_id)
				generator_name = game.teams[users_team].spymaster.name
				print(game.id, generator_name, score, sep='\t', file=f)

def getBoard(request, session):
	users_team = session.game.users.index(session.user_id)
	response = {
		'status': 'success',
		'ai': config.AI_NAMES[session.game.teams[users_team].spymaster.name],
		'board': {
			'cards': [],
		},
		'hints': session.game.hints[users_team],
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

def getEnemyTurnInfo(request, session, turn_ended):
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

def endTurn(request, session, response, turn_ended):
	if turn_ended:
		if not session.game.ended:
			response['hint'] = session.game.hint # the new hint that was generated
		
		# info about the enemy's turn
		enemy_turn = getEnemyTurnInfo(request, session, turn_ended)
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
		
		# disassociate game from session
		game = session.game
		session.game = None
		
		# archive game
		archiveGame(game)

def handleGameRequest(request, session):
	response = None
	
	if request['action'] == 'get_board':
		if session.game.ended:
			response = {
				'status': 'error',
				'error': 'Game has already ended',
			}
			return response
		
		response = getBoard(request, session)
	elif request['action'] == 'flip':
		card = session.game.cards[request['card_id']] # NOT SAFE: card_id is not guaranteed to be there
		
		if session.game.ended:
			response = {
				'status': 'error',
				'error': 'Game has already ended',
			}
			return response
		
		if card.flipped:
			response = {
				'status': 'error',
				'error': 'Card already flipped',
			}
			return response
		
		turn_ended = session.game.flipCard(card)
		response = {
			'status': 'success',
			'card': {
				'id': card.id,
				'type': card.type,
			},
		}
		
		endTurn(request, session, response, turn_ended)
	elif False and request['action'] == 'turn_info': # not used
		if session.game.ended:
			response = {
				'status': 'error',
				'error': 'Game has already ended',
			}
			return response
		
		enemy_turn = getEnemyTurnInfo(request, session, False)
		response = {
			'status': 'success',
			'enemy_turn': enemy_turn,
		}
	elif request['action'] == 'end_turn':
		if session.game.ended:
			response = {
				'status': 'error',
				'error': 'Game has already ended',
			}
			return response
		
		# end the user's turn
		session.game.endTurn()
		
		response = {
			'status': 'success',
		}
		
		endTurn(request, session, response, True)
	
	return response

def assembleHallOfFame(top_n=10):
	# open users/users.txt and create a map from user_id => username
	# load file of users
	users_file = os.path.join(config.users_directory, 'users.txt')
	users = {}
	if os.path.isfile(users_file):
		with open(users_file, encoding='utf-8') as f:
			for line in f:
				line = line.rstrip('\n')
				user_id, user_username = line.split('\t', 1)
				users[user_id] = user_username
	
	scores_by_ai = {generator_name: [] for generator_name in config.GENERATOR_NAMES}
	
	# open everything in scores/{user_id}
	scores_dir = config.scores_directory
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
							# add combo of username, score to the scores list
							scores_by_ai[generator_name].append((score, username))
	
	# take the top_n scores for each list of scores
	hall_of_fame = {generator_name: list(sorted(sorted(scores, key=lambda x: x[1]), reverse=True, key=lambda x: x[0]))[:top_n] for generator_name, scores in scores_by_ai.items()}
	
	return hall_of_fame

def getLanguageFromGeneratorName(generator_name):
	for language in config.LANGUAGES:
		if '_{}_'.format(language) in generator_name:
			return language

def handleRequest(request, session):
	if session.game is not None: # TODO: this handles things correctly, except for the fact that it tells you: unsupported action, if you try to do an action that can only be done while in game. The error message for an action that does not exist and one that doesn't make sense in the current context, mhm, should preferably be different. -> If you do manage to produce a different error message, would you be so kind as to handle this error message in the Javascript as well? Then you can just set session.in_game to false and reload the page and everybody will be happy. 
		response = handleGameRequest(request, session)
		if response:
			return response
	
	response = {'status': 'error', 'error': 'Unsupported action'}
	
	if request['action'] == 'new_game':
		if session.game is not None:
			response = {
				'status': 'error',
				'error': 'You are already in a game',
			}
			return response
		
		# create new game
		game = createNewGame(session)
		session.game = game
		
		# return the board state of the new game
		response = getBoard(request, session)
	elif request['action'] == 'change_settings':
		if session.game is not None:
			response = {
				'status': 'error',
				'error': 'You cannot change your settings while in a game',
			}
			return response
		
		if 'language' not in request or request['language'] not in config.LANGUAGES:
			response = {
				'status': 'error',
				'error': 'Invalid or missing language',
			}
			return response
		
		session.language = request['language']
		response = {
			'status': 'success',
		}
	elif request['action'] == 'get_hall_of_fame':
		hall_of_fame = assembleHallOfFame()
		
		# convert generator_names to their current AI names with language in brackets
		# convert the whole thing to a list to make it JSON friendly
		hall_of_fame = [(config.AI_NAMES[generator_name] + ' ({})'.format(getLanguageFromGeneratorName(generator_name)), scores) for generator_name, scores in hall_of_fame.items()]
		hall_of_fame.sort()
		
		response = {
			'status': 'success',
			'hall_of_fame': hall_of_fame,
		}
	
	return response

def saveSession(session):
	# save game object to disk
	if session.game is not None:
		saveGame(session.game)
	
	session_file = os.path.join(config.sessions_directory, '{}.pickle'.format(session.id))
	if session.game is not None:
		game = session.game
		session.game = session.game.id
	with open(session_file, 'wb') as f:
		pickle.dump(session, f)
	
	if session.game is not None:
		session.game = game

def createSession(username, language):
	# load file of users
	users_file = os.path.join(config.users_directory, 'users.txt')
	users = {}
	if os.path.isfile(users_file):
		with open(users_file, encoding='utf-8') as f:
			for line in f:
				line = line.rstrip('\n')
				user_id, user_username = line.split('\t', 1)
				users[user_username] = user_id
	
	# create a new user_id for the user if need be
	if username not in users:
		user_id = User._generateId()
		
		# add user to the users file
		with open(users_file, 'a', encoding='utf-8') as f:
			print(user_id, username, sep='\t', file=f)
	else:
		user_id = users[username]
	
	# create session object
	session = Session(user_id, username, language)
	
	# save the users new session_id
	username_file = os.path.join(config.users_directory, '{}'.format(session.user_id))
	with open(username_file, 'a', encoding='utf-8') as f:
		print(session.id, file=f)
	
	# save session to disk
	saveSession(session)
	
	# return session object
	return session

def loadSession(session_file):
	with open(session_file, 'rb') as f:
		session = pickle.load(f)
	
	return session

def getSession(session_id):
	session_file = os.path.join(config.sessions_directory, '{}.pickle'.format(session_id))
	
	# check if the session id is valid
	if not os.path.isfile(session_file):
		return None
	
	# get session object
	session = loadSession(session_file)
	
	# get related game object and hook it up to the session object
	if session.game is not None:
		game_file = os.path.join(config.games_directory, '{}.pickle'.format(session.game))
		game = getGame(game_file)
		session.game = game
	
	# create Session object and return
	return session

def route(request):
	# make sure all the relevant data directories exist
	os.makedirs(config.games_archive_directory, exist_ok=True)
	os.makedirs(config.games_history_directory, exist_ok=True)
	os.makedirs(config.scores_directory, exist_ok=True)
	os.makedirs(config.sessions_directory, exist_ok=True)
	os.makedirs(config.users_directory, exist_ok=True)
	
	if not 'action' in request or not request['action']:
		response = {
			'status': 'error',
			'error': 'Empty or missing action',
		}
	elif request['action'] == 'new_session':
		if 'username' not in request or not request['username']:
			response = {
				'status': 'error',
				'error': 'Empty or missing username',
			}
			return response
		
		if 'language' not in request or request['language'] not in config.LANGUAGES:
			response = {
				'status': 'error',
				'error': 'Invalid or missing language',
			}
			return response
		
		# filter surrounding whitespace for username before trusting it blindly :-)
		# also do some lowercasing so Admin and admin aren't two completely different users :)
		username = request['username']
		username = username.strip()
		username = username.lower()
		
		session = createSession(username, request['language'])
		response = {
			'status': 'success',
			'session_id': session.id,
		}
	elif 'session_id' in request:
		session = getSession(request['session_id'])
		response = handleRequest(request, session)
		saveSession(session)
	else:
		response = {
			'status': 'error',
			'error': 'Invalid or missing session_id',
		}
	
	return response

def main():
	# make sure the logs directory exists
	os.makedirs(config.logs_directory, exist_ok=True)
	
	log_file = os.path.join(config.logs_directory, 'webserver.log')
	with open(log_file, 'a', encoding='utf-8') as stderr, contextlib.redirect_stderr(stderr):
		try:
			proper_stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8') # reopen stdin with the correct encoding (in python 3.7 and above you can use sys.stdin.reconfigure('utf-8') instead)
			request = json.load(proper_stdin)
			response = route(request)
			response = json.dumps(response, ensure_ascii=False)
			proper_stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
			print(response, file=proper_stdout) # similarly, use sys.stdout.reconfigure('utf-8') in Python 3.7 and above instead.
		except:
			# log error
			import traceback
			e = traceback.format_exc()
			print(e, file=sys.stderr)
			
			# send back generic error message
			response = {
				'status': 'error',
				'error': 'Internal Server Error',
			}
			response = json.dumps(response, ensure_ascii=False)
			print(response)
			
			# reraise exception
			raise

if __name__ == '__main__':
	main()

# FUTURE: allow multiple people to be in the same game and (possibly) let people spectate games. Test whether a session_id/user_id is participating in the game and whether it is their turn.
