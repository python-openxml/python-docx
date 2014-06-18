# encoding: utf-8

"""
Test suite for docx.oxml.xmlchemy
"""

from __future__ import absolute_import, print_function, unicode_literals

import pytest

from docx.compat import Unicode
from docx.oxml import parse_xml, register_element_cls
from docx.oxml.exceptions import InvalidXmlError
from docx.oxml.ns import qn
from docx.oxml.simpletypes import BaseIntType
from docx.oxml.xmlchemy import (
    BaseOxmlElement, Choice, serialize_for_reading, OneOrMore, OneAndOnlyOne,
    OptionalAttribute, RequiredAttribute, ZeroOrMore, ZeroOrOne,
    ZeroOrOneChoice, XmlString
)

from ..unitdata import BaseBuilder
from .unitdata.text import a_b, a_u, an_i, an_rPr


class DescribeBaseOxmlElement(object):

    def it_can_find_the_first_of_its_children_named_in_a_sequence(
            self, first_fixture):
        element, tagnames, matching_child = first_fixture
        assert element.first_child_found_in(*tagnames) is matching_child

    def it_can_insert_an_element_before_named_successors(
            self, insert_fixture):
        element, child, tagnames, expected_xml = insert_fixture
        element.insert_element_before(child, *tagnames)
        assert element.xml == expected_xml

    def it_can_remove_all_children_with_name_in_sequence(
            self, remove_fixture):
        element, tagnames, expected_xml = remove_fixture
        element.remove_all(*tagnames)
        assert element.xml == expected_xml

    # fixtures ---------------------------------------------

    @pytest.fixture(params=[
        ('biu', 'iu',  'i'),
        ('bu',  'iu',  'u'),
        ('bi',  'u',   None),
        ('b',   'iu',  None),
        ('iu',  'biu', 'i'),
        ('',    'biu', None),
    ])
    def first_fixture(self, request):
        present, matching, match = request.param
        element = self.rPr_bldr(present).element
        tagnames = self.nsptags(matching)
        matching_child = element.find(qn('w:%s' % match)) if match else None
        return element, tagnames, matching_child

    @pytest.fixture(params=[
        ('iu', 'b', 'iu', 'biu'),
        ('u',  'b', 'iu', 'bu'),
        ('',   'b', 'iu', 'b'),
        ('bu', 'i', 'u',  'biu'),
        ('bi', 'u', '',   'biu'),
    ])
    def insert_fixture(self, request):
        present, new, successors, after = request.param
        element = self.rPr_bldr(present).element
        child = {
            'b': a_b(), 'i': an_i(), 'u': a_u()
        }[new].with_nsdecls().element
        tagnames = [('w:%s' % char) for char in successors]
        expected_xml = self.rPr_bldr(after).xml()
        return element, child, tagnames, expected_xml

    @pytest.fixture(params=[
        ('biu', 'b', 'iu'), ('biu', 'bi', 'u'), ('bbiiuu',  'i',   'bbuu'),
        ('biu', 'i', 'bu'), ('biu', 'bu', 'i'), ('bbiiuu',   '', 'bbiiuu'),
        ('biu', 'u', 'bi'), ('biu', 'ui', 'b'), ('bbiiuu', 'bi',     'uu'),
        ('bu',  'i', 'bu'), ('',    'ui',  ''),
    ])
    def remove_fixture(self, request):
        present, remove, after = request.param
        element = self.rPr_bldr(present).element
        tagnames = self.nsptags(remove)
        expected_xml = self.rPr_bldr(after).xml()
        return element, tagnames, expected_xml

    # fixture components ---------------------------------------------

    def nsptags(self, letters):
        return [('w:%s' % letter) for letter in letters]

    def rPr_bldr(self, children):
        rPr_bldr = an_rPr().with_nsdecls()
        for char in children:
            if char == 'b':
                rPr_bldr.with_child(a_b())
            elif char == 'i':
                rPr_bldr.with_child(an_i())
            elif char == 'u':
                rPr_bldr.with_child(a_u())
            else:
                raise NotImplementedError("got '%s'" % char)
        return rPr_bldr


