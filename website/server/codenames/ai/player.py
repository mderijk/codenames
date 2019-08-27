

class Player:
	def __init__(self, name):
		self.name = name

class DummyPlayer(Player):
	def __init__(self, name='dummy_player'):
		self.name = name
