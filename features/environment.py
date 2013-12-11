# -*- coding: utf-8 -*-
from behave import *
import logging
import os
import sys
from multiprocessing import Process
import tempfile
import sqlite3
from flaskrilio_handler import FlaskrilioHandler
from call_connect_handler import CallConnectHandler
from twilio_handler import TwilioHandler



# Set Path
pwd = os.path.abspath(os.path.dirname(__file__))
project = os.path.basename(pwd)
new_path = pwd.strip(project)
activate_this = os.path.join(new_path, 'flaskr')
sys.path.append(activate_this)

from flaskrilio import app, connect_db

##############################################################################
#
# Preconfigure the evnironment using any of these steps :)
#
def before_step(context, step):
    pass
    #logging.debug("These run before every step.\n")


def before_scenario(context, scenario):
    pass
    #logging.debug("These run before each scenario is run.\n")


def before_feature(context, feature):
    pass


def before_tag(context, tag):
    pass
    #logging.debug("These run before a section tagged with the given name. \
        #They are invoked for each tag encountered in the order they’re found \
        #in the feature file. See controlling things with tags.")


def before_all(context):
    """
    """
    # get logger
    context.log = logging.getLogger('twilio-ec2.Behave')
    # create file handler which logs even debug messages
    fh = logging.FileHandler('behave.log')
    # create console handler with a higher log level
    context.log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    fh.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s]: %(message)s',
                                  "%a %Y-%m-%d %H:%M:%S %z")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    context.log.addHandler(ch)
    context.log.addHandler(fh)
    #if not context.config.log_capture:
    #logging.basicConfig(level=logging.DEBUG)

    # get a connection to local sqlite3 twilio.db managed by flaskrilio script
    context.db = connect_db()
    # get a Flaskrilio Handler used to make HTTP requests to this service
    context.fh = FlaskrilioHandler(hostname="http://127.0.0.1:5000", logger=context.log)
    context.cc = CallConnectHandler(hostname="http://callconnect.poc.hibulabs.co.uk", logger=context.log)
    context.th = TwilioHandler(logger=context.log)


def after_step(context, step):
    pass
    #logging.debug("These run after every step.")


def after_scenario(context, scenario):
    pass
    #logging.debug("These run after each scenario is run.")


def after_feature(context, feature):
    pass
    #logging.debug("These run after each feature file is exercised.")


def after_tag(context, tag):
    pass
    #logging.debug("These run after a section tagged with the given name. \
                   #They are invoked for each tag encountered in the order \
                   #they’re found in the feature file. See controlling things \
                   #with tags.")


def after_all(context):
    # close db connection
    context.db.close()
    context.log.debug("Executed after all features")


#
#
##############################################################################
