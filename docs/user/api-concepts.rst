
API basics
==========

The API for |docx| is designed to make doing simple things simple, while
allowing more complex results to be achieved with a modest and incremental
investment of understanding.

It's possible to create a basic document using only a single object, the
|api-Document| object returned when opening a file. The methods on
|api-Document| allow *block-level* objects to be added to the end of the
document. Block-level objects include paragraphs, inline pictures, and tables.
Headings, bullets, and numbered lists are simply paragraphs with a particular
style applied.

In this way, a document can be "written" from top to bottom, roughly like
a person would if they knew exactly what they wanted to say This basic use
case, where content is always added to the end of the document, is expected to
account for perhaps 80% of actual use cases, so it's a priority to make it as
simple as possible without compromising the power of the overall API.


Inline objects
--------------

Each block-level method on |api-Document|, such as ``add_paragraph()``, returns
the block-level object created. Often the reference is unneeded; but when
inline objects must be created individually, you'll need the block-item
reference to do it.

... add example here as API solidifies ...
