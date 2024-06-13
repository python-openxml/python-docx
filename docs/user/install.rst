.. _install:

Installing
==========

.. note:: python-docx versions 0.3.0 and later are not API-compatible with
   prior versions.

|docx| is hosted on PyPI, so installation is relatively simple, and just
depends on what installation utilities you have installed.

|docx| may be installed with ``pip``::

    pip install python-docx

It can also be installed manually by downloading the distribution from PyPI,
unpacking the tarball, and running ``setup.py``::

    tar xvzf python-docx-{version}.tar.gz
    cd python-docx-{version}
    python setup.py install

|docx| depends on the ``lxml`` package. ``pip`` will take care of satisfying
those dependencies for you, but if you install manually you will need to
install it yourself.


Dependencies
------------

* Python 2.6, 2.7, 3.3, or 3.4
* lxml >= 2.3.2
