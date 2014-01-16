# -*- coding: utf-8 -*-
"""Flaskrilio

"""

classifiers = """\
Development Status :: 5 - Testing/Stable
Intended Audience :: Testers and Developers
License :: OSI Approved :: BSD Public License
Programming Language :: Python
Topic :: RESTful services
Topic :: Software Development :: Testing
Operating System :: Unix
"""

from setuptools import setup, find_packages
import sys
from distutils.core import setup

if sys.version_info < (2, 3):
    _setup = setup
    def setup(**kwargs):
        if kwargs.has_key("classifiers"):
            del kwargs["classifiers"]
        _setup(**kwargs)


doclines = __doc__.split("\n")


setup(
    name='flaskrilio',
    version='1.0a',
    maintainer="kowalcj0",
    maintainer_email="kowalcj0@gmail.com",
    url="https://github.com/kowalcj0/twilio-ec2",
    platforms = ["any"],
    long_description=doclines[0],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask==0.10',
        'behave==1.2.3',
        'httplib2==0.8',
        'twilio==3.6.4',
        'python-dateutil==2.2',
        'requests==2.1.0'
        ]
)
