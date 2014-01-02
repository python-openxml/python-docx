#!/usr/bin/env python

import os
import re

from setuptools import find_packages, setup

# Read the version from docx.__version__ without importing the package
# (and thus attempting to import packages it depends on that may not be
# installed yet)
thisdir = os.path.dirname(__file__)
init_py = os.path.join(thisdir, 'docx', '__init__.py')
version = re.search("__version__ = '([^']+)'", open(init_py).read()).group(1)
license = os.path.join(thisdir, 'LICENSE')


NAME = 'python-docx'
VERSION = version
DESCRIPTION = 'Create and update Microsoft Word .docx files.'
KEYWORDS = 'docx office openxml word'
AUTHOR = 'Steve Canny'
AUTHOR_EMAIL = 'python-docx@googlegroups.com'
URL = 'https://github.com/python-openxml/python-docx'
LICENSE = open(license).read()
PACKAGES = find_packages(exclude=['tests', 'tests.*'])
PACKAGE_DATA = {'docx': ['templates/*']}

INSTALL_REQUIRES = ['lxml>=2.3.2', 'Pillow>=2.0']
TEST_SUITE = 'tests'
TESTS_REQUIRE = ['behave', 'mock', 'pytest']

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Topic :: Office/Business :: Office Suites',
    'Topic :: Software Development :: Libraries'
]

readme = os.path.join(thisdir, 'README.rst')
history = os.path.join(thisdir, 'HISTORY.rst')
LONG_DESCRIPTION = open(readme).read() + '\n\n' + open(history).read()


params = {
    'name':             NAME,
    'version':          VERSION,
    'description':      DESCRIPTION,
    'keywords':         KEYWORDS,
    'long_description': LONG_DESCRIPTION,
    'author':           AUTHOR,
    'author_email':     AUTHOR_EMAIL,
    'url':              URL,
    'license':          LICENSE,
    'packages':         PACKAGES,
    'package_data':     PACKAGE_DATA,
    'install_requires': INSTALL_REQUIRES,
    'tests_require':    TESTS_REQUIRE,
    'test_suite':       TEST_SUITE,
    'classifiers':      CLASSIFIERS,
}

setup(**params)
