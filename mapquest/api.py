# Pymapquest
# Copyright 2011 Omniar, Inc
# See LICENSE for details.

import os

from mapquest.binder import bind_api
from mapquest.parsers import JSONParser
from mapquest.utils import import_simplejson
json = import_simplejson()


class OpenAPI(object):
    '''Mapquest Open API'''
    
    def __init__(self,
            host='open.mapquestapi.com',
            retry_count=0, retry_errors=None, retry_delay=0, parser=None):
            # short circuit this for now, change if we need Oauth, etc later
        self.host = host
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.retry_errors = retry_errors
        self.parser = parser or JSONParser()
        # not used in open calls, but kept for consistency
        self.key = None
        
    # Open MapQuest method calls
    # nominatim
    def nominatim(self, version='v1', format='json', *args, **kargs):
        return bind_api(
        path = '/nominatim/{version}/search',
        allowed_param = ['json_callback', 'q', 'addressdetails',
         'limit', 'countrycodes', 'viewbox', 'exclude_place_ids', 
         'bounded', 'routewidth', 'osm_type', 'osm_id', 'format']
         )(self, version=version, format=format, *args, **kargs)

    # directions
    # from is a reserved word, but we need to pass it in. This should do it
    def directions(self, start, end, version='v0', format='json', *args, **kargs):
        #remap start and end to from/ to for api call
        kargs['from'] = start
        kargs['to'] = end
        
        return bind_api(
        path = '/directions/{version}/route',
        allowed_param = ['inFormat', 'json', 'xml', 'outFormat',
         'callback', 'unit', 'routeType', 'narrativeType', 
         'enhancedNarrative', 'maxLinkId', 'locale', 'avoids',
         'mustAvoidLinkIds', 'tryAvoidLinkIds', 'stateBoundaryDisplay',
         'destinationManeuverDisplay', 'shapeFormat', 'generalize', 
         'cyclingRoadFactor', 'roadGradeStrategy', 'drivingStyle', 
         'highwayEfficiency', 'sessionId', 'mapState', 'format']
    )(self, version=version, format=format, *args, **kargs)


class LicensedAPI(object):
    '''Mapquest Open API'''

    def __init__(self, key,
            host='www.mapquestapi.com',
            retry_count=0, retry_errors=None, retry_delay=0, parser=None):
            # short circuit this for now, change if we need Oauth, etc later
        self.host = host
        self.key = key
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.retry_errors = retry_errors
        self.parser = parser or JSONParser()

    # directions
    # from is a reserved word, but we need to pass it in. This should do it
    def directions(self, start, end, version='v1', format='json', *args, **kargs):
        #remap start and end to from/ to for api call
        kargs['from'] = start
        kargs['to'] = end

        return bind_api(
        path = '/directions/{version}/route',
        allowed_param = ['ambiguities', 'inFormat', 'json', 'xml', 'outFormat',
         'callback', 'unit', 'routeType', 'avoidTimedConditions', 'doReverseGeoCode', 
         'narrativeType', 'enhancedNarrative', 'maxLinkId', 'locale', 'avoids',
         'mustAvoidLinkIds', 'tryAvoidLinkIds', 'stateBoundaryDisplay',
         'countryBoundaryDisplay', 'sideOfStreetDisplay',
         'destinationManeuverDisplay', 'shapeFormat', 'generalize', 
         'drivingStyle', 'highwayEfficiency', 'sessionId', 'mapState', 'format', 'key']
    )(self, version=version, format=format, *args, **kargs)


