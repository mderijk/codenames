"use strict";

function Wizard(container) {
	this.screen = null;
	this.screens = {};
	
	this.add = function(name, screen) {
		this.screens[name] = screen;
	};
	
	this.addElement = function(elem) {
		container.appendChild(elem);
	};
	
	this.show = function(name) {
		// cleanup old screen
		if (this.screen !== null) {
			this.screen.destroy();
		}
		
		// build new screen
		this.screen = this.screens[name];
		this.screen.build(container);
	};
	
	this.emptyContainer = function() {
		while (container.lastChild) {
			container.removeChild(this.container.lastChild);
		}
	};
}
