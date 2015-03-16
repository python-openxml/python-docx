
Settings part
=============

In WordprocessingML, document-level settings are defined in the
`settings.xml` part. There are 98 distinct settings, all of which are
optional (according to the spec at least).

The API does not provide for direct access to the settings part. A |Settings|
proxy object is available on the :attr:`.Document.settings` property and
provides access to the document-level settings. The |Document| object obtains
access via its document part. |DocumentPart| brokers all access to the
settings part.


Candidate Protocol
------------------

.. highlight:: python

::

  >>> document = Document()
  >>> document.settings
  <docx.settings.Settings object at 0xdeadbeef4>


Schema Excerpts
---------------

.. highlight:: xml

::

  <xsd:complexType name="CT_Settings">
    <xsd:sequence>
      <xsd:element name="writeProtection"            type="CT_WriteProtection" minOccurs="0"/>
      <xsd:element name="view"                       type="CT_View"            minOccurs="0"/>
      <xsd:element name="zoom"                       type="CT_Zoom"            minOccurs="0"/>
      <xsd:element name="removePersonalInformation"  type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="removeDateAndTime"          type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="doNotDisplayPageBoundaries" type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="displayBackgroundShape"     type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="printPostScriptOverText"    type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="printFractionalCharacterWidth" type="CT_OnOff"        minOccurs="0"/>
      <xsd:element name="printFormsData"             type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="embedTrueTypeFonts"         type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="embedSystemFonts"           type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="saveSubsetFonts"            type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="saveFormsData"              type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="mirrorMargins"              type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="alignBordersAndEdges"       type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="bordersDoNotSurroundHeader" type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="bordersDoNotSurroundFooter" type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="gutterAtTop"                type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="hideSpellingErrors"         type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="hideGrammaticalErrors"      type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="activeWritingStyle"         type="CT_WritingStyle"    minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="proofState"                 type="CT_Proof"           minOccurs="0"/>
      <xsd:element name="formsDesign"                type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="attachedTemplate"           type="CT_Rel"             minOccurs="0"/>
      <xsd:element name="linkStyles"                 type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="stylePaneFormatFilter"      type="CT_StylePaneFilter" minOccurs="0"/>
      <xsd:element name="stylePaneSortMethod"        type="CT_StyleSort"       minOccurs="0"/>
      <xsd:element name="documentType"               type="CT_DocType"         minOccurs="0"/>
      <xsd:element name="mailMerge"                  type="CT_MailMerge"       minOccurs="0"/>
      <xsd:element name="revisionView"               type="CT_TrackChangesView" minOccurs="0"/>
      <xsd:element name="trackRevisions"             type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="doNotTrackMoves"            type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="doNotTrackFormatting"       type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="documentProtection"         type="CT_DocProtect"      minOccurs="0"/>
      <xsd:element name="autoFormatOverride"         type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="styleLockTheme"             type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="styleLockQFSet"             type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="defaultTabStop"             type="CT_TwipsMeasure"    minOccurs="0"/>
      <xsd:element name="autoHyphenation"            type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="consecutiveHyphenLimit"     type="CT_DecimalNumber"   minOccurs="0"/>
      <xsd:element name="hyphenationZone"            type="CT_TwipsMeasure"    minOccurs="0"/>
      <xsd:element name="doNotHyphenateCaps"         type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="showEnvelope"               type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="summaryLength"              type="CT_DecimalNumberOrPrecent" minOccurs="0"/>
      <xsd:element name="clickAndTypeStyle"          type="CT_String"          minOccurs="0"/>
      <xsd:element name="defaultTableStyle"          type="CT_String"          minOccurs="0"/>
      <xsd:element name="evenAndOddHeaders"          type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="bookFoldRevPrinting"        type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="bookFoldPrinting"           type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="bookFoldPrintingSheets"      type="CT_DecimalNumber"   minOccurs="0"/>
      <xsd:element name="drawingGridHorizontalSpacing"        type="CT_TwipsMeasure"  minOccurs="0"/>
      <xsd:element name="drawingGridVerticalSpacing"          type="CT_TwipsMeasure"  minOccurs="0"/>
      <xsd:element name="displayHorizontalDrawingGridEvery"   type="CT_DecimalNumber" minOccurs="0"/>
      <xsd:element name="displayVerticalDrawingGridEvery"     type="CT_DecimalNumber" minOccurs="0"/>
      <xsd:element name="doNotUseMarginsForDrawingGridOrigin" type="CT_OnOff"         minOccurs="0"/>
      <xsd:element name="drawingGridHorizontalOrigin"         type="CT_TwipsMeasure"  minOccurs="0"/>
      <xsd:element name="drawingGridVerticalOrigin"  type="CT_TwipsMeasure"    minOccurs="0"/>
      <xsd:element name="doNotShadeFormData"         type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="noPunctuationKerning"       type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="characterSpacingControl"    type="CT_CharacterSpacing" minOccurs="0"/>
      <xsd:element name="printTwoOnOne"              type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="strictFirstAndLastChars"    type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="noLineBreaksAfter"          type="CT_Kinsoku"         minOccurs="0"/>
      <xsd:element name="noLineBreaksBefore"         type="CT_Kinsoku"         minOccurs="0"/>
      <xsd:element name="savePreviewPicture"         type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="doNotValidateAgainstSchema" type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="saveInvalidXml"             type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="ignoreMixedContent"         type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="alwaysShowPlaceholderText"  type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="doNotDemarcateInvalidXml"   type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="saveXmlDataOnly"            type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="useXSLTWhenSaving"          type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="saveThroughXslt"            type="CT_SaveThroughXslt" minOccurs="0"/>
      <xsd:element name="showXMLTags"                type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="alwaysMergeEmptyNamespace"  type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="updateFields"               type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="hdrShapeDefaults"           type="CT_ShapeDefaults"   minOccurs="0"/>
      <xsd:element name="footnotePr"                 type="CT_FtnDocProps"     minOccurs="0"/>
      <xsd:element name="endnotePr"                  type="CT_EdnDocProps"     minOccurs="0"/>
      <xsd:element name="compat"                     type="CT_Compat"          minOccurs="0"/>
      <xsd:element name="docVars"                    type="CT_DocVars"         minOccurs="0"/>
      <xsd:element name="rsids"                      type="CT_DocRsids"        minOccurs="0"/>
      <xsd:element  ref="m:mathPr"                                             minOccurs="0"/>
      <xsd:element name="attachedSchema"             type="CT_String"          minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element name="themeFontLang"              type="CT_Language"        minOccurs="0"/>
      <xsd:element name="clrSchemeMapping"           type="CT_ColorSchemeMapping" minOccurs="0"/>
      <xsd:element name="doNotIncludeSubdocsInStats" type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="doNotAutoCompressPictures"  type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="forceUpgrade"               type="CT_Empty"           minOccurs="0"/>
      <xsd:element name="captions"                   type="CT_Captions"        minOccurs="0"/>
      <xsd:element name="readModeInkLockDown"        type="CT_ReadingModeInkLockDown" minOccurs="0"/>
      <xsd:element name="smartTagType"               type="CT_SmartTagType"    minOccurs="0" maxOccurs="unbounded"/>
      <xsd:element  ref="sl:schemaLibrary"                                     minOccurs="0"/>
      <xsd:element name="shapeDefaults"              type="CT_ShapeDefaults"   minOccurs="0"/>
      <xsd:element name="doNotEmbedSmartTags"        type="CT_OnOff"           minOccurs="0"/>
      <xsd:element name="decimalSymbol"              type="CT_String"          minOccurs="0"/>
      <xsd:element name="listSeparator"              type="CT_String"          minOccurs="0"/>
    </xsd:sequence>
  </xsd:complexType>
