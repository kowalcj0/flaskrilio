# -*- coding: utf-8 -*-
from behave import *
import logging

##############################################################################
#
# Preconfigure the evnironment using any of these steps :)
#
def before_step(context, step):
    logging.debug("These run before every step.")

def before_scenario(context, scenario):
    logging.debug("These run before each scenario is run.")

def before_feature(context, feature):
    logging.debug("These run before each feature file is exercised.")

def before_tag(context, tag):
    logging.debug("These run before a section tagged with the given name. They are invoked for each tag encountered in the order they’re found in the feature file. See controlling things with tags.")

def before_all(context):
    # get logger
    context.logger = logging.getLogger('twilio-ec2.CallConnectHandler')
    # create file handler which logs even debug messages
    fh = logging.FileHandler('behave.log')
    # create console handler with a higher log level
    context.logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    fh.setLevel(logging.DEBUG)
    # create formatter and add it to the handlers
    formatter=logging.Formatter('[%(asctime)s] [%(levelname)s]: %(message)s', "%a %Y-%m-%d %H:%M:%S %z")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    context.logger.addHandler(ch)
    context.logger.addHandler(fh)
    #if not context.config.log_capture:
    #logging.basicConfig(level=logging.DEBUG)

def after_step(context, step):
    logging.debug("These run after every step.")

def after_scenario(context, scenario):
    logging.debug("These run after each scenario is run.")

def after_feature(context, feature):
    logging.debug("These run after each feature file is exercised.")

def after_tag(context, tag):
    logging.debug("These run after a section tagged with the given name. They are invoked for each tag encountered in the order they’re found in the feature file. See controlling things with tags.")

def after_all(context):
    logging.debug("Executed after all features")
#
#
##############################################################################




