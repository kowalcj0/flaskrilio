# -*- coding: utf-8 -*-
import json
from urllib2 import urlopen


def get_public_ip():
    return json.load(urlopen('http://httpbin.org/ip'))['origin']


if __name__ == '__main__':
    print get_public_ip()
