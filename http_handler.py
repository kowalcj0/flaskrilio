# -*- coding: utf-8 -*-
"""Simple urllib2 and json wrapper
"""
import json
import urllib2
import logging

class HttpHandler:
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
        self.__log = logger if logger is not None else logging.getLogger('HttpHandler')
        self.__log.debug("HTTP handler initialized for: %s" % self.__hostname)


    def get(self, hostname=None, endpoint=None):
        """
        Simple method to send a GET request

        Return:
            http://docs.python.org/2/library/urllib2.html#urllib2.urlopen
        """
        if hostname is None:
            hostname = self.__hostname
        if endpoint is None:
            endpoint = "/"
        req = urllib2.Request(url='%s%s' % (hostname, endpoint))
        #req.add_header("Content-Type", "application/json")
        #req.add_header("Accept", "application/json")
        try:
            return urllib2.urlopen(req)
        except IOError as e:
            self.__log.error(e)


    def post(self, hostname=None, endpoint=None, data=None):
        """
        Simple method to send a POST request with an optional payload

        Return:
            http://docs.python.org/2/library/urllib2.html#urllib2.urlopen
        """
        if hostname is None:
            hostname = self.__hostname
        if endpoint is None:
            endpoint = "/"
        if data:
            req = urllib2.Request(url='%s%s' % (hostname, endpoint), data=data)
        else:
            req = urllib2.Request(url='%s%s' % (hostname, endpoint))
        #req.add_header("Content-Type", "application/json")
        #req.add_header("Accept", "application/json")
        try:
            return urllib2.urlopen(req)
        except IOError as e:
            self.__log.error(e)


if '__main__' == __name__:
    hh = HttpHandler("http://callconnect.poc.hibulabs.co.uk")
    home = hh.get(endpoint="/").read(100)
    print home
    """
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
    """
