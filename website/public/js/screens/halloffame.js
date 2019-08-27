"use strict";

function HallOfFame(application, client) {
	this.header = null;
	this.hall_of_fame = null;
	this.menu_button = null;
	this.num_rows = 10;
	
	this.build = function(container) {
		// create header
		this.header = document.createElement('h1');
		this.header.textContent = 'Hall Of Fame';
		this.header.id = 'hall-of-fame-header';
		
		// create hall of fame
		this.hall_of_fame = document.createElement('table');
		this.hall_of_fame.id = 'hall-of-fame';
		
		// create menu button
		this.menu_button = document.createElement('input');
		this.menu_button.type = 'button';
		this.menu_button.className = 'button';
		this.menu_button.addEventListener('click', application.showMenu.bind(application));
		this.menu_button.value = 'Return to menu';
		
		container.appendChild(this.header);
		container.appendChild(this.hall_of_fame);
		container.appendChild(this.menu_button);
		
		this.getHallOfFame();
	};
	
	this.destroy = function() {
		this.header.parentNode.removeChild(this.header);
		this.hall_of_fame.parentNode.removeChild(this.hall_of_fame);
		this.menu_button.parentNode.removeChild(this.menu_button);
		
		this.header = null;
		this.hall_of_fame = null;
		this.menu_button = null;
	};
	
	this.getHallOfFame = function() {
		var data = {
			'session_id': client.session.id,
			'action': 'get_hall_of_fame',
		};
		client.sendRequest(data, function(response) {
			// add row with AI names
			var header_row = document.createElement('tr');
			var rank_cell = document.createElement('th');
			rank_cell.textContent = 'Rank';
			header_row.appendChild(rank_cell);
			for (var i = 0; i < response.hall_of_fame.length; i++) {
				var ai_name = response.hall_of_fame[i][0];
				var name_cell = document.createElement('th');
				name_cell.colSpan = 2;
				name_cell.textContent = ai_name;
				
				header_row.appendChild(name_cell);
			}
			this.hall_of_fame.appendChild(header_row);
			
			// add rows with scores for each AI
			for (var i = 0; i < this.num_rows; i++) {
				var scores_row = document.createElement('tr');
				
				var rank_cell = document.createElement('td');
				rank_cell.textContent = i + 1;
				rank_cell.className = 'rank';
				scores_row.appendChild(rank_cell);
				
				for (var j = 0; j < response.hall_of_fame.length; j++) {
					var score = '',
						username = '';
					if (response.hall_of_fame[j][1].length > i) {
						score = response.hall_of_fame[j][1][i][0];
						username = response.hall_of_fame[j][1][i][1];
					}
					
					var score_cell = document.createElement('td');
					score_cell.textContent = score;
					score_cell.className = 'score';
					var username_cell = document.createElement('td');
					username_cell.className = 'username';
					username_cell.textContent = username;
					if (username === client.session.username) {
						username_cell.className += ' user';
					}
					
					scores_row.appendChild(score_cell);
					scores_row.appendChild(username_cell);
				}
				this.hall_of_fame.appendChild(scores_row);
			}
		}.bind(this));
	};
}
