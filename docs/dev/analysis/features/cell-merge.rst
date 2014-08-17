
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
the rows, then the ``w:gridSpan`` can be replaced by a ``w:tcW`` element
specifying the width of the column. For example, if the table consists of
just one row and we merge all of its cells, then only the leftmost cell is
kept, and its width is ajusted so that it equals the combined width of
the cells merged.

For merging vertically, the ``w:vMerge`` table cell property of the
uppermost cell of the column is set to the value "restart" of type
``w:ST_Merge``. The following, lower cells included in the vertical merge
must have the ``w:vMerge`` element present in their cell property
(``w:TcPr``) element. Its value should be set to "continue", although it is
not necessary to explicitely define it, as it is the default value. A
vertical merge ends as soon as a cell ``w:TcPr`` element lacks the
``w:vMerge`` element. Similarly to the ``w:gridSpan`` element, the
``w:vMerge`` elements are only required when the table's layout is not
uniform across its different columns. In the case it is, only the topmost
cell is kept; the other lower cells in the merged area are deleted along
with their ``w:vMerge`` elements and the ``w:trHeight`` table row property
is used to specify the combined height of the merged cells.


Word specific behavior
~~~~~~~~~~~~~~~~~~~~~~

Word cannot access the columns of a table if two or more cells from that
table have been horizontally merged. Similarly, Word cannot access the rows
of a table if two or more cells from that table have been vertically merged.

Word resizes a table when a cell is refered by an out-of-bounds row index.
If the column identifier is out of bounds, an exception is raised.

An exception is raised when attempting to merge cells from different tables.


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
       <w:tblW w:w="0" w:type="auto" />
    </w:tblPr>
    <w:tblGrid>
       <w:gridCol w:w="3192" />
       <w:gridCol w:w="3192" />
       <w:gridCol w:w="3192" />
    </w:tblGrid>
    <w:tr>
       <w:tc>
          <w:tcPr>
             <w:tcW w:w="6384" w:type="dxa" />
             <w:gridSpan w:val="2" />
             <w:vMerge w:val="restart" />
          </w:tcPr>
       </w:tc>
       <w:tc>
          <w:tcPr>
             <w:tcW w:w="3192" w:type="dxa" />
          </w:tcPr>
       </w:tc>
    </w:tr>
    <w:tr>
       <w:tc>
          <w:tcPr>
             <w:tcW w:w="6384" w:type="dxa" />
             <w:gridSpan w:val="2" />
             <w:vMerge />
          </w:tcPr>
       </w:tc>
       <w:tc>
          <w:tcPr>
             <w:tcW w:w="3192" w:type="dxa" />
          </w:tcPr>
       </w:tc>
    </w:tr>
    <w:tr>
       <w:tc>
          <w:tcPr>
             <w:tcW w:w="3192" w:type="dxa" />
          </w:tcPr>
       </w:tc>
       <w:tc>
          <w:tcPr>
             <w:tcW w:w="3192" w:type="dxa" />
          </w:tcPr>
       </w:tc>
       <w:tc>
          <w:tcPr>
             <w:tcW w:w="3192" w:type="dxa" />
          </w:tcPr>
       </w:tc>
    </w:tr>
  </w:tbl>


Schema excerpt
--------------

.. highlight:: xml

::

  <xsd:complexType name="CT_TcPr">  <!-- denormalized -->
    <xsd:sequence>
      <xsd:element name="cnfStyle"             type="CT_Cnf"           minOccurs="0"/>
      <xsd:element name="tcW"                  type="CT_TblWidth"      minOccurs="0"/>
      <xsd:element name="gridSpan"             type="CT_DecimalNumber" minOccurs="0"/>
      <xsd:element name="hMerge"               type="CT_HMerge"        minOccurs="0"/>
      <xsd:element name="vMerge"               type="CT_VMerge"        minOccurs="0"/>
      <xsd:element name="tcBorders"            type="CT_TcBorders"     minOccurs="0"/>
      <xsd:element name="shd"                  type="CT_Shd"           minOccurs="0"/>
      <xsd:element name="noWrap"               type="CT_OnOff"         minOccurs="0"/>
      <xsd:element name="tcMar"                type="CT_TcMar"         minOccurs="0"/>
      <xsd:element name="textDirection"        type="CT_TextDirection" minOccurs="0"/>
      <xsd:element name="tcFitText"            type="CT_OnOff"         minOccurs="0"/>
      <xsd:element name="vAlign"               type="CT_VerticalJc"    minOccurs="0"/>
      <xsd:element name="hideMark"             type="CT_OnOff"         minOccurs="0"/>
      <xsd:element name="headers"              type="CT_Headers"       minOccurs="0"/>
      <xsd:choice                                                      minOccurs="0"/>
        <xsd:element name="cellIns"            type="CT_TrackChange"/>
        <xsd:element name="cellDel"            type="CT_TrackChange"/>
        <xsd:element name="cellMerge"          type="CT_CellMergeTrackChange"/>
      </xsd:choice>
      <xsd:element name="tcPrChange"           type="CT_TcPrChange"    minOccurs="0"/>
    </xsd:sequence>
  </xsd:complexType>

  <xsd:complexType name="CT_DecimalNumber">
    <xsd:attribute name="val" type="ST_DecimalNumber" use="required"/>
  </xsd:complexType>
  
  <xsd:simpleType name="ST_DecimalNumber">
     <xsd:restriction base="xsd:integer"/>
  </xsd:simpleType>
 
  <xsd:complexType name="CT_VMerge">
    <xsd:attribute name="val" type="ST_Merge"/>
  </xsd:complexType>

 <xsd:simpleType name="ST_Merge">
    <xsd:restriction base="xsd:string">
       <xsd:enumeration value="continue"/>
       <xsd:enumeration value="restart"/>
    </xsd:restriction>
  </xsd:simpleType>


Ressources
----------

* `Cell.Merge Method on MSDN`_

.. _`Cell.Merge Method on MSDN`:
   http://msdn.microsoft.com/en-us/library/office/ff821310%28v=office.15%29.aspx

Relevant sections in the ISO Spec
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
* 17.4.17 gridSpan (Grid Columns Spanned by Current Table Cell)
* 17.4.84 vMerge (Vertically Merged Cell)
* 17.18.57 ST_Merge (Merged Cell Type)