class DescribeSerializeForReading(object):

    def it_pretty_prints_an_lxml_element(self, pretty_fixture):
        element, expected_xml_text = pretty_fixture
        xml_text = serialize_for_reading(element)
        assert xml_text == expected_xml_text

    def it_returns_unicode_text(self, type_fixture):
        element = type_fixture
        xml_text = serialize_for_reading(element)
        assert isinstance(xml_text, Unicode)

    # fixtures ---------------------------------------------

    @pytest.fixture
    def pretty_fixture(self, element):
        expected_xml_text = (
            '<foø>\n'
            '  <bår>text</bår>\n'
            '</foø>\n'
        )
        return element, expected_xml_text

    @pytest.fixture
    def type_fixture(self, element):
        return element

    # fixture components -----------------------------------

    @pytest.fixture
    def element(self):
        return parse_xml('<foø><bår>text</bår></foø>')


class DescribeXmlString(object):

    def it_parses_a_line_to_help_compare(self, parse_fixture):
        """
        This internal function is important to test separately because if it
        doesn't parse a line properly, false equality can result.
        """
        line, expected_front, expected_attrs = parse_fixture[:3]
        expected_close, expected_text = parse_fixture[3:]
        front, attrs, close, text = XmlString._parse_line(line)
        # print("'%s' '%s' '%s' %s" % (
        #     front, attrs, close, ('%s' % text) if text else text))
        assert front == expected_front
        assert attrs == expected_attrs
        assert close == expected_close
        assert text == expected_text

    def it_knows_if_two_xml_lines_are_equivalent(self, xml_line_case):
        line, other, differs = xml_line_case
        xml = XmlString(line)
        assert xml == other
        assert xml != differs

    # fixtures ---------------------------------------------

    @pytest.fixture(params=[
        ('<a>text</a>',  '<a',   '',       '>',  'text</a>'),
        ('<a:f/>',       '<a:f', '',       '/>', None),
        ('<a:f b="c"/>', '<a:f', ' b="c"', '/>', None),
        ('<a:f>t</a:f>', '<a:f', '',       '>',  't</a:f>'),
        ('<dcterms:created xsi:type="dcterms:W3CDTF">2013-12-23T23:15:00Z</d'
         'cterms:created>', '<dcterms:created', ' xsi:type="dcterms:W3CDTF"',
         '>', '2013-12-23T23:15:00Z</dcterms:created>'),
    ])
    def parse_fixture(self, request):
        line, front, attrs, close, text = request.param
        return line, front, attrs, close, text

    @pytest.fixture(params=[
        'simple_elm', 'nsp_tagname', 'indent', 'attrs', 'nsdecl_order',
        'closing_elm',
    ])
    def xml_line_case(self, request):
        cases = {
            'simple_elm': (
                '<name/>',
                '<name/>',
                '<name>',
            ),
            'nsp_tagname': (
                '<xyz:name/>',
                '<xyz:name/>',
                '<abc:name/>',
            ),
            'indent': (
                '  <xyz:name/>',
                '  <xyz:name/>',
                '<xyz:name/>',
            ),
            'attrs': (
                '  <abc:Name foo="bar" bar="foo">',
                '  <abc:Name bar="foo" foo="bar">',
                '  <abc:Name far="boo" foo="bar">',
            ),
            'nsdecl_order': (
                '    <name xmlns:a="http://ns/1" xmlns:b="http://ns/2"/>',
                '    <name xmlns:b="http://ns/2" xmlns:a="http://ns/1"/>',
                '    <name xmlns:b="http://ns/2" xmlns:a="http://ns/1">',
            ),
            'closing_elm': (
                '</xyz:name>',
                '</xyz:name>',
                '<xyz:name>',
            ),
        }
        line, other, differs = cases[request.param]
        return line, other, differs


