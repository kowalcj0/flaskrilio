# -*- coding: utf-8 -*-
"""Simple urllib2 and json wrapper
"""
import json
import urllib2
import logging
from helpers import setup_console_logger

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
        self.__log = setup_console_logger(logger, "HttpHandler")
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


    def delete(self, hostname=None, endpoint=None):
        """
        Simple method to send a DELETE request

        Return:
            http://docs.python.org/2/library/urllib2.html#urllib2.urlopen
        """
        if hostname is None:
            hostname = self.__hostname
        if endpoint is None:
            endpoint = "/"
        url = '%s%s' % (hostname, endpoint)
        req = RequestWithMethod(url=url, method='DELETE')
        try:
            self.__log.info("Deleting resource: %s" % url)
            return urllib2.urlopen(req).getcode()
        except IOError as e:
            self.__log.error(e)



class RequestWithMethod(urllib2.Request):
    """
    Workaround for using DELETE with urllib2
    http://abhinandh.com/12/20/2010/making-http-delete-with-urllib2.html
    """
    def __init__(self, url, method, data=None, headers={},\
        origin_req_host=None, unverifiable=False):
        self._method = method
        urllib2.Request.__init__(self, url, data, headers,\
                 origin_req_host, unverifiable)

    def get_method(self):
        if self._method:
            return self._method
        else:
            return urllib2.Request.get_method(self)



if '__main__' == __name__:
    hh = HttpHandler("http://127.0.0.1:5000")
    home = hh.get(endpoint="/").read(100)
    print home
    delete = hh.delete()
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
