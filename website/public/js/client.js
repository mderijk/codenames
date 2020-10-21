"use strict";

function Client() {
	this.request_lock = false;
	this.session = JSON.parse(localStorage.getItem('session')); // id, username, in_game
	this.version = '1.5.4';
	
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
				this.onError(response);
			} else if (callback !== undefined) {
				callback(response);
			}
		}.bind(this));
	};
	
	this.onError = function(response) {
		console.log('ERROR:', response.error);
	}
	
	this.createSession = function(id, username, language) {
		this.session = {}
		this.session.version = this.version;
		this.session.id = id;
		this.session.username = username;
		this.session.language = language;
		this.session.in_game = false;
		this.session.timed_out = false;
		
		this.saveSession();
	};
	
	this.saveSession = function() {
		// save the session in local storage so that it persists after page refresh
		localStorage.setItem('session', JSON.stringify(this.session));
	}
	
	this.deleteSession = function() {
		// prevent the session from persisting after page refresh
		localStorage.removeItem('session');
	}
}
