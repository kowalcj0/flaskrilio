#! /usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Janusz Kowalczyk'

from fabric.api import *


# tasks:
# http://docs.fabfile.org/en/1.8/tutorial.html
# *- spawn ec2 instance
# *- install dependencies
# *- deploy code
# *- start flaskrilio in background
# *- run behave tests
# *- download junit report
# *- download flaskrilio db
# *- download all the logs (flaskrilio, behave, plain output)

def pack():
    # create a new source distribution as tarball
    local('python setup.py sdist --formats=gztar', capture=False)

def spawn_ec2_instaces():
    pass


def provision():
    pass


def start_flaskrilio():
    pass

def stop_flaskrilio():
    pass


def download_results():
    pass

def run_behave():
    pass
