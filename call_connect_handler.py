# -*- coding: utf-8 -*-
import json
import urllib2
import logging
from json_handler import JsonHandler

class CallConnectHandler:
    """A simple wrapper for Call Connect endpoints"""

    def __init__(self, hostname):
        self.__hostname=hostname
        self.jh = JsonHandler(self.__hostname)
        # get logger
        self.logger = logging.getLogger('twilio-ec2.CallConnectHandler')

    def get_new_caller_id(self):
        caller_id =  self.jh.post(endpoint="/api/id", data="{}")["id"]
        #self.logger.debug("Got new Caller ID: %s" % caller_id)
        return caller_id

    def get_redirect_to(self, caller_id, number):
        payload = {
                    "id": caller_id,
                    "redirectTo": number
                }
        # use json.dumps to convert payload tupple into a string
        redir = self.jh.post(endpoint="/api/callers",
                             data=json.dumps(payload))
        #self.logger.debug("Got new redirect_to:%s" % redir)
        return redir


if '__main__' == __name__:
    _cc = CallConnectHandler("http://callconnect.poc.hibulabs.co.uk")
    _id = _cc.get_new_caller_id()
    _redir = _cc.get_redirect_to(_id, "+447402028595")
    assert _id is not None
    assert _redir is not None
    print _id
    print _redir

