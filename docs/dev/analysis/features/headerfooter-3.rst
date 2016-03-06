
Headers experimentation
=======================

Notes
-----

* If Header inherits from docx.blkcntnr.BlockItemContainer (as does
  docx.document._Body), we get the content editing for free (add_paragraph(),
  .paragraphs, .tables, etc.). We'll need to take a closer look to make sure,
  but I'm thinking it should work unchanged.


Header API
----------

* Header.is_linked_to_previous - read/write boolean, behavior outlined below.

* Header.text - read/write, full text, no character formatting, \n for line
  break, \n\n for paragraph (or whatever other .text bits do). Assignment can
  only be a single paragraph; can include tabs and line breaks, but no
  paragraphs.

* Items inherited from BlockItemContainer (.paragraphs, .tables,
  .add_paragraph(), .add_table())


Operations to be supported
--------------------------

* Detect whether header is present or inherited (linked to previous)
* Create header when there is none
* Obtain reference to effective header content
* Remove header, making it inherited (linked to previous)

Protocol candidate::

    # every section has a header; it is never None

    >>> header = section.header
    >>> header
    <docx.hdrftr.Header object at 0x02468ACE>

    # if that section has no w:headerReference, it inherits from the prior
    # section

    >>> header.is_linked_to_previous
    True

    # constructive editing operations transparently operate on the source
    # header, that of the first prior section having a header (if the current
    # section has none). If no prior sections have a header, one is created
    # in the first section of the document on the first constructive edit
    # call.

    >>> header = document.sections[0].header
    >>> header.is_linked_to_previous
    True
    >>> header.text = 'foobar'
    >>> header.is_linked_to_previous
    False

    # A header can be explicitly added to a section by assigning False to
    # Header.is_linked_to_previous

    >>> header.is_linked_to_previous
    True
    >>> header.is_linked_to_previous = False
    >>> header.is_linked_to_previous
    False

    # Conversely, a header can be deleted from a section by assigning True to
    # Header.is_linked_to_previous

    >>> header.is_linked_to_previous
    False
    >>> header.is_linked_to_previous = True
    >>> header.is_linked_to_previous
    True


Use cases
---------

* Add a header to a single section document::

  >>> header = document.sections[0].header
  >>> header.text = 'foobar'

* Get the header text from a single section document::

  >>> header = document.sections[0].header
  >>> header.text
  'foobar'

* Insert a section in the middle of (above) a single section that has
  a header defined.


Conclusions
-----------

* An empty header is NOT the same as no header. Word saves an empty header
  when necessary to make a section's header distinct from that of the prior
  section. This is accomplished in the UI by unchecking the 'Link to
  Previous' checkbox. The absence of a header indicates its value is
  inherited. An empty header just displays no content, but is in every other
  way a full header.

* A header part never exists without at least one w:headerReference element
  pointing to it. The associated header part needs to be removed when
  a w:headerReference element is removed.

* A first and even header reference and part are retained even when they are
  "hidden" by the "different first page" or "even and odd" settings for the
  document.

* A header can only be inherited from (linked to) the immediately prior
  section. If the prior header is itself inherited, the inheritance is
  cascaded. Inheritance cannot "skip over" an intervening header; Only the
  first prior header is available for inheritance.


Experiment agenda
-----------------

* [ ] Create three-section document with no headers. Add header to each
      section separately and see what happens in each case. Start fresh for
      each case.

* [ ] Create single section document, give it a header, then insert second
      section in the middle. Who gets the header and who inherits (or gets
      copies)?

* [ ] Create document with even-odd headers and three sections. See if headers
      can be inherited separately or needs to be all three at once (in UI
      anyway).

* [ ] Can a header part be referred to by multiple references? (I'm thinking
      no, based on inheritance can't skip a section.) Might need to try this
      with manual editing to see if Word barfs. I'm not seeing just now how
      this might reasonably arise, except maybe inserting a section between
      two that inherit and changing the new section's header


Experiment 1 - View header/footer
---------------------------------

* A blank document has a sectPr, but it contains no header or footer
  references. The document contains no header or footer parts.

* `View > Header and Footer` displays a header and footer editing area and
  places the insertion point within.

* Entering the area but not making a change, does not create a header.

* Entering the area and adding text, creates a header. The header
  contents are displayed in a grayed out font after leaving the header
  editing area.

* Deleting the entire contents of the header (but leaving the non-deletable
  paragraph mark) removes the header part and reference.


Experiment 2 - Add section
--------------------------

* Inserting a section break in the middle of a single section document having
  no header adds a new w:sectPr at the insertion point. The new section has
  no header references.
  
* After adding a header only to the first section:
  
  + A w:headerReference is added to the first w:sectPr
  + No w:headerReference is added to the second w:sectPr
  + The 'Link to Previous' checkbox is ticked on the Header toolbar for the
    second section.
  + The section 1 header is displayed on the second section in the UI; the
    header info/control bar displays 'Same as Previous'.

* Adding a header only to the second section has two variants:

  + In the default case, the 'Link to Previous' checkbox is checked (for the
    second section) by default when the new section is inserted.

    In this case, a w:headerReference element is added to the *first*
    w:sectPr and is inherited by the second section, even though the editing
    is done on the section section editing area.

  + The second case requires clearing the 'Link to Previous' checkbox.

    In this case, a w:headerReference is added to the second section only.
    Only the one header part is added.


Anomalies
---------

* Something odd happens when unlinking then relinking the second header. The
  first section gets all three header and footerReference elements and six
  new parts are added (3 each header and footer).


Common experiment steps
-----------------------

1. Create new document, change page setup to A5 landscape (so multiple pages
   show easily at once).

2. Type in 'Section 1<CR>Section 2'. Insert a section break (next page)
   before the 'S' beginning the second paragraph.

3. Enter header edit mode using View > Header and Footer
