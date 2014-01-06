# -*- coding: utf-8 -*-
import twilio
from twilio.rest import TwilioRestClient
import ConfigParser
import logging
from sys import exit
import os
from helpers.common import setup_console_logger


class TwilioHandler:
    """A simple class to make a call from a twilio number"""

    def __init__(self, logger=None):
        self.__log = setup_console_logger(logger, "TwilioHandler")
        self.__log.debug("TwilioHandler initialized")
        self.cfg = {}


    def load_config(self, twilio_config):
        with open(twilio_config, 'rb') as cfg:
            cp = ConfigParser.RawConfigParser(allow_no_value=True)
            cp.read(twilio_config)
            self.__log.info("Configuration loaded from %s" % twilio_config)
            self.twilio_config = twilio_config
            self.cfg['twilio_api_ver'] = cp.get('twilio_api', 'twilio_api_ver')
            self.cfg['account_sid'] = cp.get('twilio_api', 'account_sid')
            self.cfg['auth_token'] = cp.get('twilio_api', 'auth_token')


    def connect_to_twilio(self):
        try:
            self.client = twilio.rest.TwilioRestClient(self.cfg['account_sid'],
                                                  self.cfg['auth_token'])
            self.__log.info("Connected to Twilio 😏 ")
        except twilio.TwilioRestException as e:
            self.__log.error("Something went wrong when trying to connect to Twilio...😓 ")
            print e


    def call(self, from_no, to_no):
        try:
            call = self.client.calls.create(to = to_no,
                                           from_= from_no,
                                           url = "http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient")
            self.__log.info("Call from %s to %s successfully created - call_sid %s" % (from_no, to_no, call.sid))
            return call
        except twilio.TwilioRestException as e:
            self.__log.error("Something went wrong when trying to establish a call...")
            print e


    def call_with_twiml(self, from_no, to_no, twiml_url, scu_url=None, scu_method=None):
        try:
            if scu_url is not None:
                scu_method = 'POST' if scu_method is None else scu_method
                call = self.client.calls.create(to = to_no,
                                            from_= from_no,
                                            url = twiml_url,
                                            status_callback = scu_url,
                                            status_method = scu_method)
            else:
                call = self.client.calls.create(to = to_no,
                                            from_= from_no,
                                            url = twiml_url)
            self.__log.debug("Twilio Call dict: %s " % call.__dict__)
            self.__log.info("Call from %s to %s successfully created - call_sid %s" % (from_no, to_no, call.sid))
            return call
        except twilio.TwilioRestException as e:
            self.__log.error("Something went wrong when trying to establish a call...")
            print e



    def get_call_details(self, callSid):
        try:
            return self.client.calls.get(callSid)
        except twilio.TwilioRestException as e:
            self.__log.error("Something went wrong when trying to get call details for call_sid=%s" % callSid)
            print e


    def print_config(self):
        for key,val in self.cfg.items():
            self.__log.info("%s=%s" % (key, val))


    def get_recording(self, call):
        pass


    def set_voice_url(self, url):
        # more on this here
        #https://twilio-python.readthedocs.org/en/latest/api/rest/resources.html#twilio.rest.resources.PhoneNumber
        pass


    def get_all_incoming_twilio_numbers(self):
        phoneNumbers = self.client.phone_numbers.list()
        self.__log.debug("List of all available incoming Twilio numbers:")
        for n in phoneNumbers:
            self.__log.debug("Number:%s - sid:%s - Object dict: %s" % (n.phone_number, n.sid, n.__dict__))
        return phoneNumbers


    def get_number_sid_for_phone(self, number):
        all_numbers = self.get_all_incoming_twilio_numbers()
        for n in all_numbers:
            if n.phone_number == number:
                self.__log.debug(
                    "Found '%s' in the list of all numbers. " \
                    "Its sid is: %s" % (number, n.sid))
                return n.sid
        return None


    def get_number_details(self, number=None, number_sid=None):
        if number_sid is None:
            number_sid = self.get_number_sid_for_phone(number)
        number_details = self.client.phone_numbers.get(number_sid)
        self.__log.debug("%s details: %s" % (number_details.phone_number,
                                             number_details.__dict__))
        return number_details


    def update_number_vru_url(self,
                              number_sid=None,
                              vru=None,
                              method=None):
        method = 'POST' if method is None else method
        self.client.phone_numbers.get(number_sid).update(
            voice_url=vru,
            voice_method=method
        )


    def update_number_vfu_url(self,
                              number_sid=None,
                              vfu=None,
                              method=None):
        method = 'POST' if method is None else method
        self.client.phone_numbers.get(number_sid).update(
            voice_fallback_url=vfu,
            voice_fallback_method=method
        )


    def update_number_scu_url(self,
                              number_sid=None,
                              scu=None,
                              method=None):
        method = 'POST' if method is None else method
        self.client.phone_numbers.get(number_sid).update(
            status_callback=scu,
            status_callback_method=method
        )


    def update_number_mru_url(self,
                              number_sid=None,
                              mru=None,
                              method=None):
        method = 'POST' if method is None else method
        self.client.phone_numbers.get(number_sid).update(
            sms_url=mru,
            sms_method=method
        )


    def update_number_mfu_url(self,
                              number_sid=None,
                              mfu=None,
                              method=None):
        method = 'POST' if method is None else method
        self.client.phone_numbers.get(number_sid).update(
            sms_fallback_url=mfu,
            sms_fallback_method=method
        )



if '__main__' == __name__:
    import optparse

    # Populate our options, -h/--help is already there for you.
    optp = optparse.OptionParser()
    optp.add_option('-v', '--verbose', dest='verbose', action='count',
                    help="Increase verbosity (specify multiple times for more)")
    optp.add_option('-c', '--config-file', dest='config',
                    help="Config file")
    # Parse the arguments (defaults to parsing sys.argv).
    opts, args = optp.parse_args()

    # Here would be a good place to check what came in on the command line and
    # call optp.error("Useful message") to exit if all it not well.


    # create logger with '__name__'
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    formatter=logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s', "%a %Y-%m-%d %H:%M:%S %z")
    ch.setFormatter(formatter)
    logger.addHandler(ch)


    log_level = logging.INFO # default
    if opts.verbose >= 1:
        log_level = logging.DEBUG

    if not opts.config:
        logger.error("No config file specified!")
        exit(1)
    else:
        if os.path.exists(opts.config):
            config=opts.config
        else:
            logger.error("Input file '%s' doesn't exist!" %  opts.config)
            exit(66)

    caller = Caller()
    caller.load_config(twilio_config=opts.config)
    caller.connect_to_twilio()
    caller.print_config()
    caller.call(from_no="+441353210177", to_no="+447402028595")
