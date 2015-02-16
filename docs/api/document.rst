
.. _document_api:

Document objects
================

The main Document and related objects.


|Document| constructor
----------------------

.. autofunction:: docx.Document


|Document| objects
------------------

.. autoclass:: docx.document.Document()
   :members:
   :exclude-members: styles_part


|CoreProperties| objects
-------------------------

Each |Document| object provides access to its |CoreProperties| object via its
:attr:`core_properties` attribute. A |CoreProperties| object provides
read/write access to the so-called *core properties* for the document. The
core properties are author, category, comments, content_status, created,
identifier, keywords, language, last_modified_by, last_printed, modified,
revision, subject, title, and version.

Each property is one of three types, |str|, |datetime|, or |int|. String
properties are limited in length to 255 characters and return an empty string
('') if not set. Date properties are assigned and returned as |datetime|
objects without timezone, i.e. in UTC. Any timezone conversions are the
responsibility of the client. Date properties return |None| if not set.

|docx| does not automatically set any of the document core properties other
than to add a core properties part to a presentation that doesn't have one
(very uncommon). If |docx| adds a core properties part, it contains default
values for the title, last_modified_by, revision, and modified properties.
Client code should update properties like revision and last_modified_by
if that behavior is desired.

.. currentmodule:: docx.opc.coreprops

.. class:: CoreProperties

   .. attribute:: author

      *string* -- An entity primarily responsible for making the content of the
      resource.

   .. attribute:: category

      *string* -- A categorization of the content of this package. Example
      values might include: Resume, Letter, Financial Forecast, Proposal,
      or Technical Presentation.

   .. attribute:: comments

      *string* -- An account of the content of the resource.

   .. attribute:: content_status

      *string* -- completion status of the document, e.g. 'draft'

   .. attribute:: created

      *datetime* -- time of intial creation of the document

   .. attribute:: identifier

      *string* -- An unambiguous reference to the resource within a given
      context, e.g. ISBN.

   .. attribute:: keywords

      *string* -- descriptive words or short phrases likely to be used as
      search terms for this document

   .. attribute:: language

      *string* -- language the document is written in

   .. attribute:: last_modified_by

      *string* -- name or other identifier (such as email address) of person
      who last modified the document

   .. attribute:: last_printed

      *datetime* -- time the document was last printed

   .. attribute:: modified

      *datetime* -- time the document was last modified

   .. attribute:: revision

      *int* -- number of this revision, incremented by Word each time the
      document is saved. Note however |docx| does not automatically increment
      the revision number when it saves a document.

   .. attribute:: subject

      *string* -- The topic of the content of the resource.

   .. attribute:: title

      *string* -- The name given to the resource.

   .. attribute:: version

      *string* -- free-form version string
