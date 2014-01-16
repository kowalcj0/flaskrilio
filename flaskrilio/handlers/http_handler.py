# -*- coding: utf-8 -*-
"""Simple wrapper around two libs: requests and json
"""
import json
import requests
import logging
from flaskrilio.helpers.common import setup_console_logger

class HttpHandler:
    """A simple wrapper around requests and json
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
            http://docs.python-requests.org/en/latest/api/#requests.request
        """
        if hostname is None:
            hostname = self.__hostname
        if endpoint is None:
            endpoint = "/"
        return requests.get(url='%s%s' % (hostname, endpoint))


    def post(self, hostname=None, endpoint=None, data=None, headers=None):
        """
        Simple method to send a POST request with an optional payload

        Return:
            http://docs.python-requests.org/en/latest/api/#requests.request
        """
        if hostname is None:
            hostname = self.__hostname
        if endpoint is None:
            endpoint = "/"
        url='%s%s' % (hostname, endpoint)
        if data:
            if headers:
                return requests.post(url=url, data=data, headers=headers)
            else:
                return requests.post(url=url, data=data)
        else:
            if headers:
                return requests.post(url=url, headers=headers)
            else:
                return requests.post(url=url)


    def delete(self, hostname=None, endpoint=None):
        """
        Simple method to send a DELETE request

        Return:
            http://docs.python-requests.org/en/latest/api/#requests.request
        """
        if hostname is None:
            hostname = self.__hostname
        if endpoint is None:
            endpoint = "/"
        url = '%s%s' % (hostname, endpoint)
        return requests.delete(url=url)


if '__main__' == __name__:
    __package__ = "flaskrilio.handlers"
    hh = HttpHandler("http://127.0.0.1:5000")
    home = hh.get(endpoint="/")
    print home
    delete = hh.delete()
    print delete
