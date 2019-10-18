"use strict";

function Client() {
	this.request_lock = false;
	this.session = JSON.parse(localStorage.getItem('session')); // id, username, in_game
	
	this.sendAjaxRequest = function(url, data, callback) {
		if (this.request_lock === false) {
			this.request_lock = true;
			var json = JSON.stringify(data);
			var request = new XMLHttpRequest();
			request.onload = function(e) {
				if (callback !== undefined) {
					var response = JSON.parse(this.responseText);
					callback(response);
				}
			}
			request.open('POST', url, true);
			request.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
			request.send(json);
		}
	};
	
	this.sendRequest = function(data, callback) {
		this.sendAjaxRequest('client.php', data, function(response) {
			this.request_lock = false;
			if (response.status === 'error') {
				this.handleError(response);
			} else if (callback !== undefined) {
				callback(response);
			}
		}.bind(this));
	};
	
	this.handleError = function(response) {
		console.log('ERROR:', response.error);
		
		if (response.error === 'Game has already ended') {
			console.log('Attempting fix...');
			this.session.in_game = false;
			this.saveSession();
			console.log('Refreshing page...');
			console.log('Please report the issue if this did not solve it.');
			window.location.reload();
		}
	}
	
	this.createSession = function(id, username, language) {
		this.session = {}
		this.session.version = '1.2';
		this.session.id = id;
		this.session.username = username;
		this.session.language = language;
		this.session.in_game = false;
		
		this.saveSession();
	};
	
	this.saveSession = function() {
		localStorage.setItem('session', JSON.stringify(this.session));
	}
}
