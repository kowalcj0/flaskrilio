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
        self.logger.setLevel(logging.INFO)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        # create formatter and add it to the handlers
        formatter=logging.Formatter('[%(asctime)s] [%(levelname)s]: %(message)s', "%a %Y-%m-%d %H:%M:%S %z")
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)


    def get_new_uuid(self):
        uuid =  self.__get_json__("/api/id", "{}")["id"]
        self.logger.debug("Got new UUID: %s" % uuid)
        return uuid

    def get_redirect_to(self, uuid, number):
        payload = {
                    "id": uuid,
                    "redirectTo": number
                }
        # use json.dumps to convert payload tupple into a string
        redir = self.__get_json__("/api/callers",
                                  json.dumps(payload))
        self.logger.debug("Got new redirect_to:\n%s" % redir)
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
    cc = CallConnectHandler("http://callconnect.poc.hibulabs.co.uk")
    id = cc.get_new_uuid()
    redir = cc.get_redirect_to(id, "+447402028595")
    print id
    print redir

