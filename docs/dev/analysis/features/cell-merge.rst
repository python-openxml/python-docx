
Table Cells Merge
=================
 
In Word, table cells can be merged with the following restrictions: 

* Only rectangular selections are supported.
* If the to-be-merged selection contains previously merged cells, then that
  selection must extend the contained merged cells area.

The area to be merged is determined by the two opposite corner cells of that
area. The to-be-merged area can span across multiple rows and/or columns.

For merging horizontally, the ``w:gridSpan`` table cell property of the
leftmost cell of the area to be merged is set to a value of type
``w:ST_DecimalNumber`` corresponding to the number of columns the cell
should span across. Only that leftmost cell is preserved; the other cells
of the merge selection are deleted. Note that having the ``w:gridSpan``
element is only required if there exists another table row using a
different column layout. When the same column layout is shared across all
the rows, then the ``w:gridSpan`` is replaced by a ``w:tcW`` element
specifying the width of each column. For example, if the table consists of
just one row and we merge all of its cells, then only the leftmost cell is
kept, and its width is ajusted so that it is equal to the combined width of
the cells merged.

For merging vertically, the ``w:vMerge`` table cell property of the
uppermost cell of the column is set to the value "restart" of type
``w:ST_Merge``. The following, lower cells included in the vertical merge
must have the ``w:vMerge`` element present in their cell property
(``w:TcPr``) element. Its value should be set to "continue", although Word
uses empty valued ``w:vMerge`` elements. A vertical merge ends as soon as a
cell ``w:TcPr`` element lacks the ``w:vMerge`` element. Similarly to the
``w:gridSpan`` element, the ``w:vMerge`` elements are only required when
the table's layout is not uniform across its different columns. In the case
it is, only the topmost cell is kept; the other lower cells in the merged
area are deleted along with their ``w:vMerge`` elements and the
``w:trHeight`` table row property is used to specify the combined heigth of
the merged cells.


Additionnal notes
~~~~~~~~~~~~~~~~~

Word cannot report how many cells a specific column contains if one or more 
cells in this column have a different width due to having been merged with 
another cell. 

Similarly, Word cannot report how many cells a specific row contains if one or
more cells of that row have been vertically merged.


Candidate protocol -- cell.merge()
----------------------------------

The following interactive session demonstrates the protocol for merging table
cells::

    >>> table = doc.add_table(5,5)
    >>> table.rows[0].cells[0].merge(table.rows[3].cells[3])


Specimen XML
------------

.. highlight:: xml 

A 3 x 3 table where an area defined by the 2 x 2 topleft cells has been
merged, demonstrating the combined use of the ``w:gridSpan`` as well as the 
``w:vMerge`` elements, as produced by Word::

   <w:tbl>
      <w:tblPr>
         <w:tblStyle w:val="Grilledutableau" />
         <w:tblW w:w="0" w:type="auto" />
         <w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="1" w:lastColumn="0" w:noHBand="0" w:noVBand="1" />
      </w:tblPr>
      <w:tblGrid>
         <w:gridCol w:w="3192" />
         <w:gridCol w:w="3192" />
         <w:gridCol w:w="3192" />
      </w:tblGrid>
      <w:tr w:rsidR="00AC2064" w:rsidTr="00F528C2">
         <w:tc>
            <w:tcPr>
               <w:tcW w:w="6384" w:type="dxa" />
               <w:gridSpan w:val="2" />
               <w:vMerge w:val="restart" />
            </w:tcPr>
            <w:p w:rsidR="00AC2064" w:rsidRDefault="00AC2064">
               <w:bookmarkStart w:id="0" w:name="_GoBack" w:colFirst="0" w:colLast="0" />
            </w:p>
         </w:tc>
         <w:tc>
            <w:tcPr>
               <w:tcW w:w="3192" w:type="dxa" />
            </w:tcPr>
            <w:p w:rsidR="00AC2064" w:rsidRDefault="00AC2064" />
         </w:tc>
      </w:tr>
      <w:bookmarkEnd w:id="0" />
      <w:tr w:rsidR="00AC2064" w:rsidTr="00F528C2">
         <w:tc>
            <w:tcPr>
               <w:tcW w:w="6384" w:type="dxa" />
               <w:gridSpan w:val="2" />
               <w:vMerge />
            </w:tcPr>
            <w:p w:rsidR="00AC2064" w:rsidRDefault="00AC2064" />
         </w:tc>
         <w:tc>
            <w:tcPr>
               <w:tcW w:w="3192" w:type="dxa" />
            </w:tcPr>
            <w:p w:rsidR="00AC2064" w:rsidRDefault="00AC2064" />
         </w:tc>
      </w:tr>
      <w:tr w:rsidR="00AC2064" w:rsidTr="00AC2064">
         <w:tc>
            <w:tcPr>
               <w:tcW w:w="3192" w:type="dxa" />
            </w:tcPr>
            <w:p w:rsidR="00AC2064" w:rsidRDefault="00AC2064" />
         </w:tc>
         <w:tc>
            <w:tcPr>
               <w:tcW w:w="3192" w:type="dxa" />
            </w:tcPr>
            <w:p w:rsidR="00AC2064" w:rsidRDefault="00AC2064" />
         </w:tc>
         <w:tc>
            <w:tcPr>
               <w:tcW w:w="3192" w:type="dxa" />
            </w:tcPr>
            <w:p w:rsidR="00AC2064" w:rsidRDefault="00AC2064" />
         </w:tc>
      </w:tr>
   </w:tbl>


Schema excerpt
--------------

.. highlight:: xml

::

   <xsd:simpleType name="ST_Merge">
      <xsd:restriction base="xsd:string">
         <xsd:enumeration value="continue"/>
         <xsd:enumeration value="restart"/>
      </xsd:restriction>
   </xsd:simpleType>

   <xsd:complexType name="CT_VMerge">
      <xsd:attribute name="val" type="ST_Merge"/>
   </xsd:complexType>

   
Ressources
----------

* `Cell.Merge Method on MSDN`_
* `w:gridSpan reference from Datypic`_
* `w:vMerge reference from Datypic`_
* `w:CT_VMerge reference from Datypic`_
* `w:ST_Merge reference from Datypic`_

.. _`Cell.Merge Method on MSDN`:
   http://msdn.microsoft.com/en-us/library/office/ff821310%28v=office.15%29.aspx
 
.. _`w:gridSpan reference from Datypic`:
   http://www.datypic.com/sc/ooxml/e-w_gridSpan-1.html
   
.. _`w:vMerge reference from Datypic`:
   http://www.datypic.com/sc/ooxml/e-w_vMerge-1.html
   
.. _`w:CT_VMerge reference from Datypic`:
   http://www.datypic.com/sc/ooxml/t-w_CT_VMerge.html

.. _`w:ST_Merge reference from Datypic`:
   http://www.datypic.com/sc/ooxml/t-w_ST_Merge.html


Relevant sections in the ISO Spec
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* 17.4.17 gridSpan (Grid Columns Spanned by Current Table Cell)
* 17.4.84 vMerge (Vertically Merged Cell)
* 17.18.57 ST_Merge (Merged Cell Type)
