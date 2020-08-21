
from multiprocessing.connection import Listener
import os
import socket
import sys

from .protocol import Protocol

# Connector class
class Connector:
	def __init__(self, socket, logs_directory, protocol=None):
		self.socket = socket
		self.logfile = os.path.join(logs_directory, 'connector.log')
		if protocol is None:
			protocol = Protocol()
		self.protocol = protocol
		
		# create log directory
		logdir = os.path.dirname(self.logfile)
		os.makedirs(logdir, exist_ok=True)
	
	def __enter__(self):
		# in this context all errors are written to a log file
		self._sys_stderr = sys.stderr
		sys.stderr = open(self.logfile, 'a')
		
		# establish communications
		self.listener = Listener(self.socket)
		
		return self
	
	def __exit__(self, exc_type, exc_value, traceback):
		self.listener.close()
		
		if exc_type == exc_value == traceback == None: # if there were no errors, reinstate the old stderr
			sys.stderr.close()
			sys.stderr = self._sys_stderr
	
	def send(self, data):
		self.connection.send(data)
		self.connection.close()
	
	def error(self, *errors):
		response = self.protocol.error(*errors)
		self.send(response)
	
	def receive(self):
		while True:
			self.connection = self.listener.accept()
			response = self.connection.recv()
			
			errors = []
			for attribute in self.protocol.required:
				if attribute not in response:
					errors.append(self.protocol.required[attribute])
			if not errors:
				break
			self.error(*errors)
		
		return response
