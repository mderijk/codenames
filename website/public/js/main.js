"use strict";

function Application(client, wizard) {
	this.status_message = null;
	this.blinking = false;
	
	this.setDefaultStatus = function(message) {
		this.status_message = message;
		if (!this.blinking) {
			this.status_bar.textContent = this.status_message;
		}
	};
	
	this.setStatus = function(message) {
		this.status_bar.className = 'blink';
		this.status_bar.textContent = message;
		this.blinking = true;
	};
	
	this.clearStatus = function() {
		this.status_bar.className = '';
		this.status_bar.textContent = this.status_message;
		this.blinking = false;
	};
	
	this.newGame = function() {
		wizard.screens.game.newGame();
	};
	
	this.showUsername = function() {
		wizard.show('username');
	};
	
	this.showHallOfFame = function() {
		wizard.show('hall of fame');
		this.setDefaultStatus('Admiring our best agents');
	};
	
	this.showSettings = function() {
		wizard.show('settings');
	};
	
	this.showGame = function() {
		wizard.show('game');
	};
	
	this.showMenu = function() {
		this.refreshMenu();
		wizard.show('menu');
		this.setDefaultStatus('Undergoing mission briefing');
	};
	
	this.refreshMenu = function() {
		if (client.session.in_game === true) {
			// show resume game button
			wizard.screens.menu.changeOption(0, 'Resume game', this.showGame.bind(this));
		} else {
			// show new game button
			wizard.screens.menu.changeOption(0, 'New game', this.newGame.bind(this));
		}
	};
	
	this.init = function() {
		// if there is a session, verify client version that the session was created on
		if (client.session !== null && (!client.session.version || client.session.version !== client.version)) {
			// incompatible version, delete old session
			console.log('Session created on incompatible version, deleting old session.');
			client.session = null;
		}
		
		// create status bar
		this.status_bar = document.createElement('div');
		this.status_bar.id = 'status-bar';
		wizard.addElement(this.status_bar);
		
		if (client.session === null) {
			// show username screen (one time thing)
			this.showUsername();
		} else if (client.session.in_game === true) {
			// show active game
			this.showGame();
		} else {
			// show menu
			this.showMenu();
		}
	};
}

function init() {
	// create client, wizard and application
	var client = new Client(),
		wizard = new Wizard(document.body),
		application = new Application(client, wizard);
	
	// build UI screens
	var username = new Username(application, client);
	username.addLanguageOption('Czech', 'cz');
	username.addLanguageOption('English', 'en');
	var hall_of_fame = new HallOfFame(application, client);
	var settings = new Settings(application, client);
	settings.addLanguageOption('Czech', 'cz');
	settings.addLanguageOption('English', 'en');
	var menu = new Menu();
	menu.addOption('New Game', application.newGame.bind(application));
	menu.addOption('Hall of Fame', application.showHallOfFame.bind(application));
	menu.addOption('Settings', application.showSettings.bind(application));
	var game = new Game(client, application);
	
	// add screens to wizard
	wizard.add('username', username);
	wizard.add('hall of fame', hall_of_fame);
	wizard.add('settings', settings);
	wizard.add('menu', menu);
	wizard.add('game', game);
	
	// start application
	application.init();
}

document.addEventListener('DOMContentLoaded', init);
