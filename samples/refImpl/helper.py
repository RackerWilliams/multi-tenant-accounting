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

from httplib import HTTPConnection
from urlparse import urlparse

class DummyApp(object):
	"""
		This is a very simple App that acts as a proxy. It is used only in
		the Deployment Strategy where the Auth Component is deployed in a 
		separate end point.

		This App passes the request through to the Service and passes back
		the response to the Auth Component.
	"""
	def __init__(self, *args, **kwargs):
		self.app_host = kwargs.get('app_host')
		self.app_port = kwargs.get('app_port')
	
	ConnectionClass = HTTPConnection

	def __call__(self, environ, start_response):
		url = urlparse(reconstruct_url(environ, self.app_host, self.app_port))
		try:
			connection = self.ConnectionClass(url.netloc)
		except Exception:
			start_response("501 Gateway Error", [('Content-Type', 'text/html')])
			return ['Could Not Connect']

		# Get the request's body
		request_body = None
		if environ.get('CONTENT_LENGTH'):
			length = int(environ['CONTENT_LENGTH'])
			request_body = environ['wsgi.input'].read(length)
			
		# Get the request's headers
		headers = {}
		for key in environ.keys():
			# From PEP 3333 Keys that start with HTTP_ are all headers
			if key.startswith('HTTP_'):
				key = key.replace('HTTP_', '', 1).lower().replace('_', '-')
				headers[key] = environ[key]

		# content-type special case because it doesn't start with 'HTTP_'
		if environ.get('CONTENT_TYPE'):
			headers['content-type'] = environ['CONTENT_TYPE']

		# Pass the request to the Service
		try:
			connection.request(\
				environ['REQUEST_METHOD'], url.geturl(), \
					body=request_body, headers=headers)
		except:
			start_response("501 Gateway Error", [('Content-Type', 'text/html')])
			return ['Could not connect']

		# Get the response from the Service and pass it back to the Auth Comp
		response = connection.getresponse()
		if str(response.status).startswith('401'):
			return respond500(environ, start_response)	
		else:
			start_response(str(response.status) + ' ' + response.reason, \
				response.getheaders())
			return [response.read(response.length)]

def reconstruct_url(environ, host, port):
	url = environ['wsgi.url_scheme'] + '://'
	url = url + host + ':' + str(port)
	url += environ['SCRIPT_NAME']
	url += environ['PATH_INFO']
	if environ.get('QUERY_STRING'):
		url += '?' + environ['QUERY_STRING']

	environ['reconstructed_url'] = url
	return url

def respond401(environ, start_response, authenticate=True):
	response_status = '401 Authorization Required'
	response_headers = [('content-type', 'text/html')]
	if authenticate:
		response_headers.append(('WWW-AUTHENTICATE', 'Basic realm="secure"'))
	response_body = """
	<html>
		<head><title>Authentication Required</title></head>
		<body>
			<h1>Authentication Required</h1>
			If you can't get in, then stay out.
		</body>
	</html>
	"""
	start_response(response_status, response_headers)
	return [response_body]

def respond305(environ, start_response, location):
	response_status = '305 Use Proxy'
	response_headers = [('content-type', 'text/html'), \
		('LOCATION', location)]
	response_body = """ Use Proxy """
	start_response(response_status, response_headers)
	return [response_body]

def respond500(environ, start_response):
	response_status = '500 Internal Server Error'
	response_headers = [('content-type', 'text/html')]
	response_body = """ Internal Server Error """
	start_response(response_status, response_headers)
	return [response_body]