class DescribeChoice(object):

    def it_adds_a_getter_property_for_the_choice_element(
            self, getter_fixture):
        parent, expected_choice = getter_fixture
        assert parent.choice is expected_choice

    def it_adds_a_creator_method_for_the_child_element(self, new_fixture):
        parent, expected_xml = new_fixture
        choice = parent._new_choice()
        assert choice.xml == expected_xml

    def it_adds_an_insert_method_for_the_child_element(self, insert_fixture):
        parent, choice, expected_xml = insert_fixture
        parent._insert_choice(choice)
        assert parent.xml == expected_xml
        assert parent._insert_choice.__doc__.startswith(
            'Return the passed ``<w:choice>`` '
        )

    def it_adds_an_add_method_for_the_child_element(self, add_fixture):
        parent, expected_xml = add_fixture
        choice = parent._add_choice()
        assert parent.xml == expected_xml
        assert isinstance(choice, CT_Choice)
        assert parent._add_choice.__doc__.startswith(
            'Add a new ``<w:choice>`` child element '
        )

    def it_adds_a_get_or_change_to_method_for_the_child_element(
            self, get_or_change_to_fixture):
        parent, expected_xml = get_or_change_to_fixture
        choice = parent.get_or_change_to_choice()
        assert isinstance(choice, CT_Choice)
        assert parent.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def add_fixture(self):
        parent = self.parent_bldr().element
        expected_xml = self.parent_bldr('choice').xml()
        return parent, expected_xml

    @pytest.fixture(params=[
        ('choice2', 'choice'),
        (None,      'choice'),
        ('choice',  'choice'),
    ])
    def get_or_change_to_fixture(self, request):
        before_member_tag, after_member_tag = request.param
        parent = self.parent_bldr(before_member_tag).element
        expected_xml = self.parent_bldr(after_member_tag).xml()
        return parent, expected_xml

    @pytest.fixture(params=['choice', None])
    def getter_fixture(self, request):
        choice_tag = request.param
        parent = self.parent_bldr(choice_tag).element
        expected_choice = parent.find(qn('w:choice'))  # None if not found
        return parent, expected_choice

    @pytest.fixture
    def insert_fixture(self):
        parent = (
            a_parent().with_nsdecls().with_child(
                an_oomChild()).with_child(
                an_oooChild())
        ).element
        choice = a_choice().with_nsdecls().element
        expected_xml = (
            a_parent().with_nsdecls().with_child(
                a_choice()).with_child(
                an_oomChild()).with_child(
                an_oooChild())
        ).xml()
        return parent, choice, expected_xml

    @pytest.fixture
    def new_fixture(self):
        parent = self.parent_bldr().element
        expected_xml = a_choice().with_nsdecls().xml()
        return parent, expected_xml

    # fixture components ---------------------------------------------

    def parent_bldr(self, choice_tag=None):
        parent_bldr = a_parent().with_nsdecls()
        if choice_tag == 'choice':
            parent_bldr.with_child(a_choice())
        if choice_tag == 'choice2':
            parent_bldr.with_child(a_choice2())
        return parent_bldr


class DescribeOneAndOnlyOne(object):

    def it_adds_a_getter_property_for_the_child_element(self, getter_fixture):
        parent, oooChild = getter_fixture
        assert parent.oooChild is oooChild

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def getter_fixture(self):
        parent = a_parent().with_nsdecls().with_child(an_oooChild()).element
        oooChild = parent.find(qn('w:oooChild'))
        return parent, oooChild


