	def __call__(self, environ, start_response):
		# Make sure the request comes from Auth Component
		if not environ.get("HTTP_AUTHORIZATION"):
			return respond305(environ, start_response, \
				reconstruct_url(environ, self.proxy_host, self.proxy_port))

		# Now let's authenticate the Auth Component itself
		import base64
		auth_header = environ['HTTP_AUTHORIZATION']
		auth_type, encoded_creds = auth_header.split(None, 1)
		# Not very secure, but you get the picture
		if str(encoded_creds) != "dTpw":
			print encoded_creds
			return respond401(environ, start_response, False)
		elif not environ.get("HTTP_X_AUTHORIZATION"): 
			return respond401(environ, start_response)
		else:
			# Here is where the service processes the request
			response_headers = [('content-type', 'text/html')]
			response_status = '200 OK'
			user_auth_header = environ["HTTP_X_AUTHORIZATION"]
			auth_type, username = user_auth_header.split(None, 1)
			response_body = "Welcome %s to OpenStack <BR>" % username
			start_response(response_status, response_headers)
			return [response_body]
