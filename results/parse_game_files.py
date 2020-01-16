
import os
import re

def parse_card_string(string):
	cards = [match.group(1) for match in re.finditer('\'(\w+)\'', string)]
	return cards

def parse_card_rating_string(string):
	cards = zip([match.group(1) for match in re.finditer('\'(\w+)\'', string)], [float(match.group()) for match in re.finditer('\d+(\.\d+)?', string)])
	cards = list(sorted(cards, key=lambda x: x[1], reverse=True))
	return cards

# blacklist of games that had bugs or were otherwise invalid.
blacklisted_games = set([
	# max_hint_number bug for word embeddings top 1 Czech. (the hint number could be larger than 1)
	'f00c47d6-e9a9-4032-a649-c040ca490639',
	'f306d4b5-c340-47dc-8d13-8af736053117',
	'7c4a4633-f867-47e4-ba72-8a0e3fe955c6',
	'c2448b60-26ae-474d-bab2-75feca18af57',
	'fb3e436d-4d75-4345-8b2b-b0e950b13adc',
	'91c53c98-6dc5-4d82-bbbe-871be98107ac',
	
	# incorrect hint number setup for English word embedding games (no hint number was shown while playing these games)
	# top 1
	'3a3126ba-e126-494e-8a20-68b6d2f45031',
	'b25a2f2d-a3c7-4f5c-8a26-10ccb819d1c6',
	'eea54a92-28f6-4a08-9f1f-0c2fe218dbb6',
	'9c62942e-68aa-4a0b-9527-fbd2cf31a03e',
	'f595adde-acd2-4427-b7c2-3eb693e876b3',
	'a5adedb5-f763-4a78-b796-b960674e3783',
	'ae4c9d26-e21a-4845-a92d-328f0a73c88d',
	'9f487591-b83a-4a8a-8269-54c55b08af78',
	'd0282975-385f-42e0-84b3-d147e40d94ed',
	'76bbb1b5-61c9-4173-831e-ce3235f1b820',
	'a512a23a-a4a1-468b-af8b-794053487d7b',
	'e5db02b6-3d63-4465-aad0-cad358347fe4',
	'9281ef25-6794-4727-9057-d238247b33ff',
	'c1cfc993-78a9-49e0-8cc2-0efcca87e97c',
	'e892d657-96d9-4d66-80ab-28cffae5aa91',
	'5c2d1a31-6e87-4817-8fd5-66766ef36344',
	'67114828-0f07-4d19-aa3b-31a17a560878',
	'7a4b46c7-3223-40c1-b808-bb0285f00ac3',
	'b3d554d0-b88c-4135-9855-2ea1829a6f7c',
	
	# ...
	# top 2
	'1627b4f9-d559-4690-a900-5bc28495e948',
	'041378ee-9eca-4081-b797-a38c47c9185f',
	'4d3526d6-c0da-476c-8fd1-ba0f4a96c005',
	'60078395-4bfb-4814-a07c-45e6b3fc302a',
	'b7658ae0-cd48-4823-aff8-312029b1e5a3',
	'3ec41387-b093-4179-a408-1485f8043942',
	'a319ab51-b10c-445d-84b3-d1253be4f206',
	'9f098349-3d95-4f8a-a0f4-20e68891bf19',
	'f197b483-71dc-4562-886b-702e9c9663e0',
	'81fd46fc-95cd-4b9a-9294-8c5f124c4a35',
	'43470bb4-960c-44eb-91da-e7cc3f2bcc68',
	'b9ab504d-1894-4473-bde6-d33a3218c5db',
	'92d8a3be-0668-4578-86a8-212c49482e5f',
	'721af12d-f578-4fff-8f6a-05ec8d9511e5',
	'a55dd5ab-2fb1-4f29-9556-e134619d28c0',
	'52356bb2-3ec4-4639-bb61-b53feadfc354',
	'84b4db88-d142-4348-b24f-83c16cc34c96',
	'b5aa0230-7931-4965-a42f-de7ee3d36290',
	
	# ...
	# top 3
	'b1ceeaee-b7c0-4562-b2ce-dd976f3ecea8',
	'2524c2b9-e7a6-4cee-8255-e1c39e5d6839',
	'd53dd543-2a43-48ab-9c38-3f2d70154fe3',
	'976fdc59-f237-4eb4-8a65-056929c5fe97',
	'4111101e-ffdc-47bb-8df9-ac22ff7435a8',
	'527aac0a-616d-4845-b45a-deaa3111037a',
	'fb94394a-5f2b-41ac-8545-906fddb3e56a',
	'6638a028-5e31-44bf-88b5-553c8d1a6b12',
	'53006ff7-993c-4790-9317-05099eac45e5',
	'51c9a5ad-411a-4ec7-a17b-4cd6757a5495',
	'9f3b04b8-7dd4-492d-bd3e-c63d3535ec46',
	'3840c705-e8d3-401f-8109-6fad0a9cdbf5',
	'c0a17d39-831c-4210-8d91-f902a6bdbd68',
	'9d9f5c1c-71ec-4aa0-884b-9ef216436157',
	'ce0e52bf-e540-4aef-813e-22058da78fa5',
])

