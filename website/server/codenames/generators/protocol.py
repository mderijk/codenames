
# Protocol
# descriptive model for errors
class Protocol:
	def __init__(self, required=None, default_error='An unexpected error has occured.'):
		if required is None:
			required = {}
		self.required = required
		
		self.default_error = default_error
	
	def error(self, *errors):
		if not errors:
			errors = self.default_error
		response = {}
		response['status'] = 'error'
		response['error'] = errors
		return response
