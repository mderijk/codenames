
class Module:
	def __init__(self, config, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.config = config
	
	@classmethod
	def error(cls, message):
		return {
			'status': 'error',
			'error': message,
		}
	
	@classmethod
	def missing(cls, attribute):
		return cls.error('Empty or missing \'{attribute}\''.format(attribute=attribute))
	
	@staticmethod
	def _require(request, *required_args):
		for arg in required_args:
			if not (arg in request and request[arg] != ''):
				return False
		
		return True
