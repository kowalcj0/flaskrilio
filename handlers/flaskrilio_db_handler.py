# -*- coding: utf-8 -*-
import logging
from helpers import setup_console_logger
import sqlite3
from flaskrilio import connect_db


class FlaskrilioDBHandler:
    """A simple wrapper for the local Flaskrilio service"""


    def __init__(self, db_conn=None, logger=None):
        self.__db = db_conn if db_conn is not None else sqlite3.connect("flaskrilio.db")
        self.__log = setup_console_logger(logger, "FlaskrilioDBHandler")
        self.__log.debug("Flaskrilio DB Handler successfully initialized!")


    def dict_from_row(self, cur):
        """Transforms sqlite3 result cursor into dictionary"""
        colname = [ d[0] for d in cur.description ]
        result_dict = [ dict(zip(colname, r)) for r in cur.fetchall() ]
        return result_dict


    def close(self):
        self.__log.debug("Closing DB connection")
        self.__db.close()


    def get_all_calls(self):
        cur = self.__db.execute('select * from calls order by id desc')
        return self.dict_from_row(cur)


    def get_last_outbound_call(self, from_no, to_no):
        """
        Will try to select last matching outbound call record
        """
        query = 'select * from calls where '\
                'FromNo="%s" '\
                'and ToNo="%s" '\
                'and Direction="outbound-api" '\
                'order by id desc ' \
                'limit 1;' \
                % (str(from_no).replace("+", ""),
                   str(to_no).replace("+", ""))
        self.__log.debug("Querying DB with: '%s'" % query)
        outbound_call_cur = self.__db.execute(query)
        res = self.dict_from_row(outbound_call_cur)[0]
        if res is not None:
            return res[0]
        else:
            return []


    def get_last_inbound_call(self, from_no, to_no):
        """
        Will try to select last matchin inbound call record
        """
        query = 'select * from calls where '\
                'FromNo="%s" '\
                'and ToNo="%s" '\
                'and Direction="inbound" '\
                'order by id desc ' \
                'limit 1;' \
                % (str(from_no).replace("+", ""),
                   str(to_no).replace("+", ""))
        self.__log.debug("Querying DB with: '%s'" % query)
        inbound_call_cur = self.__db.execute(query)
        res = self.dict_from_row(inbound_call_cur)
        if res is not None:
            return res[0]
        else:
            return []


    def add_times_to_call(self, callSid, start_time, end_time):
        """
        Will add start and end times to a selected call
        """
        query = 'update calls set ' \
                'StartTime="%s", ' \
                'EndTime="%s" ' \
                'where CallSId="%s";' \
                % (start_time, end_time, callSid)
        self.__log.debug("Updating DB with: '%s'" % query)
        self.__db.execute(query)
        self.__db.commit()
        self.__log.debug("Successfully updated times for callSid:'%s'" % callSid)
