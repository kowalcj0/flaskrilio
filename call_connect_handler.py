# -*- coding: utf-8 -*-
import json
import urllib2
import logging

class CallConnectHandler:
    """A simple wrapper for Call Connect endpoints"""

    def __init__(self, hostname):
        self.__hostname=hostname
        # get logger
        self.logger = logging.getLogger('twilio-ec2.CallConnectHandler')

    def get_new_caller_id(self):
        caller_id =  self.__get_json__("/api/id", "{}")["id"]
        #self.logger.debug("Got new Caller ID: %s" % caller_id)
        return caller_id

    def get_redirect_to(self, caller_id, number):
        payload = {
                    "id": caller_id,
                    "redirectTo": number
                }
        # use json.dumps to convert payload tupple into a string
        redir = self.__get_json__("/api/callers",
                                  json.dumps(payload))
        #self.logger.debug("Got new redirect_to:%s" % redir)
        return redir

    def __get_json__(self, endpoint, data):
        """Simple method to send and retrieve a json requests"""
        req = urllib2.Request(url='%s%s' % (self.__hostname, endpoint),
                              data=data)
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "application/json")
        try:
            return json.load(urllib2.urlopen(req))
        except IOError as e:
            self.logger.error(e)



if '__main__' == __name__:
    _cc = CallConnectHandler("http://callconnect.poc.hibulabs.co.uk")
    _id = _cc.get_new_caller_id()
    _redir = _cc.get_redirect_to(_id, "+447402028595")
    print _id
    print _redir

