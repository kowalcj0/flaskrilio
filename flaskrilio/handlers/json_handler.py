# -*- coding: utf-8 -*-
"""Simple wrapper around two libs: requests and json
"""
import json
import logging
import requests
from flaskrilio.helpers.common import setup_console_logger


class JsonHandler:
    """A simple wrapper for requests lib and json
    """

    def __init__(self, hostname=None, logger=None):
        """constructor

        Args:
            hostname (str): define the base hostname
                            can be overwritten on per GET/POST request basis
                            by providing a 'hostname' param
        """
        self.__hostname = hostname if hostname is not None else "http://127.0.0.0:5000"
        self.__log = setup_console_logger(logger, "JsonReqHandler")
        self.__log.debug("Json handler initialized for: %s" % self.__hostname)


    def get(self, hostname=None, endpoint=None):
        """Simple method to send a GET request expecting a JSON response"""
        if hostname is None:
            hostname = self.__hostname
        if endpoint is None:
            endpoint = "/"
        url = '%s%s' % (hostname, endpoint)
        headers = { "Accept": "application/json" }
        return requests.get(url, headers=headers)


    def post(self, hostname=None, endpoint=None, data=None):
        """
        Simple method to send a POST request with an optional JSON payload
        and that expects a JSON response
        """
        if hostname is None:
            hostname = self.__hostname
        if endpoint is None:
            endpoint = "/"
        url = '%s%s' % (hostname, endpoint)
        headers = { "Content-Type": "application/json", \
                    "Accept": "application/json" }
        return requests.post(url, data=data, headers=headers)


if '__main__' == __name__:
    __package__ = "flaskrilio.handlers"
    _cc = JsonHandler("http://callconnect.dev.hibulabs.co.uk")
    _id = _cc.post(endpoint="/api/id", data="{}")
    print _id.status_code

    _tcc = JsonHandler("http://ip.jsontest.com")
    _ip = _tcc.get()
    assert _ip.json()['ip'] is not None
    print "My public IP is: %s" % _ip.json()['ip']
