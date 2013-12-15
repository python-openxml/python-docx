.. _install:

Installing
==========

|docx| is hosted on PyPI, so installation is relatively simple, and just
depends on what installation utilities you have installed.

|docx| may be installed with ``pip`` if you have it available::

    pip install python-docx

It can also be installed using ``easy_install``::

    easy_install python-docx

If neither ``pip`` nor ``easy_install`` is available, it can be installed
manually by downloading the distribution from PyPI, unpacking the tarball,
and running ``setup.py``::

    tar xvzf python-docx-0.1.0a1.tar.gz
    cd python-docx-0.1.0a1
    python setup.py install

|docx| depends on the ``lxml`` package and the ``Pillow`` Imaging Library.
Both ``pip`` and ``easy_install`` will take care of satisfying those
dependencies for you, but if you use this last method you will need to install
those yourself.


Dependencies
------------

* Python 2.6, 2.7, 3.3, 3.4
* lxml
* Pillow
