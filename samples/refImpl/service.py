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

from helper import reconstruct_url
from helper import respond401
from helper import respond305

class MyApp(object):
	"""
		This is a small service that prints 
		"Welcome {username} to OpenStack"
		Note that the username should be passed only from the Auth Component
	"""
	def __init__(self, *args, **kwargs):
		# The arguments are used if the App is running as a stand-alone service.
		self.proxy_host = kwargs.get('proxy_host')
		self.proxy_port = kwargs.get('proxy_port')
	
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

# For running this App as a stand-alone service
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) is 1:
        print '''
Usage: 
python service.py host=0.0.0.0 port=7070 proxy_host=0.0.0.0 proxy_port=8080
		'''
        sys.exit
    
    args = {'host':'0.0.0.0', 'port':7070, \
		'proxy_host':'0.0.0.0', 'proxy_port':8080}
    sys.argv.pop(0)
    for arg in sys.argv:
        if arg.find('=') is -1:
            print 'args must be in key=value format'
            sys.exit()
        args.__setitem__(*arg.split('='))
    
	from wsgiref.simple_server import make_server
	app = MyApp(\
		proxy_host=args['proxy_host'], proxy_port=args['proxy_port'])
	try:
		make_server(args['host'], args['port'], app).serve_forever()
	except KeyboardInterrupt:
		print '^C'
