.. image:: https://travis-ci.org/python-openxml/python-docx.svg?branch=master
   :target: https://travis-ci.org/python-openxml/python-docx

*python-docx* is a Python library for creating and updating Microsoft Word
(.docx) files.

More information is available in the `python-docx documentation`_.

.. _`python-docx documentation`:
   https://python-docx.readthedocs.org/en/latest/

This fork of the repository includes a merge from `renejsum's fork <https://github.com/renejsum/python-docx>`_ with recent master from `the origin <https://github.com/python-openxml/python-docx>`_ to provide support read/write access to custom metadata properties of the document. For example::

  >>> import docx
  >>> d = docx.Document('test1.docx')
  >>> p = d.custom_properties
  >>> print(p['prov_wasDerivedFrom'])
  fid://slap.G24X2UWc
  >>> p['prov_wasAssociatedWith'] = 'some other value'
  >>> d.save('test1.docx')
