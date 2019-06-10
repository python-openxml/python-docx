#!/usr/bin/env python

import os
import re

from setuptools import find_packages, setup


def text_of(relpath):
    """
    Return string containing the contents of the file at *relpath* relative to
    this file.
    """
    thisdir = os.path.dirname(__file__)
    file_path = os.path.join(thisdir, os.path.normpath(relpath))
    with open(file_path) as f:
        text = f.read()
    return text


# Read the version from docx.__version__ without importing the package
# (and thus attempting to import packages it depends on that may not be
# installed yet)
version = re.search(
    "__version__ = '([^']+)'", text_of('docx/__init__.py')
).group(1)


NAME = 'python-docx'
VERSION = version
DESCRIPTION = 'Create and update Microsoft Word .docx files.'
KEYWORDS = 'docx office openxml word'
AUTHOR = 'Steve Canny'
AUTHOR_EMAIL = 'python-docx@googlegroups.com'
URL = 'https://github.com/python-openxml/python-docx'
LICENSE = text_of('LICENSE')
PACKAGES = find_packages(exclude=['tests', 'tests.*'])
PACKAGE_DATA = {'docx': ['templates/*.xml', 'templates/*.docx']}

INSTALL_REQUIRES = ['lxml>=2.3.2']
TEST_SUITE = 'tests'
TESTS_REQUIRE = ['behave', 'mock', 'pyparsing', 'pytest']

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
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Topic :: Office/Business :: Office Suites',
    'Topic :: Software Development :: Libraries'
]

LONG_DESCRIPTION = text_of('README.rst') + '\n\n' + text_of('HISTORY.rst')


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
