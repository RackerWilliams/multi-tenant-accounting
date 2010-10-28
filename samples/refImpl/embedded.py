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

from wsgiref.simple_server import make_server
from authcomp import OpenStackBasicAuthMiddleware
from service import MyApp

if __name__ == '__main__':
	app = MyApp()
	authComp = OpenStackBasicAuthMiddleware(app)
	try:
		make_server('0.0.0.0', 8080, authComp).serve_forever()
	except KeyboardInterrupt:
		print '^C'
