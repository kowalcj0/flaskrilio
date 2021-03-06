# -*- coding: utf-8 -*-
import json
import logging
from handlers.json_handler import JsonHandler
from handlers.http_handler import HttpHandler
from helpers.common import setup_console_logger


class FlaskrilioHandler:
    """A simple wrapper for the local Flaskrilio service"""


    def __init__(self, hostname=None, logger=None):
        self.__hostname = hostname if hostname is not None else "http://127.0.0.0:5000"
        self.__log = setup_console_logger(logger, "FlaskrilioHandler")
        self.__jh = JsonHandler(hostname=self.__hostname, logger=self.__log)
        self.__hh = HttpHandler(hostname=self.__hostname, logger=self.__log)
        self.__log.debug("Flaskrilio handler initialized for: %s" % self.__hostname)


    def get_home(self):
        return self.__jh.get(endpoint="/")


    def get_twiml(self, ctx):
        self.__log.debug("Getting TwilML for an endpoint: %s" % ctx)
        return self.__hh.get(endpoint=ctx)


    def get_calls(self):
        calls =  self.__jh.get(endpoint="/calls")
        self.__log.debug("Got calls: %s" % calls)
        if calls is None:
            return []
        else:
            return calls


if '__main__' == __name__:
    __package__ = "flaskrilio.handlers"
    f = FlaskrilioHandler()
    calls = f.get_calls()
    print calls
    assert calls is not None, "Error: %s " % calls
