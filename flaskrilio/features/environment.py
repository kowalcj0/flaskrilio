# -*- coding: utf-8 -*-
from behave import *
import logging
import os
import sys
from multiprocessing import Process
import tempfile
import sqlite3
from helpers.common import get_public_ip
from handlers.call_connect_handler import CallConnectHandler
from handlers.flaskrilio_handler import FlaskrilioHandler
from handlers.twilio_handler import TwilioHandler
from handlers.flaskrilio_db_handler import FlaskrilioDBHandler



# Set Path
pwd = os.path.abspath(os.path.dirname(__file__))
project = os.path.basename(pwd)
new_path = pwd.strip(project)
activate_this = os.path.join(new_path, 'flaskr')
sys.path.append(activate_this)

from flaskriliosrv import app, connect_db

##############################################################################
#
# Preconfigure the evnironment using any of these steps :)
#
def before_step(context, step):
    context.log.debug("[STEP]: '%s %s'" % (step.keyword, step.name))


def before_scenario(context, scenario):
    context.log.info(
        "\n\n===============================================================\n" \
        "Starting scenario: '%s'\n" \
        "================================================================" \
        % scenario.name)


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
    # overwrite the old log file
    fh = logging.FileHandler(filename='reports/behave.log', mode='w')
    # create console handler with a higher log level
    context.log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    fh.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s',
                                  "%a %Y-%m-%d %H:%M:%S %z")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    context.log.addHandler(ch)
    context.log.addHandler(fh)
    #if not context.config.log_capture:
    #logging.basicConfig(level=logging.DEBUG)

    # get a connection to local sqlite3 twilio.db managed by flaskrilio script
    context.db = FlaskrilioDBHandler(db_conn=connect_db(), logger=context.log)

    ##########################################################################
    # configure FlaskrilioHandler
    if os.environ.get('MODE') is not None:
        if os.environ['MODE'] == 'EC2':
            from helpers.common import get_public_ip
            context.flaskip = get_public_ip()
            context.flaskport = 80
            context.flaskhost = "http://%s:%d" % (context.flaskip,
                                                  context.flaskport)
            context.publichost = "http://%s:%d" % (context.flaskip,
                                                  context.flaskport)
    else:
        context.flaskip = "127.0.0.1"
        context.flaskport = 5000
        context.flaskhost = "http://%s:%d" % (context.flaskip,
                                              context.flaskport)
        # Provide a publicly available host serving Twimls when running locally
        if os.environ.get('NGROK') is not None:
            context.publichost = os.environ.get('NGROK')
        else:
            context.publichost = "http://54.247.15.37"
    context.log.debug("PUBLIC HOST set to: %s" % context.publichost)
    context.fh = FlaskrilioHandler(hostname="%s" % (context.flaskhost),
                                   logger=context.log)
    ##########################################################################

    ##########################################################################
    # configure CallConnectHandler
    if os.environ.get('ENV') is not None:
        if os.environ['ENV'] == 'POC':
            cchost = "http://callconnect.poc.hibulabs.co.uk"
        elif os.environ['ENV'] == 'DEV':
            cchost = "http://callconnect.dev.hibulabs.co.uk"
        elif os.environ['ENV'] == 'USPROD':
            cchost = "http://callconnect.dev.hibulabs.co.uk"
    else:
        cchost = "http://callconnect.dev.hibulabs.co.uk"
    context.cch = CallConnectHandler(hostname=cchost, logger=context.log)
    ##########################################################################

    ##########################################################################
    # configure TwilioHandler
    context.th = TwilioHandler(logger=context.log)
    context.th.load_config(twilio_config="twilio.cfg")
    context.th.connect_to_twilio()
    ##########################################################################


def after_step(context, step):
    pass
    #logging.debug("These run after every step.")


def after_scenario(context, scenario):
    context.log.info(
        "\n===============================================================\n" \
        "Finished scenario: '%s'\n" \
        "================================================================\n" \
        % scenario.name)


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