class DescribeOneOrMore(object):

    def it_adds_a_getter_property_for_the_child_element_list(
            self, getter_fixture):
        parent, oomChild = getter_fixture
        assert parent.oomChild_lst[0] is oomChild

    def it_adds_a_creator_method_for_the_child_element(self, new_fixture):
        parent, expected_xml = new_fixture
        oomChild = parent._new_oomChild()
        assert oomChild.xml == expected_xml

    def it_adds_an_insert_method_for_the_child_element(self, insert_fixture):
        parent, oomChild, expected_xml = insert_fixture
        parent._insert_oomChild(oomChild)
        assert parent.xml == expected_xml
        assert parent._insert_oomChild.__doc__.startswith(
            'Return the passed ``<w:oomChild>`` '
        )

    def it_adds_a_private_add_method_for_the_child_element(self, add_fixture):
        parent, expected_xml = add_fixture
        oomChild = parent._add_oomChild()
        assert parent.xml == expected_xml
        assert isinstance(oomChild, CT_OomChild)
        assert parent._add_oomChild.__doc__.startswith(
            'Add a new ``<w:oomChild>`` child element '
        )

    def it_adds_a_public_add_method_for_the_child_element(self, add_fixture):
        parent, expected_xml = add_fixture
        oomChild = parent.add_oomChild()
        assert parent.xml == expected_xml
        assert isinstance(oomChild, CT_OomChild)
        assert parent._add_oomChild.__doc__.startswith(
            'Add a new ``<w:oomChild>`` child element '
        )

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def add_fixture(self):
        parent = self.parent_bldr(False).element
        expected_xml = self.parent_bldr(True).xml()
        return parent, expected_xml

    @pytest.fixture
    def getter_fixture(self):
        parent = self.parent_bldr(True).element
        oomChild = parent.find(qn('w:oomChild'))
        return parent, oomChild

    @pytest.fixture
    def insert_fixture(self):
        parent = (
            a_parent().with_nsdecls().with_child(
                an_oooChild()).with_child(
                a_zomChild()).with_child(
                a_zooChild())
        ).element
        oomChild = an_oomChild().with_nsdecls().element
        expected_xml = (
            a_parent().with_nsdecls().with_child(
                an_oomChild()).with_child(
                an_oooChild()).with_child(
                a_zomChild()).with_child(
                a_zooChild())
        ).xml()
        return parent, oomChild, expected_xml

    @pytest.fixture
    def new_fixture(self):
        parent = self.parent_bldr(False).element
        expected_xml = an_oomChild().with_nsdecls().xml()
        return parent, expected_xml

    # fixture components ---------------------------------------------

    def parent_bldr(self, oomChild_is_present):
        parent_bldr = a_parent().with_nsdecls()
        if oomChild_is_present:
            parent_bldr.with_child(an_oomChild())
        return parent_bldr


class DescribeOptionalAttribute(object):

    def it_adds_a_getter_property_for_the_attr_value(self, getter_fixture):
        parent, optAttr_python_value = getter_fixture
        assert parent.optAttr == optAttr_python_value

    def it_adds_a_setter_property_for_the_attr(self, setter_fixture):
        parent, value, expected_xml = setter_fixture
        parent.optAttr = value
        assert parent.xml == expected_xml

    def it_adds_a_docstring_for_the_property(self):
        assert CT_Parent.optAttr.__doc__.startswith(
            "ST_IntegerType type-converted value of "
        )

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def getter_fixture(self):
        parent = a_parent().with_nsdecls().with_optAttr('24').element
        return parent, 24

    @pytest.fixture(params=[36, None])
    def setter_fixture(self, request):
        value = request.param
        parent = a_parent().with_nsdecls().with_optAttr('42').element
        if value is None:
            expected_xml = a_parent().with_nsdecls().xml()
        else:
            expected_xml = a_parent().with_nsdecls().with_optAttr(value).xml()
        return parent, value, expected_xml


