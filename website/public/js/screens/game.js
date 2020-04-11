"use strict";

function Game(client, application) {
	this.card_click_functions = [];
	this.board_screen = null;
	this.banner = null;
	this.board = null;
	this.left_floaty = null;
	this.right_floaty = null;
	this.current_hint_display = null;
	this.current_hint = null;
	this.hint_list = null;
	this.score_board = null;
	this.turn = null;
	this.team_score = null;
	this.cards_left = null;
	this.menu_button = null;
	this.new_hint_button = null;
	var ai = null;
	
	// Build screen elements
	this.build = function(container) {
		this.board_screen = document.createElement('div');
		this.board_screen.id = 'board-screen';
		
		// create banner
		this.banner = document.createElement('banner');
		this.banner.id = 'banner';
		
		// create game board
		this.board = document.createElement('div');
		this.board.id = 'board';
		
		// create display for current hint
		this.current_hint_display = document.createElement('div');
		this.current_hint_display.textContent = 'Current hint: ';
		this.current_hint = document.createElement('span');
		this.current_hint.id = 'current-hint';
		this.current_hint_display.appendChild(this.current_hint);
		
		// create list of hints
		this.hint_list = document.createElement('ul');
		this.hint_list.id = 'hints';
		
		// create score board
		this.score_board = document.createElement('div');
		this.score_board.id = 'score-board';
		
		this.turn = document.createElement('div');
		this.team_score = document.createElement('div');
		this.cards_left = document.createElement('div');
		this.score_board.appendChild(this.turn);
		this.score_board.appendChild(this.team_score);
		this.score_board.appendChild(this.cards_left);
		
		// create new hint button
		this.new_hint_button = document.createElement('input');
		this.new_hint_button.type = 'button';
		this.new_hint_button.className = 'button';
		this.new_hint_button.addEventListener('click', this.newHint.bind(this));
		this.new_hint_button.value = 'End turn';
		
		// create menu button
		this.menu_button = document.createElement('input');
		this.menu_button.type = 'button';
		this.menu_button.className = 'button';
		this.menu_button.addEventListener('click', application.showMenu.bind(application));
		this.menu_button.value = 'Return to menu';
		
		// create left panel
		this.left_floaty = document.createElement('div');
		this.left_floaty.className = 'half-width left';
		
		// create right panel
		this.right_floaty = document.createElement('div');
		this.right_floaty.className = 'half-width right';
		
		// add elements to the container
		this.board_screen.appendChild(this.banner);
		this.board_screen.appendChild(this.board);
		
		this.left_floaty.appendChild(this.current_hint_display);
		this.left_floaty.appendChild(this.hint_list);
		this.board_screen.appendChild(this.left_floaty);
		
		this.right_floaty.appendChild(this.score_board);
		this.right_floaty.appendChild(this.new_hint_button);
		this.right_floaty.appendChild(this.menu_button);
		this.board_screen.appendChild(this.right_floaty);
		
		container.appendChild(this.board_screen);
		
		// populate the board
		this.getBoard();
	};
	
	// Destroy screen elements
	this.destroy = function() {
		// remove the UI elements from the container
		this.board_screen.parentNode.removeChild(this.board_screen);
		
		// destroy references to the old UI elements to prevent memory leaks
		this.board_screen = null;
		this.banner = null;
		this.board = null;
		this.left_floaty = null;
		this.right_floaty = null;
		this.current_hint = null;
		this.current_hint_display = null;
		this.hint_list = null;
		this.score_board = null;
		this.turn = null;
		this.team_score = null;
		this.cards_left = null;
		this.menu_button = null;
		this.new_hint_button = null;
	}
	
	this.addHint = function(hint) {
		var word = hint[0],
			number = hint[1],
			old_hint = this.current_hint.textContent;
		
		if (number === null) {
			this.current_hint.textContent = word;
		} else {
			this.current_hint.textContent = word + ', ' + number;
		}
		
		if (old_hint !== '') {
			var hint_list_item = document.createElement('li');
			var hint_text = document.createTextNode(old_hint);
			hint_list_item.appendChild(hint_text);
			this.hint_list.insertBefore(hint_list_item, this.hint_list.childNodes[0]);
		}
	};
	
	this.updateGameState = function(response) {
		if (response.hint !== undefined) {
			// display new hint
			this.addHint(response.hint);
		}
		
		if (response.enemy_turn !== undefined && response.enemy_turn !== null) {
			// show the cards that the enemy flipped over
			for (var i = 0; i < response.enemy_turn.flipped.length; i++) {
				var card = response.enemy_turn.flipped[i];
				this.flipOverCard(card);
			}
		}
		
		if (response.turn !== undefined) {
			this.turn.textContent = 'Turn: ' + Math.floor((response.turn + 1) / 2);
		}
		
		if (response.score !== undefined) {
			this.team_score.textContent = 'Score: ' + response.score;
		}				
		
		if (response.cards_left !== undefined) {
			this.cards_left.textContent = 'Cards left: ' + response.cards_left;
		}
		
		if (response.winner !== undefined) {
			// announce winner on screen
			var text1 = document.createElement('span');
			text1.textContent = client.session.username + ' and ' + this.ai_name;
			var text2 = document.createElement('span');
			text2.textContent = 'against team Dummy.';
			var outcome = document.createElement('span');
			
			if (response.winner === 0) {
				outcome.textContent = ' won ';
				outcome.className = 'winner';
			} else {
				outcome.textContent = ' lost ';
				outcome.className = 'loser';
			}
			this.banner.textContent = '';
			this.banner.appendChild(text1);
			this.banner.appendChild(outcome);
			this.banner.appendChild(text2);
			
			// remove the event listeners that are still left
			while (this.card_click_functions.length > 0) {
				var event_listener = this.card_click_functions.pop();
				var card_node = event_listener[0];
				var card_click_function = event_listener[1];
				card_node.removeEventListener('click', card_click_function);
			}
			
			// show the cards that were never flipped during the game
			for (var i = 0; i < response.cards.length; i++) {
				var card = response.cards[i];
				this.flipOverCard(card, true);
			}
			
			// let the rest of the application know we are not in game anymore
			client.session.in_game = false;
			client.saveSession();
			
			// change return to menu text to clarify that this is the last chance to look at the game
			this.menu_button.value = 'Exit game';
			
			// remove new hint button
			this.new_hint_button.parentNode.removeChild(this.new_hint_button);
			this.new_hint_button = null;
			
			// show the intended targets and their scores when hovering over a hint
			if (response.hints !== undefined) {
				var hint = response.hints[response.hints.length - 1],
					target_cards = hint[1];
				
				this.addHintTargetWordsHover(this.current_hint, target_cards);
				
				for (var i = 0; i < this.hint_list.childNodes.length; i++) {
					var hint_list_item = this.hint_list.childNodes[i];
						hint = response.hints[this.hint_list.childNodes.length - 1 - i],
						target_cards = hint[1];
					
					this.addHintTargetWordsHover(hint_list_item, target_cards);
				}
			}
		}
		
		// remove the loading status again
		application.clearStatus();
	};
	
	this.addHintTargetWordsHover = function(node, target_cards) {
		node.addEventListener('mouseover', function(e) {
			for (var i = 0; i < target_cards.length; i++) {
				var target_card = target_cards[i],
					card = target_card[0],
					score = target_card[0];
				
				this.addCardHighlight(card);
				node.className = 'highlight';
			}
		}.bind(this));
		node.addEventListener('mouseout', function(e) {
			for (var i = 0; i < target_cards.length; i++) {
				var target_card = target_cards[i],
					card = target_card[0],
					score = target_card[0];
				
				this.removeCardHighlight(card);
				node.className = '';
			}
		}.bind(this));
	};
	
	this.addCardHighlight = function(card) {
		var post_game;
		if (card.flipped) {
			post_game = '';
		} else {
			post_game = ' post-game';
		}
		var card_node = this.board.childNodes[card.id];
		card_node.className = 'card ' + card.type + post_game + ' target';
	};
	
	this.removeCardHighlight = function(card) {
		var post_game;
		if (card.flipped) {
			post_game = '';
		} else {
			post_game = ' post-game';
		}
		var card_node = this.board.childNodes[card.id];
		card_node.className = 'card ' + card.type + post_game;
	};
	
	this.selectCard = function(card_id) {
		var data = {session_id: client.session.id, action: 'flip'};
		data.card_id = card_id;
		
		client.sendRequest(data, function(response) {
			this.flipOverCard(response.card);
			
			this.updateGameState(response);
		}.bind(this));
	};
	
	this.flipOverCard = function(card, is_post_game) {
		var post_game;
		if (is_post_game) {
			post_game = ' post-game';
		} else {
			post_game = '';
		}
		var card_node = this.board.childNodes[card.id];
		card_node.className = 'card ' + card.type + post_game;
	};
	
	this.addCardToBoard = function(card) {
		var card_node = document.createElement('span');
		var card_text = document.createTextNode(card.word);
		var card_click_function;
		
		if (card.flipped === true) {
			card_node.className = 'card ' + card.type;
		} else {
			card_node.className = 'card';
			
			// make card clickable
			card_click_function = function(e) {
				this.selectCard(card.id);
				
				// make sure you can't flip cards more than once
				card_node.removeEventListener('click', card_click_function);
			}.bind(this);
			card_node.addEventListener('click', card_click_function);
			this.card_click_functions.push([card_node, card_click_function]);
		}
		
		card_node.appendChild(card_text);
		this.board.appendChild(card_node);
	};
	
	this.newGame = function() {
		// let the player know we are loading the game which might take time.
		application.setStatus('Creating game...');
		
		var data = {session_id: client.session.id, action: 'new_game'};
		client.sendRequest(data, function(response) {
			client.session.in_game = true;
			client.saveSession();
			
			application.showGame();
			
			// remove the loading status again
			application.clearStatus();
		}.bind(this));
	};
	
	this.getBoard = function() {
		// let the player know we are loading the game which might take time.
		application.setStatus('Loading game...');
		
		var data = {session_id: client.session.id, action: 'get_board'};
		client.sendRequest(data, this.addCardsToBoard.bind(this));
	};
	
	this.addCardsToBoard = function(response) {
		// add cards to board
		for (var i = 0; i < response.board.cards.length; i++) {
			var card = response.board.cards[i];
			this.addCardToBoard(card);
		}
		
		// display AI name in the banner
		this.ai_name = response.ai;
//		this.banner.textContent = client.session.username + ' playing singleplayer with ' + this.ai_name + ' as spymaster.';
		application.setDefaultStatus('On a mission with ' + this.ai_name);
		
		// display hints on screen
		response.hints.forEach(function(hint) {
			this.addHint(hint);
		}.bind(this));
		
		this.updateGameState(response);
	};
	
	this.newHint = function() {
		// let the player know we are generating a new hint which might take time.
		application.setStatus('Generating new hint...');
		
		var data = {session_id: client.session.id, action: 'end_turn'};
		client.sendRequest(data, this.updateGameState.bind(this));
	};
}
