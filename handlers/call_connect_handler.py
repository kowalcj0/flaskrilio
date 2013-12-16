# -*- coding: utf-8 -*-
import json
import urllib2
import logging
from handlers.json_handler import JsonHandler
from handlers.http_handler import HttpHandler
from helpers import setup_console_logger

class CallConnectHandler:
    """A simple wrapper for Call Connect endpoints"""

    def __init__(self, hostname=None, logger=None):
        self.__hostname = hostname if hostname is not None else "http://127.0.0.0:5000"
        self.__log = setup_console_logger(logger, "CallConnectHandler")
        self.__jh = JsonHandler(hostname=self.__hostname, logger=self.__log)
        self.__hh = HttpHandler(hostname=self.__hostname, logger=self.__log)
        self.__log.debug("CallConnect handler initialized for: %s" % self.__hostname)


    def get_new_caller_id(self):
        caller_id =  self.__jh.post(endpoint="/api/id", data="{}")["id"]
        self.__log.debug("Received new Caller ID: %s" % caller_id)
        return caller_id


    def get_redirect_to(self, caller_id, number):
        payload = {
                    "id": caller_id,
                    "redirectTo": number
                }
        # use json.dumps to convert payload tupple into a string
        redir = self.__jh.post(endpoint="/api/callers",
                               data=json.dumps(payload))
        self.__log.debug("Received new redirect_to: %s" % redir)
        return redir


    def delete_caller_id(self, callerId):
        self.__log.debug("Deleting callerId: %s" % callerId)
        return self.__hh.delete(endpoint="/api/callers/%s" % callerId)


    def get_callers_details(self, callerId):
        self.__log.debug("Getting details for callerId: %s" % callerId)
        return self.__jh.get(endpoint="/api/callers/%s" % callerId)


    def get_number_pool(self):
        pool = self.__jh.get(endpoint="/api/pool")
        self.__log.debug("Got Number pool: %s" % pool)
        return pool


if '__main__' == __name__:
    _cc = CallConnectHandler("http://callconnect.dev.hibulabs.co.uk")
    _id = _cc.get_new_caller_id()
    _redir = _cc.get_redirect_to(_id, "+447402028595")
    assert _id is not None
    assert _redir is not None
    print _id
    print _redir