class DescribeRequiredAttribute(object):

    def it_adds_a_getter_property_for_the_attr_value(self, getter_fixture):
        parent, reqAttr_python_value = getter_fixture
        assert parent.reqAttr == reqAttr_python_value

    def it_adds_a_setter_property_for_the_attr(self, setter_fixture):
        parent, value, expected_xml = setter_fixture
        parent.reqAttr = value
        assert parent.xml == expected_xml

    def it_adds_a_docstring_for_the_property(self):
        assert CT_Parent.reqAttr.__doc__.startswith(
            "ST_IntegerType type-converted value of "
        )

    def it_raises_on_get_when_attribute_not_present(self):
        parent = a_parent().with_nsdecls().element
        with pytest.raises(InvalidXmlError):
            parent.reqAttr

    def it_raises_on_assign_invalid_value(self, invalid_assign_fixture):
        parent, value, expected_exception = invalid_assign_fixture
        with pytest.raises(expected_exception):
            parent.reqAttr = value

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def getter_fixture(self):
        parent = a_parent().with_nsdecls().with_reqAttr('42').element
        return parent, 42

    @pytest.fixture(params=[
        (None, TypeError),
        (-4,   ValueError),
        ('2',  TypeError),
    ])
    def invalid_assign_fixture(self, request):
        invalid_value, expected_exception = request.param
        parent = a_parent().with_nsdecls().with_reqAttr(1).element
        return parent, invalid_value, expected_exception

    @pytest.fixture
    def setter_fixture(self):
        parent = a_parent().with_nsdecls().with_reqAttr('42').element
        value = 24
        expected_xml = a_parent().with_nsdecls().with_reqAttr(value).xml()
        return parent, value, expected_xml


class DescribeZeroOrMore(object):

    def it_adds_a_getter_property_for_the_child_element_list(
            self, getter_fixture):
        parent, zomChild = getter_fixture
        assert parent.zomChild_lst[0] is zomChild

    def it_adds_a_creator_method_for_the_child_element(self, new_fixture):
        parent, expected_xml = new_fixture
        zomChild = parent._new_zomChild()
        assert zomChild.xml == expected_xml

    def it_adds_an_insert_method_for_the_child_element(self, insert_fixture):
        parent, zomChild, expected_xml = insert_fixture
        parent._insert_zomChild(zomChild)
        assert parent.xml == expected_xml
        assert parent._insert_zomChild.__doc__.startswith(
            'Return the passed ``<w:zomChild>`` '
        )

    def it_adds_an_add_method_for_the_child_element(self, add_fixture):
        parent, expected_xml = add_fixture
        zomChild = parent._add_zomChild()
        assert parent.xml == expected_xml
        assert isinstance(zomChild, CT_ZomChild)
        assert parent._add_zomChild.__doc__.startswith(
            'Add a new ``<w:zomChild>`` child element '
        )

    def it_adds_a_public_add_method_for_the_child_element(self, add_fixture):
        parent, expected_xml = add_fixture
        zomChild = parent.add_zomChild()
        assert parent.xml == expected_xml
        assert isinstance(zomChild, CT_ZomChild)
        assert parent._add_zomChild.__doc__.startswith(
            'Add a new ``<w:zomChild>`` child element '
        )

    def it_removes_the_property_root_name_used_for_declaration(self):
        assert not hasattr(CT_Parent, 'zomChild')

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def add_fixture(self):
        parent = self.parent_bldr(False).element
        expected_xml = self.parent_bldr(True).xml()
        return parent, expected_xml

    @pytest.fixture
    def getter_fixture(self):
        parent = self.parent_bldr(True).element
        zomChild = parent.find(qn('w:zomChild'))
        return parent, zomChild

    @pytest.fixture
    def insert_fixture(self):
        parent = (
            a_parent().with_nsdecls().with_child(
                an_oomChild()).with_child(
                an_oooChild()).with_child(
                a_zooChild())
        ).element
        zomChild = a_zomChild().with_nsdecls().element
        expected_xml = (
            a_parent().with_nsdecls().with_child(
                an_oomChild()).with_child(
                an_oooChild()).with_child(
                a_zomChild()).with_child(
                a_zooChild())
        ).xml()
        return parent, zomChild, expected_xml

    @pytest.fixture
    def new_fixture(self):
        parent = self.parent_bldr(False).element
        expected_xml = a_zomChild().with_nsdecls().xml()
        return parent, expected_xml

    def parent_bldr(self, zomChild_is_present):
        parent_bldr = a_parent().with_nsdecls()
        if zomChild_is_present:
            parent_bldr.with_child(a_zomChild())
        return parent_bldr


