# Pymapquest
# Copyright 2011 Omniar, Inc
# See LICENSE for details.

"""
Pymapquest MapQuest API library
"""
__version__ = '0.1.0'
__author__ = 'Omniar'
__license__ = 'MIT'

from mapquest.error import MapQuestError
from mapquest.api import OpenAPI, LicensedAPI

def debug(enable=True, level=1):
    
    import httplib
    httplib.HTTPConnection.debuglevel = level