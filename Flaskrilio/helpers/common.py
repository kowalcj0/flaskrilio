# -*- coding: utf-8 -*-
import os
import errno
import json
import logging
import copy
from urllib2 import urlopen
from datetime import datetime


def get_public_ip():
    return json.load(urlopen('http://httpbin.org/ip'))['origin']


def get_datetime():
    return datetime.now().strftime("%Y-%m-%d_-_%H_%M_%S")


def mkdir_p(path):
    """http://stackoverflow.com/a/600612"""
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise


def setup_console_logger(logger=None, name=None, level=None):
    if logger is not None:
        log = copy.copy(logger)
        log.name = name
        return log
    else:
        log = logging.getLogger(name)
        if level is None:
            log.setLevel(logging.DEBUG)
        else:
            log.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        # create formatter and add it to the handlers
        formatter = logging.Formatter(
            '[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s',
            "%a %Y-%m-%d %H:%M:%S %z")
        ch.setFormatter(formatter)
        log.addHandler(ch)
        return log


def setup_file_logger(logger=None, name=None, logfile=None, level=None):
    if logger is not None:
        return logger
    else:
        log = logging.getLogger(name)
        # create file handler which logs even debug messages
        fh = logging.FileHandler(logfile)
        if level is None:
            log.setLevel(logging.DEBUG)
        else:
            log.setLevel(level)
        fh.setLevel(logging.DEBUG)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s',
                                        "%a %Y-%m-%d %H:%M:%S %z")
        fh.setFormatter(formatter)
        log.addHandler(fh)
        return log


if __name__ == '__main__':
    print get_public_ip()
