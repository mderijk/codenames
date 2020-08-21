
import os
import random
import uuid

from .card import Card

class Game:
	team_names = ('blue', 'red')
	team_card_colors = ('blue', 'red')
	
	def __init__(self, users, possible_words, teams, games_directory, generator_sockets, initiative=None):
		self.games_directory = games_directory
		self.id = self._generateId()
		self.users = users
		self.history = []
		self._cards = []
		self._cards_by_word = {}
#		self._points = [0, 0]
		self.teams = teams
#		self.teams = (('player1_username', 'ai1'), ('player2_username', 'ai2')) # teams are referred to by index (0 and 1)
		self.generator_sockets = generator_sockets
		self.hint = None
		self.hints = tuple([] for _ in self.teams)
		self.winner = None
		self.ended = False
		
		if initiative is None:
			self.initiative = random.randrange(2) # 0 means blue begins, 1 means red begins
		else:
			self.initiative = initiative
		self.turn = 1
		
		labels = ['blue'] * (9 - self.initiative) + ['red'] * (8 + self.initiative) + ['neutral'] * 7 + ['assassin']
		random.shuffle(labels)
		cards = zip(labels, random.sample(possible_words, 25))
		
		for id, (label, word) in enumerate(cards):
			word = word.capitalize()
			card = Card(id, label, word)
			self._cards.append(card)
			
			word = word.lower()
			self._cards_by_word[word.lower()] = card
		
		self.history.append((self.turn, 'Game id:', self.id))
		self.history.append((self.turn, 'Game cards:', *self.getActiveWordsByType(team_index=0))) # [team_0], [team_1], [civilian], [assassin]
		for index, team in enumerate(self.teams):
			self.history.append((self.turn, 'Game team {}: spymaster \'{}\', agents {}'.format(index, team.spymaster.name, [agent.name for agent in team.agents])))
		self.history.append((self.turn, 'Game has started.'))
		self.history.append((self.turn, 'Team {} has initiative.'.format(self.initiative)))
		
		self.generateHint()
	
	def _generateId(self):
		# create game id and make sure it doesn't exist yet
		while True:
			id = str(uuid.uuid4())
			game_file = os.path.join(self.games_directory, '{}.pickle'.format(id))
			
			if not os.path.isfile(game_file):
				break
		
		return id
	
	@property
	def cards(self):
		return self._cards
	
	def getCardByWord(self, word):
		word = word.lower()
		return self._cards_by_word[word]
	
	def getActiveCardsByType(self, team_index=None):
		if team_index is None:
			team_index = self.initiative
		
		positive_cards = [card for card in self._cards if not card.flipped and card.type == self.team_card_colors[team_index]]
		negative_cards = [card for card in self._cards if not card.flipped and card.type == self.team_card_colors[(team_index + 1) % 2]]
		neutral_cards = [card for card in self._cards if not card.flipped and card.type == 'neutral']
		assassin_cards = [card for card in self._cards if not card.flipped and card.type == 'assassin']
		
		return positive_cards, negative_cards, neutral_cards, assassin_cards
	
	def getActiveWordsByType(self, team_index=None):
		cards_by_type = self.getActiveCardsByType(team_index=team_index)
		positive_words, negative_words, neutral_words, assassin_words = tuple([card.word.lower() for card in cards] for cards in cards_by_type)
		
		return positive_words, negative_words, neutral_words, assassin_words
	
	def checkGameEnd(self, card):
		game_ended = True
		if card.type == 'assassin':
			self.winner = (self.initiative + 1) % 2
			self.history.append((self.turn, 'Team {} turned over the assassin.'.format(self.initiative)))
			self.history.append((self.turn, 'Team {} won.'.format(self.winner)))
		elif all(card.flipped for card in self._cards if card.type == 'blue'):
			self.winner = self.team_card_colors.index('blue')
			self.history.append((self.turn, 'All of team {}\'s cards were turned over.'.format(self.winner)))
			self.history.append((self.turn, 'Team {} won.'.format(self.winner)))
		elif all(card.flipped for card in self._cards if card.type == 'red'):
			self.winner = self.team_card_colors.index('red')
			self.history.append((self.turn, 'All of team {}\'s cards were turned over.'.format(self.winner)))
			self.history.append((self.turn, 'Team {} won.'.format(self.winner)))
		else:
			game_ended = False
		
		self.ended = game_ended
	
	def generateHint(self):
		# get current team and words on the board that haven't been turned over yet
		current_team = self.teams[self.initiative]
		positive_words, negative_words, neutral_words, assassin_words = self.getActiveWordsByType()
		
		# generate hint and log it
		previous_hints = [(word, number) for word, number in self.hints[self.initiative] if word] # filter out potential None types generated when the hint servers were offline.
		self.hint = current_team.spymaster.generateHint(self.id, positive_words, negative_words, neutral_words, assassin_words, generator_sockets=self.generator_sockets, previous_hints=previous_hints)
		if self.hint is None:
			self.hint = (None, None)
			self.history.append(('ERROR', 'Received NoneType hint. Hint servers might be offline.'))
			return
		
		self.hints[self.initiative].append(self.hint)
		self.history.append((self.turn, 'New hint for team {}: \'{}\'. Target cards and scores: {}'.format(self.initiative, *self.hint)))
	
	def endTurn(self):
		self.turn += 1
		self.history.append((self.turn, 'New turn.'))
		self.initiative = (self.initiative + 1) % 2
		self.history.append((self.turn, 'Team {} has initiative.'.format(self.initiative)))
		
		self.generateHint()
	
	def flipCard(self, card):
		card.flipped = True
		self.history.append((self.turn, 'Team {0} flipped card {1}, \'{2}\', \'{3}\'.'.format(self.initiative, card.id, card.word, card.type)))
		
		self.checkGameEnd(card)
		if not self.ended:
			turn_ended = False
			team_card_color = self.team_card_colors[self.initiative]
			if team_card_color != card.type: # end the team's turn if they flipped over a card that does not belong to their team.
				self.endTurn()
				turn_ended = True
		else:
			self.history.append((self.turn, 'Game has ended.'))
			turn_ended = True
		
		return turn_ended
