# Pymapquest
# Copyright 2011 Omniar, Inc
# See LICENSE for details.

from mapquest.utils import import_simplejson
from mapquest.error import MapQuestError

class Parser(object):

    def parse(self, method, payload):
        """
        Parse the response payload and return the result.
        Returns a tuple that contains the result data and the cursors
        (or None if not present).
        """
        raise NotImplementedError

    def parse_error(self, payload):
        """
        Parse the error message from payload.
        If unable to parse the message, throw an exception
        and default error message will be used.
        """
        raise NotImplementedError
        

class JSONParser(Parser):

    payload_format = 'json'

    def __init__(self):
        self.json_lib = import_simplejson()

    def parse(self, method, payload):        
        try:
            json = self.json_lib.loads(payload)
        except Exception, e:
            raise MapQuestError('Failed to parse JSON payload: %s' % e)

        return json

    def parse_error(self, payload):
        error = self.json_lib.loads(payload)
        # if error.has_key('error-reason'):
        #             return error['error-reason']
        #         else:
        #             return error['error-code']