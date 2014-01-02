.. _install:

Installing
==========

.. note:: python-docx versions 0.3.0 and later are not API-compatible with
   prior versions. Alpha users are encouraged to install in a virtualenv if
   they wish to continue using an installed prior version.

|docx| is hosted on PyPI, so installation is relatively simple, and just
depends on what installation utilities you have installed.

|docx| may be installed with ``pip`` if you have it available::

    pip install -pre python-docx

Note the ``-pre`` flag, which is required by recent versions of ``pip`` to
install pre-release versions, those with a version string having an alpha
suffix like ``0.3.0a1``. This protects the unsuspecting from upgrading to
a pre-release version.

|docx| can also be installed using ``easy_install``, although this is
discouraged::

    easy_install python-docx

If neither ``pip`` nor ``easy_install`` is available, it can be installed
manually by downloading the distribution from PyPI, unpacking the tarball,
and running ``setup.py``::

    tar xvzf python-docx-{version}.tar.gz
    cd python-docx-{version}
    python setup.py install

|docx| depends on the ``lxml`` package and the ``Pillow`` Imaging Library.
Both ``pip`` and ``easy_install`` will take care of satisfying those
dependencies for you, but if you use this last method you will need to install
those yourself.


Dependencies
------------

* Python 2.6, 2.7, 3.3, or 3.4
* lxml >= 2.3.2
* Pillow >= 2.0
