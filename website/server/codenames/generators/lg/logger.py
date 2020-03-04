
import os

from . import log

class Logger:
	def __init__(self, log_directory):
		self.log_directory = log_directory
	
	def openLog(self, log_name):
		log_filepath = os.path.join(self.log_directory, log_name + '.log')
		self.log = log.Log(log_filepath)
		return self.log