def get_games(data_dir, exclude_blacklisted_games=True):
	history_dir = os.path.join(data_dir, 'games', 'history')
	games = []
	for root, dirs, filenames in os.walk(history_dir):
		for filename in filenames:
			game = {'hints': [], 'hints_board': [], 'decisions': [], 'numbers': []}
			bad_game = False
			
			# extract game id, ai name, board, hints and player decisions from the game log
			game_log = os.path.join(root, filename)
			with open(game_log, encoding='utf-8') as f:
				turn_decisions = []
				turn = None
				for line in f:
					line = line.strip()
					if 'Game id:' in line:
						game['id'] = line.split('\t')[-1]
					if 'Game cards:' in line:
						board_string = ' '.join(line.split('\t')[2:])
						own_cards, enemy_cards, neutral_cards, assassin_cards = map(parse_card_string, board_string.split('] ['))
						game['board'] = (own_cards, enemy_cards, neutral_cards, assassin_cards)
					elif 'Game team 0' in line:
						game['ai_name'] = line.split(' ')[-3][1:-2]
					elif 'New hint' in line and 'team 0' in line:
						word = line.split(' ')[5][1:-2]
						
						if word == 'None':
							bad_game = True
							break # skip game files for which the server died and returned None type hints.
						
						if 'Relates to' in line:
							number = line.split(' ')[8]
							number = int(number)
							game['numbers'].append(number)
					elif 'Team 0 flipped card' in line:
						word = line.split(' ')[5][1:-2]
						
						if '\'blue\'.' in line:
							turn_decisions.append((word, 'own'))
						elif '\'red\'.' in line:
							turn_decisions.append((word, 'enemy'))
						elif '\'neutral\'.' in line:
							turn_decisions.append((word, 'neutral'))
						elif '\'assassin\'.' in line:
							turn_decisions.append((word, 'assassin'))
					elif 'Team 0 has initiative.' in line:
						turn = int(line.split('\t')[0])
						if turn % 2 == 1 and turn != 1:
							game['decisions'].append(turn_decisions)
						turn_decisions = []
					elif 'won.' in line:
						game['winner'] = int(line.split(' ')[1])
					elif 'turned over' in line:
						game['win_condition'] = line.split('\t')[1]
			
			if bad_game: # skip game files for which the server died and returned None type hints.
				continue
			
			game['decisions'].append(turn_decisions)
			
			# extract hint ratings from the relevant hint files
			hints_log = os.path.join(data_dir, 'hints', game['ai_name'], '{}.log'.format(game['id']))
			try:
				with open(hints_log, encoding='utf-8') as f:
					for line in f:
						line = line.strip()
						if 'Generated hint' in line:
							hint = line.split(' ')[3][1:-1]
							rating = float(line.split(' ')[6][1:-1])
							game['hints'].append((hint, rating))
						elif 'Cosine similarities' in line or 'PMI scores' in line:
							board_string = '['.join(line.split('[')[1:]) # remove text before the board string
							own_cards, enemy_cards, neutral_cards, assassin_cards = map(parse_card_rating_string, board_string.split('] ['))
							game['hints_board'].append((own_cards, enemy_cards, neutral_cards, assassin_cards))
			except FileNotFoundError: # ignore old files for which no hints were logged
				continue
			
			# recover intermittent board states for dep_col_and_word_embeddings_combined_cz_v1.0 and _en_v1.0 (without ratings unfortunately, it's a bit of work to do that, although not impossible)
			if not game['hints_board']:
				board = tuple([(word, None) for word in cards] for cards in game['board'])
				game['hints_board'].append(board)
				for decisions in game['decisions']:
					for decision_word, decision in decisions:
						board = tuple([(word, None) for word, _ in cards if word.lower() != decision_word.lower()] for cards in board)
					game['hints_board'].append(board)
			
			games.append(game)
	
	if exclude_blacklisted_games:
		games = [game for game in games if game['id'] not in blacklisted_games]
	
	return games
