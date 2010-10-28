	def __call__(self, environ, start_response):
		if not environ.get("HTTP_AUTHORIZATION"): 
			# The user needs to be authenticated. We reject the request and 
			# return 401 before the Service (MyApp) receives the request. 
			return respond401(environ, start_response)
		else:
			# Let's authenticate the user against the users.ini file.
			import base64
			auth_header = environ['HTTP_AUTHORIZATION']
			auth_type, encoded_creds = auth_header.split(None, 1)
			username, password  = base64.b64decode(encoded_creds).split(':', 1)
			if self.validateCreds(username, password):
				# The Auth Component has to authenticate itself to the service.
				environ['HTTP_AUTHORIZATION'] = "Basic dTpw"
				# The Auth Component passes the username to the Service
				environ['HTTP_X_AUTHORIZATION'] = "Proxy %s" % username
				return self.app(environ, start_response)
			else:
				return respond401(environ, start_response)
