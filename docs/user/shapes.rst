
Understanding pictures and other shapes
=======================================

Conceptually, Word documents have two *layers*, a *text layer* and a *drawing
layer*. In the text layer, text objects are flowed from left to right and from
top to bottom, starting a new page when the prior one is filled. In the drawing
layer, drawing objects, called *shapes*, are placed at arbitrary positions.
These are sometimes referred to as *floating* shapes.

A picture is a shape that can appear in either the text or drawing layer. When
it appears in the text layer it is called an *inline shape*, or more
specifically, an *inline picture*.

Inline shapes are treated like a big text character (a *character glyph*). The
line height is increased to accomodate the shape and the shape is wrapped to
a line it will fit on width-wise, just like text. Inserting text in front of it
will cause it to move to the right. Often, a picture is placed in a paragraph
by itself, but this is not required. It can have text before and after it in
the paragraph in which it's placed.

At the time of writing, |docx| only supports inline pictures. Floating pictures
can be added. If you have an active use case, submit a feature request on the
issue tracker. The ``Document.add_picture()`` method adds a specified picture
to the end of the document in a paragraph of its own. However, by digging
a little deeper into the API you can place text on either side of the picture
in its paragraph, or both.
