
import datetime
import pickle
import os
import uuid

from . import module

__all__ = ['Sessions']

class User:
	@classmethod
	def _generateId(cls, users_directory):
		# create user id and make sure it doesn't exist yet
		while True:
			id = str(uuid.uuid4())
			user_file = os.path.join(users_directory, '{}'.format(id))
			
			if not os.path.isfile(user_file):
				break
		
		return id

class Session:
	def __init__(self, user_id, username, language, game=None, sessions_directory=os.path.join('data', 'sessions')):
		self.id = self._generateId(sessions_directory)
		self.user_id = user_id
		self.username = username
		self.language = language
		self.game = game
		self.last_seen = datetime.datetime.now()
	
	def _generateId(self, sessions_directory):
		# create session id and make sure it doesn't exist yet
		while True:
			id = str(uuid.uuid4())
			game_file = os.path.join(sessions_directory, '{}.pickle'.format(id))
			
			if not os.path.isfile(game_file):
				break
		
		return id

class Sessions(module.Module):
	def createSession(self, username, language):
		# load file of users
		users_file = os.path.join(self.config.users_directory, 'users.txt')
		users = {}
		if os.path.isfile(users_file):
			with open(users_file, encoding='utf-8') as f:
				for line in f:
					line = line.rstrip('\n')
					user_id, user_username = line.split('\t', 1)
					users[user_username] = user_id
		
		# create a new user_id for the user if need be
		if username not in users:
			user_id = User._generateId(self.config.users_directory)
			
			# add user to the users file
			with open(users_file, 'a', encoding='utf-8') as f:
				print(user_id, username, sep='\t', file=f)
		else:
			user_id = users[username]
		
		# create session object
		session = Session(user_id, username, language, sessions_directory=self.config.sessions_directory)
		
		# save the users new session_id
		username_file = os.path.join(self.config.users_directory, '{}'.format(session.user_id))
		with open(username_file, 'a', encoding='utf-8') as f:
			print(session.id, file=f)
		
		# save session to disk
		self.saveSession(session)
		
		# return session object
		return session
	
	def loadSession(self, session_file):
		with open(session_file, 'rb') as f:
			session = pickle.load(f)
		
		return session
	
	def getSession(self, session_id):
		session_file = os.path.join(self.config.sessions_directory, '{}.pickle'.format(session_id))
		
		# check if the session id is valid
		if not os.path.isfile(session_file):
			return None
		
		# load session object from disk
		session = self.loadSession(session_file)
		
		# update last seen date
		self.last_seen = datetime.datetime.now()
		
		return session
	
	def saveSession(self, session):
		# save session to disk
		session_file = os.path.join(self.config.sessions_directory, '{}.pickle'.format(session.id))
		with open(session_file, 'wb') as f:
			pickle.dump(session, f)
