"use strict";

function Settings(application, client) {
	this.header = null;
	this.settings_form = null;
	this.language_select = null;
	this.menu_button = null;
	
	var language_options = [];
	
	this.build = function(container) {
		// create header
		this.header = document.createElement('h1');
		this.header.textContent = 'Settings';
		
		// create username form
		this.settings_form = document.createElement('form');
		this.settings_form.id = 'settings-form';
		
		// create username field
		var username_field = document.createElement('div');
		username_field.id = 'username-field';
		username_field.textContent = 'Username: ' + client.session.username;
		
		// create language select
		var language_select_wrapper = document.createElement('div');
		language_select_wrapper.textContent = 'Language: ';
		this.language_select = document.createElement('select');
		this.language_select.id = 'language';
		this.language_select.required = true;
		language_select_wrapper.appendChild(this.language_select);
		
		// add options to language select
		language_options.forEach(function(language_option) {
			var name = language_option[0],
				value = language_option[1];
			
			var opt = document.createElement('option');
			opt.textContent = name;
			if (value === client.session.language) {
				opt.selected = true;
			}
			opt.value = value;
			this.language_select.appendChild(opt);
		}, this);
		
		// create submit button
		var submit_button = document.createElement('input');
		submit_button.type = 'submit';
		submit_button.id = 'submit';
		if (client.session.in_game) {
			submit_button.value = 'Cannot change language while in game';
			submit_button.disabled = true;
		} else {
			submit_button.value = 'Save changes';
		}
		
		// create menu button
		this.menu_button = document.createElement('input');
		this.menu_button.type = 'button';
		this.menu_button.className = 'button';
		this.menu_button.addEventListener('click', application.showMenu.bind(application));
		this.menu_button.value = 'Return to menu';
		
		// create on click action that saves the settings and sends them to the server
		this.settings_form.addEventListener('submit', function(event) {
			event.preventDefault();
			if (this.language_select.selectedIndex !== -1) {
				var language = this.language_select.options[this.language_select.selectedIndex].value;
				this.changeSettings(language);
			}
		}.bind(this));
		
		this.settings_form.appendChild(username_field);
		this.settings_form.appendChild(language_select_wrapper);
		this.settings_form.appendChild(submit_button);
		
		container.appendChild(this.header);
		container.appendChild(this.settings_form);
		container.appendChild(this.menu_button);
	};
	
	this.destroy = function() {
		this.header.parentNode.removeChild(this.header);
		this.settings_form.parentNode.removeChild(this.settings_form);
		this.menu_button.parentNode.removeChild(this.menu_button);
		
		this.header = null;
		this.settings_form = null;
		this.language_select = null;
		this.menu_button = null;
	};
	
	this.addLanguageOption = function(name, value) {
		language_options.push([name, value]);
	};
	
	this.changeSettings = function(language) {
		// let the player know we are sending the new settings to the server which might take time
		application.setStatus('Configuring settings...');
		
		var data = {
			'session_id': client.session.id,
			'action': 'change_settings',
			'language': language,
		};
		client.sendRequest(data, function(response) {
			// save the newly created session locally
			client.session.language = language;
			client.saveSession();
			
			// switch to the menu
			application.showMenu();
			
			// remove the loading status again
			application.clearStatus();
		}.bind(this));
	};
}