class DescribeZeroOrOne(object):

    def it_adds_a_getter_property_for_the_child_element(self, getter_fixture):
        parent, zooChild = getter_fixture
        assert parent.zooChild is zooChild

    def it_adds_an_add_method_for_the_child_element(self, add_fixture):
        parent, expected_xml = add_fixture
        zooChild = parent._add_zooChild()
        assert parent.xml == expected_xml
        assert isinstance(zooChild, CT_ZooChild)
        assert parent._add_zooChild.__doc__.startswith(
            'Add a new ``<w:zooChild>`` child element '
        )

    def it_adds_an_insert_method_for_the_child_element(self, insert_fixture):
        parent, zooChild, expected_xml = insert_fixture
        parent._insert_zooChild(zooChild)
        assert parent.xml == expected_xml
        assert parent._insert_zooChild.__doc__.startswith(
            'Return the passed ``<w:zooChild>`` '
        )

    def it_adds_a_get_or_add_method_for_the_child_element(
            self, get_or_add_fixture):
        parent, expected_xml = get_or_add_fixture
        zooChild = parent.get_or_add_zooChild()
        assert isinstance(zooChild, CT_ZooChild)
        assert parent.xml == expected_xml

    def it_adds_a_remover_method_for_the_child_element(self, remove_fixture):
        parent, expected_xml = remove_fixture
        parent._remove_zooChild()
        assert parent.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def add_fixture(self):
        parent = self.parent_bldr(False).element
        expected_xml = self.parent_bldr(True).xml()
        return parent, expected_xml

    @pytest.fixture(params=[True, False])
    def getter_fixture(self, request):
        zooChild_is_present = request.param
        parent = self.parent_bldr(zooChild_is_present).element
        zooChild = parent.find(qn('w:zooChild'))  # None if not found
        return parent, zooChild

    @pytest.fixture(params=[True, False])
    def get_or_add_fixture(self, request):
        zooChild_is_present = request.param
        parent = self.parent_bldr(zooChild_is_present).element
        expected_xml = self.parent_bldr(True).xml()
        return parent, expected_xml

    @pytest.fixture
    def insert_fixture(self):
        parent = (
            a_parent().with_nsdecls().with_child(
                an_oomChild()).with_child(
                an_oooChild()).with_child(
                a_zomChild())
        ).element
        zooChild = a_zooChild().with_nsdecls().element
        expected_xml = (
            a_parent().with_nsdecls().with_child(
                an_oomChild()).with_child(
                an_oooChild()).with_child(
                a_zomChild()).with_child(
                a_zooChild())
        ).xml()
        return parent, zooChild, expected_xml

    @pytest.fixture(params=[True, False])
    def remove_fixture(self, request):
        zooChild_is_present = request.param
        parent = self.parent_bldr(zooChild_is_present).element
        expected_xml = self.parent_bldr(False).xml()
        return parent, expected_xml

    # fixture components ---------------------------------------------

    def parent_bldr(self, zooChild_is_present):
        parent_bldr = a_parent().with_nsdecls()
        if zooChild_is_present:
            parent_bldr.with_child(a_zooChild())
        return parent_bldr


class DescribeZeroOrOneChoice(object):

    def it_adds_a_getter_for_the_current_choice(self, getter_fixture):
        parent, expected_choice = getter_fixture
        assert parent.eg_zooChoice is expected_choice

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[None, 'choice', 'choice2'])
    def getter_fixture(self, request):
        choice_tag = request.param
        parent = self.parent_bldr(choice_tag).element
        tagname = 'w:%s' % choice_tag
        expected_choice = parent.find(qn(tagname))  # None if not found
        return parent, expected_choice

    # fixture components ---------------------------------------------

    def parent_bldr(self, choice_tag=None):
        parent_bldr = a_parent().with_nsdecls()
        if choice_tag == 'choice':
            parent_bldr.with_child(a_choice())
        if choice_tag == 'choice2':
            parent_bldr.with_child(a_choice2())
        return parent_bldr


