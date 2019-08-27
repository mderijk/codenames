"use strict";

function Menu() {
	var introduction = null,
		menu = null,
		options = [];
	
	this.build = function(container) {
		// create introduction
		introduction = document.createElement('div');
		introduction.id = 'introduction';
		
		var fill = document.createElement('div');
		fill.className = 'fill';
		
		introduction.appendChild(fill);
		
		var welcome = document.createElement('div');
		welcome.id = 'welcome';
		welcome.textContent = 'Welcome, agent! Today you are up against the infamous team Dummy. Guess all their cards before they guess yours! To assist you in your secret mission, we will pair you with one of our AIs who will give you covert hints.';
		
		// create explanation section
		var how_to_play_header = document.createElement('h2');
		how_to_play_header.textContent = 'How to Play';
		
		var how_to_play = document.createElement('div');
		how_to_play.id = 'how-to-play';
		
		// create explanation board
		var explanation_cards = document.createElement('div');
		explanation_cards.id = 'explanation-cards';
		
		// create concealed card
		var concealed_card_wrapper = document.createElement('div');
		concealed_card_wrapper.className = 'card-wrapper full-width';
		var concealed_card_span = document.createElement('span');
		concealed_card_span.textContent = 'Dance';
		concealed_card_span.className = 'card';
		concealed_card_wrapper.appendChild(concealed_card_span);
		
		var concealed_card_explanation_text = document.createTextNode('Concealed (25)');
		concealed_card_wrapper.appendChild(concealed_card_explanation_text);
		
		explanation_cards.appendChild(concealed_card_wrapper);
		
		var cards = [
			['Knight', 'blue', 'Your team (9)'],
			['Tokyo', 'red', 'Enemy team (8)'],
			['Chocolate', 'neutral', 'Neutral (7)'],
			['Penguin', 'assassin', 'Assassin (1)'],
		];
		for (var i = 0; i < cards.length; i++) {
			var card = cards[i],
				card_text = card[0],
				card_type = card[1],
				card_explanation = card[2];
			
			var card_wrapper = document.createElement('div');
			card_wrapper.className = 'card-wrapper';
			var card_span = document.createElement('span');
			card_span.textContent = card_text;
			card_span.className = 'card ' + card_type;
			card_wrapper.appendChild(card_span);
			
			var card_explanation_text = document.createTextNode(card_explanation);
			card_wrapper.appendChild(card_explanation_text);
			
			explanation_cards.appendChild(card_wrapper);
		}
		how_to_play.appendChild(explanation_cards);
		
		var how_to_play_text1 = document.createElement('p');
		how_to_play_text1.textContent = 'The goal of the game is to turn over all your cards (blue) before the enemy turns over all of theirs (red). The game starts with 25 concealed cards (grey), 9 of which belong to your team and 8 to the enemy team, your team starts. Each turn you can turn over cards by clicking on them. You can keep guessing until you reveal a card that does not belong to your team, after which the turn ends. There is one assassin card (black) which you want to avoid, because you lose the game if you turn it over. Revealing a neutral card helps neither player, but does end your turn. At the start of each turn your teammate will give you a hint that is related to the words of your team. During the enemy team\'s turn (team Dummy) they will turn over one of their own cards and pass the game back to you.';
		var how_to_play_text2 = document.createElement('p');
		how_to_play_text2.textContent = 'The current and previous hints are displayed in the bottom left below the game board. Some information about your mission is displayed in the status box in the top right corner of the screen. If a hint is too cryptic or you want to play it safe, you can end your turn and get a new hint by pressing the End turn button. Click the New Game button below to start playing.';
		how_to_play.appendChild(how_to_play_text1);
		how_to_play.appendChild(how_to_play_text2);
		
		var additional_notes_header = document.createElement('h2');
		additional_notes_header.textContent = 'Project Notes';
		var additional_notes_text1 = document.createElement('p');
		additional_notes_text1.textContent = 'The goal of this project is to test different strategies for generating good hints. Our AIs are not perfect, so you will occassionally see a hint that does not make sense.'
		
		var additional_notes_text2 = document.createElement('p');
		additional_notes_text2.textContent = 'Good luck beating team Dummy!';
		
		introduction.appendChild(welcome);
		introduction.appendChild(how_to_play_header);
		introduction.appendChild(how_to_play);
		introduction.appendChild(additional_notes_header);
		introduction.appendChild(additional_notes_text1);
		introduction.appendChild(additional_notes_text2);
		
		// add bottom fill
		var bottom_fill = document.createElement('div');
		bottom_fill.className = 'bottom-fill';
		
		introduction.appendChild(bottom_fill);
		
		// create menu wrapper
		menu = document.createElement('div');
		menu.id = 'menu-wrapper';
		
		// create menu
		var menu_items = document.createElement('ul');
		menu_items.id = 'menu';
		
		// add each menu option to the ul element
		options.forEach(function(menu_option) {
			var name = menu_option[0],
				onclick = menu_option[1];
			
			// create menu item
			var item = document.createElement('li');
			var item_text = document.createTextNode(name);
			
			// add onclick method
			if (onclick !== undefined) {
				item.addEventListener('click', onclick);
			}
			
			// add the new item to the menu
			item.appendChild(item_text);
			menu_items.appendChild(item);
		}, this);
		
		menu.appendChild(menu_items);
		
		container.appendChild(introduction);
		container.appendChild(menu);
	};
	
	this.destroy = function() {
		introduction.parentNode.removeChild(introduction);
		menu.parentNode.removeChild(menu);
		
		introduction = null;
		menu = null;
	};
	
	this.rebuild = function() {
		var container = menu.parentNode;
		this.destroy();
		this.build(container);
	};
	
	this.addOption = function(name, onclick) {
		options.push([name, onclick]);
	};
	
	this.changeOption = function(index, name, onclick) {
		options[index] = [name, onclick];
	};
}
