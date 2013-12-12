# -*- coding: utf-8 -*-
"""Simple urllib2 and json wrapper
"""
import json
import urllib2
import logging

class JsonHandler:
    """A simple wrapper for urllib2 and json
    """

    def __init__(self, hostname=None, logger=None):
        """constructor

        Args:
            hostname (str): define the base hostname
                            can be overwritten on per GET/POST request basis
                            by providing a 'hostname' param
        """
        self.__hostname = hostname if hostname is not None else "http://127.0.0.0:5000"
        self.__log = logger if logger is not None else logging.getLogger('twilio-ec2.JsonHandler')
        self.__log.debug("Json handler initialized for: %s" % self.__hostname)


    def get(self, hostname=None, endpoint=None):
        """Simple method to send a GET request expecting a JSON response"""
        if hostname is None:
            hostname = self.__hostname
        if endpoint is None:
            endpoint = "/"
        req = urllib2.Request(url='%s%s' % (hostname, endpoint))
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "application/json")
        try:
            return json.load(urllib2.urlopen(req))
        except IOError as e:
            self.__log.error(e)


    def post(self, hostname=None, endpoint=None, data=None):
        """
        Simple method to send a POST request with an optional JSON payload
        and that expects a JSON response
        """
        if hostname is None:
            hostname = self.__hostname
        if endpoint is None:
            endpoint = "/"
        if data:
            req = urllib2.Request(url='%s%s' % (hostname, endpoint), data=data)
        else:
            req = urllib2.Request(url='%s%s' % (hostname, endpoint))
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "application/json")
        try:
            return json.load(urllib2.urlopen(req))
        except IOError as e:
            self.__log.error(e)


if '__main__' == __name__:
    _cc = JsonHandler("http://callconnect.poc.hibulabs.co.uk")
    _id = _cc.post(endpoint="/api/id", data="{}")['id']
    number = "+447402028595"
    payload = {
                "id": _id,
                "redirectTo": number
               }
    # use json.dumps to convert payload tupple into a string
    _redir = _cc.post(endpoint="/api/callers",
                      data=json.dumps(payload))

    assert _id is not None
    assert _redir is not None
    print "My CallConnect new callerID is: %s" % _id
    print "Here's my redir response: %s" % _redir

    _tcc = JsonHandler("http://ip.jsontest.com")
    _ip = _tcc.get()
    assert _ip["ip"] is not None
    print "My public IP is: %s" % _ip["ip"]

