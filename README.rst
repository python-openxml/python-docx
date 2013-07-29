###########
python-docx
###########

VERSION: 0.3.0d1 (first development release)


STATUS (as of July 29 2013)
===========================

First development release. Under active development.


Vision
======


Documentation
=============

Documentation is hosted on Read The Docs (readthedocs.org) at
https://python-docx.readthedocs.org/en/latest/.


Reaching out
============

We'd love to hear from you if you like |pd|, want a new feature, find a bug,
need help using it, or just have a word of encouragement.

The **mailing list** for |pd| is (google groups ... )

The **issue tracker** is on github at `python-openxml/python-docx`_.

Feature requests are best broached initially on the mailing list, they can be
added to the issue tracker once we've clarified the best approach,
particularly the appropriate API signature.

.. _`python-openxml/python-docx`:
   https://github.com/python-openxml/python-docx


Installation
============

|pd| may be installed with ``pip`` if you have it available::

    pip install python-docx

It can also be installed using ``easy_install``::

    easy_install python-docx

If neither ``pip`` nor ``easy_install`` is available, it can be installed
manually by downloading the distribution from PyPI, unpacking the tarball,
and running ``setup.py``::

    tar xvzf python-docx-0.0.1d1.tar.gz
    cd python-docx-0.0.1d1
    python setup.py install

|pd| depends on the ``lxml`` package. Both ``pip`` and ``easy_install`` will
take care of satisfying that dependency for you, but if you use this last
method you will need to install ``lxml`` yourself.


Release History
===============

July 29, 2013 - v0.3.0d1
   * Establish initial enviornment and development branches


License
=======

Licensed under the `MIT license`_. Short version: this code is copyrighted by
me (Steve Canny), I give you permission to do what you want with it except
remove my name from the credits. See the LICENSE file for specific terms.

.. _MIT license:
   http://www.opensource.org/licenses/mit-license.php

.. |pd| replace:: ``python-docx``
