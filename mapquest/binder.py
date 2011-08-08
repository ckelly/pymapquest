# Pymapquest
# Copyright 2011 Omniar, Inc
# See LICENSE for details.

import httplib
import urllib
import time
import re

from mapquest.error import MapQuestError
from mapquest.utils import convert_to_utf8_str

re_path_template = re.compile('{\w+}')

def bind_api(**config):

    class APIMethod(object):

        path = config['path']
        allowed_param = config.get('allowed_param', [])
        method = config.get('method', 'GET')

        def __init__(self, api, args, kargs):

            self.api = api
            self.parser = kargs.pop('parser', self.api.parser)
            
            #self.post_data = kargs.pop('post_data', None)
            self.retry_count = kargs.pop('retry_count', api.retry_count)
            self.retry_delay = kargs.pop('retry_delay', api.retry_delay)
            self.retry_errors = kargs.pop('retry_errors', api.retry_errors)
            self.headers = kargs.pop('headers', {})
            self.post_data = kargs.pop('post_data', {})
            
            self.build_parameters(args, kargs)

            # Perform any path variable substitution
            self.build_path()
            self.scheme = 'http://'    
            self.host = api.host

        def build_parameters(self, args, kargs):
            self.parameters = {}
            for idx, arg in enumerate(args):
                if arg is None:
                    continue

                try:
                    self.parameters[self.allowed_param[idx]] = convert_to_utf8_str(arg)
                except IndexError:
                    raise MapQuestError('Too many parameters supplied!')

            for k, arg in kargs.items():
                if arg is None:
                    continue
                if k in self.parameters:
                    raise MapQuestError('Multiple values for parameter %s supplied!' % k)

                self.parameters[k] = convert_to_utf8_str(arg)

        def build_path(self):
            for variable in re_path_template.findall(self.path):
                name = variable.strip('{}')
                try:
                    value = urllib.quote(self.parameters[name])
                except KeyError:
                    raise MapQuestError('No parameter value found for path variable: %s' % name)
                del self.parameters[name]

                self.path = self.path.replace(variable, value)

        def execute(self):
            # Build the request URL
            url = self.path
                
            if len(self.parameters):
                url = '%s?%s' % (url, urllib.urlencode(self.parameters))

            # Continue attempting request until successful
            # or maximum number of retries is reached.
            retries_performed = 0
            while retries_performed < self.retry_count + 1:
                # Open connection
                # FIXME: add timeout
                conn = httplib.HTTPConnection(self.host)

                # Execute request
                try:
                    conn.request(self.method, url, headers=self.headers, body=self.post_data)
                    resp = conn.getresponse()
                except Exception, e:
                    raise MapQuestError('Failed to send request: %s' % e)

                # Exit request loop if non-retry error code
                if self.retry_errors:
                    if resp.status not in self.retry_errors: break
                else:
                    if resp.status == 200: break

                # Sleep before retrying request again
                time.sleep(self.retry_delay)
                retries_performed += 1

            # If an error was returned, throw an exception
            self.api.last_response = resp
            if resp.status != 200:
                try:
                    error_msg = self.parser.parse_error(resp.read())
                except Exception:
                    error_msg = "MapQuest error response: status code = %s" % resp.status
                raise MapQuestError(error_msg, resp)

            # Parse the response payload
            result = self.parser.parse(self, resp.read())

            conn.close()
            
            return result


    def _call(api, *args, **kargs):

        method = APIMethod(api, args, kargs)
        return method.execute()
        
    return _call