# --------------------------------------------------------------------
# static shared fixture
# --------------------------------------------------------------------

class ST_IntegerType(BaseIntType):

    @classmethod
    def validate(cls, value):
        cls.validate_int(value)
        if value < 1 or value > 42:
            raise ValueError(
                "value must be in range 1 to 42 inclusive"
            )


class CT_Parent(BaseOxmlElement):
    """
    ``<w:parent>`` element, an invented element for use in testing.
    """
    eg_zooChoice = ZeroOrOneChoice(
        (Choice('w:choice'), Choice('w:choice2')),
        successors=('w:oomChild', 'w:oooChild')
    )
    oomChild = OneOrMore('w:oomChild', successors=(
        'w:oooChild', 'w:zomChild', 'w:zooChild'
    ))
    oooChild = OneAndOnlyOne('w:oooChild')
    zomChild = ZeroOrMore('w:zomChild', successors=('w:zooChild',))
    zooChild = ZeroOrOne('w:zooChild', successors=())
    optAttr = OptionalAttribute('w:optAttr', ST_IntegerType)
    reqAttr = RequiredAttribute('reqAttr', ST_IntegerType)


class CT_Choice(BaseOxmlElement):
    """
    ``<w:choice>`` element
    """


class CT_OomChild(BaseOxmlElement):
    """
    Oom standing for 'OneOrMore', ``<w:oomChild>`` element, representing a
    child element that can appear multiple times in sequence, but must appear
    at least once.
    """


class CT_ZomChild(BaseOxmlElement):
    """
    Zom standing for 'ZeroOrMore', ``<w:zomChild>`` element, representing an
    optional child element that can appear multiple times in sequence.
    """


class CT_ZooChild(BaseOxmlElement):
    """
    Zoo standing for 'ZeroOrOne', ``<w:zooChild>`` element, an invented
    element for use in testing.
    """


register_element_cls('w:parent',   CT_Parent)
register_element_cls('w:choice',   CT_Choice)
register_element_cls('w:oomChild', CT_OomChild)
register_element_cls('w:zomChild', CT_ZomChild)
register_element_cls('w:zooChild', CT_ZooChild)


class CT_ChoiceBuilder(BaseBuilder):
    __tag__ = 'w:choice'
    __nspfxs__ = ('w',)
    __attrs__ = ()


class CT_Choice2Builder(BaseBuilder):
    __tag__ = 'w:choice2'
    __nspfxs__ = ('w',)
    __attrs__ = ()


class CT_ParentBuilder(BaseBuilder):
    __tag__ = 'w:parent'
    __nspfxs__ = ('w',)
    __attrs__ = ('w:optAttr', 'reqAttr')


class CT_OomChildBuilder(BaseBuilder):
    __tag__ = 'w:oomChild'
    __nspfxs__ = ('w',)
    __attrs__ = ()


class CT_OooChildBuilder(BaseBuilder):
    __tag__ = 'w:oooChild'
    __nspfxs__ = ('w',)
    __attrs__ = ()


class CT_ZomChildBuilder(BaseBuilder):
    __tag__ = 'w:zomChild'
    __nspfxs__ = ('w',)
    __attrs__ = ()


class CT_ZooChildBuilder(BaseBuilder):
    __tag__ = 'w:zooChild'
    __nspfxs__ = ('w',)
    __attrs__ = ()


def a_choice():
    return CT_ChoiceBuilder()


def a_choice2():
    return CT_Choice2Builder()


def a_parent():
    return CT_ParentBuilder()


def a_zomChild():
    return CT_ZomChildBuilder()


def a_zooChild():
    return CT_ZooChildBuilder()


def an_oomChild():
    return CT_OomChildBuilder()


def an_oooChild():
    return CT_OooChildBuilder()
