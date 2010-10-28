# Author: Khaled Hussein <khaled.hussein@rackspace.com>
#
# Copyright (c) 2010 OpenStack, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from helper import respond401

class OpenStackBasicAuthMiddleware(object):
	"""
		This is a sample Authentication Middleware that implements 
		Basic Authentication and uses a file for storage of user credentials 
	"""
	def __init__(self, app):
		self.app = app
	
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


	def validateCreds(self, username, password):
		#check in the ini file.
		import ConfigParser, os
		usersConfig = ConfigParser.ConfigParser()
		usersConfig.readfp(open('users.ini'))
		for un, pwd in usersConfig.items('users'):
			if username == un and password == pwd:
				return True

		return False

# For running this Auth Comp as a stand-alone HTTP Proxy
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) is 1:
        print '''
Usage: python authcomp.py host=0.0.0.0 port=8080 app_host=0.0.0.0 app_port=7070
		'''
        sys.exit
    
    args = {'host':'0.0.0.0', 'port':8080, \
		'app_host':'0.0.0.0', 'app_port':7070}
    sys.argv.pop(0)
    for arg in sys.argv:
        if arg.find('=') is -1:
            print 'args must be in key=value format'
            sys.exit()
        args.__setitem__(*arg.split('='))
    
	from wsgiref.simple_server import make_server
	from authcomp import OpenStackBasicAuthMiddleware
	from helper import DummyApp
	app = DummyApp(app_host=args['app_host'], app_port=args['app_port'])
	authComp = OpenStackBasicAuthMiddleware(app)
	try:
		make_server(args['host'], int(args['port']), authComp).serve_forever()
	except KeyboardInterrupt:
		print '^C'
