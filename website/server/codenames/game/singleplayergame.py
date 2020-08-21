
import random

import codenames.ai as ai
from .game import Game
from .team import Team

class SinglePlayerGame(Game):
	def __init__(self, users, possible_words, games_directory, generator_sockets, ai_name=None, teams=None):
		if teams is None and ai_name is not None:
			team = Team(
				ai.AI(ai_name),
				[ai.Player(users[0])]
			)
			dummy_team = Team(
				ai.DummyAI('dummy_ai'),
				[ai.DummyPlayer('dummy_player')]
			)
			teams = (team, dummy_team)
		
		# make sure the player begins and is always blue
		initiative = 0
		
		super().__init__(users, possible_words, teams=teams, games_directory=games_directory, generator_sockets=generator_sockets, initiative=initiative)
		
		self.last_enemy_turn = None
	
	def getScoreByTeam(self, team_index):
		positive_cards, negative_cards, _, assassin_cards = self.getActiveCardsByType(team_index=team_index)
		if len(assassin_cards) == 0:
			return 0
		
		enemy_guessed = 8 - len(negative_cards)
		score = 8 - enemy_guessed
		
		return score
	
	def getCardsLeftByTeam(self, team_index):
		positive_cards, _, _, _ = self.getActiveCardsByType(team_index=team_index)
		cards_left = len(positive_cards)
		
		return cards_left
	
	def endTurn(self):
		super().endTurn()
		
		if self.hint == (False, None): # if the generateHint() method returns (False, None), we know it was the dummy team's spymaster, so we simulate the dummy teams turn
			# find one of the dummy team's cards and flip it over
			positive_cards, negative_cards, neutral_cards, assassin_cards = self.getActiveCardsByType()
			card = random.choice(positive_cards)
			turn_ended = self.flipCard(card) # turn could be ended if the AI flipped their last card
			
			self.last_enemy_turn = {
				'flipped': [card],
			}
			
			# pass the turn back over to the player's team
			if not turn_ended:
				self.endTurn()
