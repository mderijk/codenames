
class Log:
	def __init__(self, filename, mode='a', encoding='utf-8', **kwargs):
		self.filename = filename
		self.mode = mode
		self.encoding = encoding
		self._open_kwargs = kwargs
	
	def open(self, *args, **kwargs):
		self._fd = open(self.filename, *args, **kwargs)
	
	def close(self):
		self._fd.close()
	
	def __enter__(self):
		self.open(mode=self.mode, encoding=self.encoding, **self._open_kwargs)
		return self
	
	def __exit__(self, exc_type, exc_value, traceback):
		self.close()
	
	def write(self, msg):
		self._fd.write(msg)
	
	def log(self, *args, **kwargs):
		print('LOG', *args, **kwargs, file=self)
	
	def warning(self, *args, **kwargs):
		print('WARNING', *args, **kwargs, file=self)
	
	def error(self, *args, **kwargs):
		print('ERROR', *args, **kwargs, file=self)
