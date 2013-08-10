=================
Design Narratives
=================

Narrative explorations into design issues, serving initially as an aid to
reasoning and later as a memorandum of the considerations undertaken during
the design process.


Semi-random bits
----------------

*partname* is a marshaling/serialization concern.

*partname* (pack URI) is the addressing scheme for accessing serialized parts
within the package. It has no direct relevance to the unmarshaled graph except
for use in re-marshaling unmanaged parts or to avoid renaming parts when the
load partname will do just fine.

What determines part to be constructed? Relationship type or content type?

   *Working hypothesis*: Content type should be used to determine the type of
   part to be constructed during unmarshaling.

   Content type is more granular than relationship type. For example, an image
   part can be any of several content types, e.g. jpg, gif, or png. Another
   example is RT.OFFICE_DOCUMENT. This can apply to any of CT.PRESENTATION,
   CT.DOCUMENT, or CT.SPREADSHEET and their variants.

   However, I can't think of any examples of where a particular content type
   may be the target of more than one possible relationship type. That seems
   like a logical possibility though.

   There are examples of where a relationship type (customXml for example) are
   used to refer to more than one part type (Additional Characteristics,
   Bibliography, and Custom XML parts in this case). In such a case I expect
   the unmarshaling and part selection would need to be delegated to the source
   part which presumably would contain enough information to resolve the
   ambiguity in its body XML. In that case, a BasePart could be constructed and
   let the source part create a specific subclass on |after_unmarshal|.

When properties of a mutable type (e.g. list) are returned, what is returned
should be a copy or perhaps an immutable variant (e.g. tuple) so that
client-side changes don't need to be accounted for in testing. If the return
value really needs to be mutable and a snapshot won't do, it's probably time to
make it a custom collection so the types of mutation that are allowed can be
specified and tested.

In PackURI, the baseURI property does not include any trailing slash. This
behavior is consistent with the values returned from ``posixpath.split()`` and
is then in a form suitable for use in ``posixpath.join()``.


Design Narrative -- Blob proxy
==============================

Certain use cases would be better served if loading large binary parts such as
images could be postponed or avoided. For example, if the use case is to
retrieve full text from a presentation for indexing purposes, the resources
and time consumed to load images into memory is wasted. It seems feasible to
develop some sort of blob proxy to postpone the loading of these binary parts
until such time as they are actually required, passing a proxy of some type to
be used instead. If it were cleverly done, the client code wouldn't have to
know, i.e. the proxy would be transparent.

The main challenge I see is how to gain an entry point to close the zip archive
after all loading has been completed. If it were reopened and closed each time
a part was loaded that would be pretty expensive (an early verion of
python-pptx did exactly that for other reasons). Maybe that could be done when
the presentation is garbage collected or something.

Another challenge is how to trigger the proxy to load itself. Maybe blob could
be an object that has file semantics and the read method could lazy load.

Another idea was to be able to open the package in read-only mode. If the file
doesn't need to be saved, the actual binary objects don't actually need to be
accessed. Maybe this would be more like read-text-only mode or something.
I don't know how we'd guarantee that no one was interested in the image
binaries, even if they promised not to save.

I suppose there could be a "read binary parts" method somewhere that gets
triggered the first time a binary part is accessed, as it would be during
save(). That would address the zip close entry point challenge.

It does all sound a bit complicated for the sake of saving a few milliseconds,
unless someone (like Google :) was dealing with really large scale.


Design Narrative -- Custom Part Class mapping
=============================================

::

    pkg.register_part_classes(part_class_mapping)

    part_class_mapping = {
        CT_SLIDE: _Slide,
        CT_PRESENTATION: _Presentation
        ...
    }


Design Narrative -- Model-side relationships
============================================

Might it make sense to maintain XML of .rels stream throughout life-cycle?
--------------------------------------------------------------------------

No. The primary rationale is that a partname is not a primary model-side
entity; partnames are driven by the serialization concern, providing a method
for addressing serialized parts. Partnames are not required to be up-to-date in
the model until after the |before_marshal| call to the part returns. Even if
all part names were kept up-to-date, it would be a leakage across concern
boundaries to require a part to notify relationships of name changes; not to
mention it would introduce additional complexity that has nothing to do with
manipulation of the in-memory model.

**always up-to-date principle**

  Model-side relationships are maintained as new parts are added or existing
  parts are deleted. Relationships for generic parts are maintained from load
  and delivered back for save without change.

I'm not completely sure that the always-up-to-date principle need necessarily
apply in every case. As long as the relationships are up-to-date before
returning from the |before_marshal| call, I don't see a reason why that
choice couldn't be at the designer's discretion. Because relationships don't
have a compelling model-side runtime purpose, it might simplify the code to
localize the pre-serialization concern to the |before_marshal| method.

.. |before_marshal| replace:: :meth:`before_marshal`
.. |after_unmarshal| replace:: :meth:`after_unmarshal`


Members
-------

**rId**

   The relationship identifier. Must be a unique xsd:ID string. It is usually
   of the form 'rId%d' % {sequential_int}, e.g. ``'rId9'``, but this need not
   be the case. In situations where a relationship is created (e.g. for a new
   part) or can be rewritten, e.g. if presentation->slide relationships were
   rewritten on |before_marshal|, this form is preferred. In all other cases
   the existing rId value should be preserved. When a relationship is what the
   spec terms as *explicit*, there is a reference to the relationship within
   the source part XML, the key of which is the rId value; changing the rId
   would break that mapping.

   The **sequence** of relationships in the collection is not significant. The
   relationship collection should be regarded as a mapping on rId, not as
   a sequence with the index indicated by the numeric suffix of rId. While
   PowerPoint observes the convention of using sequential rId values for
   the slide relationships of a presentation, for example, this should not be
   used to determine slide sequence, nor is it a requirement for package
   production (saving a .pptx file).

**reltype**

  A clear purpose for reltype is still a mystery to me.

**target_mode**

**target_part**

**target_ref**
