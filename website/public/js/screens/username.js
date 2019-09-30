"use strict";

function Username(application, client) {
	this.username_form = null;
	this.username = null;
	this.language_select = null;
	this.consent = null;
	
	var language_options = [];
	
	this.build = function(container) {
		// create username form
		this.username_form = document.createElement('form');
		this.username_form.id = 'username-form';
		
		var fieldset = document.createElement('fieldset');
		var legend = document.createElement('legend');
		legend.textContent = 'Login';
		
		// create username field
		var username_wrapper = document.createElement('div');
		username_wrapper.textContent = 'Username: ';
		this.username = document.createElement('input');
		this.username.type = 'text';
		this.username.id = 'username';
		this.username.placeholder = 'choose a username';
		this.username.required = true;
		username_wrapper.appendChild(this.username);
		
		// create language select
		var language_select_wrapper = document.createElement('div');
		language_select_wrapper.textContent = 'Language: ';
		this.language_select = document.createElement('select');
		this.language_select.id = 'language';
		this.language_select.required = true;
		language_select_wrapper.appendChild(this.language_select);
		
		// add default option
		var select_language_option = document.createElement('option');
		select_language_option.hidden = true;
		select_language_option.disabled = true;
		select_language_option.selected = true;
		select_language_option.value = '';
		select_language_option.textContent = '-- select game language --';
		this.language_select.appendChild(select_language_option);
		
		// add options to language select
		language_options.forEach(function(language_option) {
			var name = language_option[0],
				value = language_option[1];
			
			var opt = document.createElement('option');
			opt.textContent = name;
			opt.value = value;
			this.language_select.appendChild(opt);
		}, this);
		
		// create consent "option"
		var consent_wrapper = document.createElement('div');
		this.consent = document.createElement('input');
		this.consent.type = 'checkbox';
		this.consent.required = true;
		var consent_text = document.createTextNode(' I agree that the anonymized data of the games I play can be used for research purposes.');
		consent_wrapper.appendChild(this.consent);
		consent_wrapper.appendChild(consent_text);
		
		// create submit button
		var submit_button = document.createElement('input');
		submit_button.type = 'submit';
		submit_button.id = 'submit';
		submit_button.value = 'Next';
		
		// create on click action that saves the username and sends it to the server
		this.username_form.addEventListener('submit', function(event) {
			event.preventDefault();
			if (this.consent.checked && this.username.value !== '' && this.language_select.selectedIndex !== -1) {
				var username = this.username.value;
				var language = this.language_select.options[this.language_select.selectedIndex].value;
				this.createNewSession(username, language);
			}
		}.bind(this));
		
		fieldset.appendChild(legend);
		fieldset.appendChild(username_wrapper);
		fieldset.appendChild(language_select_wrapper);
		fieldset.appendChild(consent_wrapper);
		fieldset.appendChild(submit_button);
		
		this.username_form.appendChild(fieldset);
		
		container.appendChild(this.username_form);
	};
	
	this.destroy = function() {
		this.username_form.parentNode.removeChild(this.username_form);
		
		this.username = null;
		this.language_select = null;
		this.username_form = null;
	};
	
	this.addLanguageOption = function(name, value) {
		language_options.push([name, value]);
	};
	
	this.createNewSession = function(username, language) {
		var data = {
			'action': 'new_session',
			'username': username,
			'language': language,
		};
		client.sendRequest(data, function(response) {
			// save the newly created session locally
			client.createSession(response.session_id, username, language);
			
			// switch to the menu
			application.showMenu();
		}.bind(this));
	};
}