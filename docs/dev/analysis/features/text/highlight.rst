
Highlight
=========

Text in a Word document can be "highlighted" with a number of colors, providing text background color.


Protocol
--------

The call protocol for highlight involves manipulating the font highlight (background color) by assigning a string value from a fixed, case-sensitive list.

    >>> run = paragraph.add_run()
    >>> font = run.font
    >>> font.highlight
    None
    >>> font.highlight = 'yellow'
    >>> font.highlight
    'yellow'
    >>> font.highlight = 'cyan'
    >>> font.highlight
    'cyan'
    >>> font.highlight = 'darkRed'
    >>> font.highlight
    'darkRed'
    >>> font.highlight = 'Yellow'
    >>> font.highlight
    None
    >>> font.highlight = 'YELLOW'
    >>> font.highlight
    None


Enumerations
------------


I was unable to locate an enumeration for the HighlightColor on MSDN.  From exhaustive selection in Word 2010, I have come up with the following list::

'yellow', 'green', 'cyan', 'magenta', 'blue', 'red', 'darkBlue', 'darkCyan', 'darkGreen', 'darkMagenta', 'darkRed', 'darkYellow', 'darkGray', 'lightGray', 'black'

These values ARE case-sensitive.  Other variations cause an error when the resulting document is loaded in Word. 


Specimen XML
------------

.. highlight:: xml

Baseline run::

  <w:r>
    <w:t xml:space="preserve">Black text, White background </w:t>
  </w:r>

Blue text, Green Highlight::

  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Courier New" w:hAnsi="Courier New" w:cs="Courier New"/>
      <w:color w:val="0000FF"/>
      <w:sz w:val="24"/>
      <w:szCs w:val="24"/>
      <w:highlight w:val="green"/>
    </w:rPr>
    <w:t xml:space="preserve">Blue text on Green background </w:t>
  </w:r>


Schema excerpt
--------------

Sorry, I have no idea how to proceed here.  The Schema presented in font Analysis Document includes mention of the highlight property.

.. highlight:: xml

::




