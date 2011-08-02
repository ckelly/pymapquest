# Pymapquest
# Copyright 2011 Omniar, Inc
# See LICENSE for details.

class MapQuestError(Exception):
    """Mapquest exception"""

    def __init__(self, reason, response=None):
        self.reason = unicode(reason)
        self.response = response

    def __str__(self):
        return self.reason