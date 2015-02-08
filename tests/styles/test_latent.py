# encoding: utf-8

"""
Unit test suite for the docx.styles.latent module
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from docx.styles.latent import _LatentStyle, LatentStyles

from ..unitutil.cxml import element, xml


class DescribeLatentStyle(object):

    def it_can_delete_itself(self, delete_fixture):
        latent_style, latent_styles, expected_xml = delete_fixture
        latent_style.delete()
        assert latent_styles.xml == expected_xml
        assert latent_style._element is None

    def it_knows_its_name(self, name_get_fixture):
        latent_style, expected_value = name_get_fixture
        assert latent_style.name == expected_value

    def it_knows_its_priority(self, priority_get_fixture):
        latent_style, expected_value = priority_get_fixture
        assert latent_style.priority == expected_value

    def it_can_change_its_priority(self, priority_set_fixture):
        latent_style, new_value, expected_xml = priority_set_fixture
        latent_style.priority = new_value
        assert latent_style._element.xml == expected_xml

    def it_knows_its_on_off_properties(self, on_off_get_fixture):
        latent_style, prop_name, expected_value = on_off_get_fixture
        actual_value = getattr(latent_style, prop_name)
        assert actual_value == expected_value

    def it_can_change_its_on_off_properties(self, on_off_set_fixture):
        latent_style, prop_name, value, expected_xml = on_off_set_fixture
        setattr(latent_style, prop_name, value)
        assert latent_style.element.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def delete_fixture(self):
        latent_styles = element('w:latentStyles/w:lsdException{w:name=Foo}')
        latent_style = _LatentStyle(latent_styles[0])
        expected_xml = xml('w:latentStyles')
        return latent_style, latent_styles, expected_xml

    @pytest.fixture(params=[
        ('w:lsdException{w:name=heading 1}', 'Heading 1'),
    ])
    def name_get_fixture(self, request):
        lsdException_cxml, expected_value = request.param
        latent_style = _LatentStyle(element(lsdException_cxml))
        return latent_style, expected_value

    @pytest.fixture(params=[
        ('w:lsdException',                     'hidden',           None),
        ('w:lsdException',                     'locked',           None),
        ('w:lsdException',                     'quick_style',      None),
        ('w:lsdException',                     'unhide_when_used', None),
        ('w:lsdException{w:semiHidden=1}',     'hidden',           True),
        ('w:lsdException{w:locked=1}',         'locked',           True),
        ('w:lsdException{w:qFormat=1}',        'quick_style',      True),
        ('w:lsdException{w:unhideWhenUsed=1}', 'unhide_when_used', True),
        ('w:lsdException{w:semiHidden=0}',     'hidden',           False),
        ('w:lsdException{w:locked=0}',         'locked',           False),
        ('w:lsdException{w:qFormat=0}',        'quick_style',      False),
        ('w:lsdException{w:unhideWhenUsed=0}', 'unhide_when_used', False),
    ])
    def on_off_get_fixture(self, request):
        lsdException_cxml, prop_name, expected_value = request.param
        latent_style = _LatentStyle(element(lsdException_cxml))
        return latent_style, prop_name, expected_value

    @pytest.fixture(params=[
        ('w:lsdException',                 'hidden',           True,
         'w:lsdException{w:semiHidden=1}'),
        ('w:lsdException{w:semiHidden=1}', 'hidden',           False,
         'w:lsdException{w:semiHidden=0}'),
        ('w:lsdException{w:semiHidden=0}', 'hidden',           None,
         'w:lsdException'),
        ('w:lsdException',                 'locked',           True,
         'w:lsdException{w:locked=1}'),
        ('w:lsdException',                 'quick_style',      False,
         'w:lsdException{w:qFormat=0}'),
        ('w:lsdException',                 'unhide_when_used', True,
         'w:lsdException{w:unhideWhenUsed=1}'),
        ('w:lsdException{w:locked=1}',     'locked',           None,
         'w:lsdException'),
    ])
    def on_off_set_fixture(self, request):
        lsdException_cxml, prop_name, value, expected_cxml = request.param
        latent_styles = _LatentStyle(element(lsdException_cxml))
        expected_xml = xml(expected_cxml)
        return latent_styles, prop_name, value, expected_xml

    @pytest.fixture(params=[
        ('w:lsdException',                  None),
        ('w:lsdException{w:uiPriority=42}', 42),
    ])
    def priority_get_fixture(self, request):
        lsdException_cxml, expected_value = request.param
        latent_style = _LatentStyle(element(lsdException_cxml))
        return latent_style, expected_value

    @pytest.fixture(params=[
        ('w:lsdException',                  42,
         'w:lsdException{w:uiPriority=42}'),
        ('w:lsdException{w:uiPriority=42}', 24,
         'w:lsdException{w:uiPriority=24}'),
        ('w:lsdException{w:uiPriority=24}', None,
         'w:lsdException'),
    ])
    def priority_set_fixture(self, request):
        lsdException_cxml, new_value, expected_cxml = request.param
        latent_style = _LatentStyle(element(lsdException_cxml))
        expected_xml = xml(expected_cxml)
        return latent_style, new_value, expected_xml


class DescribeLatentStyles(object):

    def it_can_add_a_latent_style(self, add_fixture):
        latent_styles, name, expected_xml = add_fixture

        latent_style = latent_styles.add_latent_style(name)

        assert latent_styles.element.xml == expected_xml
        assert isinstance(latent_style, _LatentStyle)
        assert latent_style.element is latent_styles.element[0]

    def it_knows_how_many_latent_styles_it_contains(self, len_fixture):
        latent_styles, expected_value = len_fixture
        assert len(latent_styles) == expected_value

    def it_can_iterate_over_its_latent_styles(self, iter_fixture):
        latent_styles, expected_count = iter_fixture
        lst = [ls for ls in latent_styles]
        assert len(lst) == expected_count
        for latent_style in lst:
            assert isinstance(latent_style, _LatentStyle)

    def it_can_get_a_latent_style_by_name(self, getitem_fixture):
        latent_styles, name, lsdException = getitem_fixture
        latent_style = latent_styles[name]
        assert isinstance(latent_style, _LatentStyle)
        assert latent_style._element is lsdException

    def it_raises_on_latent_style_not_found(self, getitem_raises_fixture):
        latent_styles, name = getitem_raises_fixture
        with pytest.raises(KeyError):
            latent_styles[name]

    def it_knows_its_default_priority(self, priority_get_fixture):
        latent_styles, expected_value = priority_get_fixture
        assert latent_styles.default_priority == expected_value

    def it_can_change_its_default_priority(self, priority_set_fixture):
        latent_styles, value, expected_xml = priority_set_fixture
        latent_styles.default_priority = value
        assert latent_styles._element.xml == expected_xml

    def it_knows_its_load_count(self, count_get_fixture):
        latent_styles, expected_value = count_get_fixture
        assert latent_styles.load_count == expected_value

    def it_can_change_its_load_count(self, count_set_fixture):
        latent_styles, value, expected_xml = count_set_fixture
        latent_styles.load_count = value
        assert latent_styles._element.xml == expected_xml

    def it_knows_its_boolean_properties(self, bool_prop_get_fixture):
        latent_styles, prop_name, expected_value = bool_prop_get_fixture
        actual_value = getattr(latent_styles, prop_name)
        assert actual_value == expected_value

    def it_can_change_its_boolean_properties(self, bool_prop_set_fixture):
        latent_styles, prop_name, value, expected_xml = bool_prop_set_fixture
        setattr(latent_styles, prop_name, value)
        assert latent_styles.element.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def add_fixture(self):
        latent_styles = LatentStyles(element('w:latentStyles'))
        name = 'Heading 1'
        expected_xml = xml('w:latentStyles/w:lsdException{w:name=heading 1}')
        return latent_styles, name, expected_xml

    @pytest.fixture(params=[
        ('w:latentStyles', 'default_to_hidden',           False),
        ('w:latentStyles', 'default_to_locked',           False),
        ('w:latentStyles', 'default_to_quick_style',      False),
        ('w:latentStyles', 'default_to_unhide_when_used', False),
        ('w:latentStyles{w:defSemiHidden=1}',
         'default_to_hidden',           True),
        ('w:latentStyles{w:defLockedState=0}',
         'default_to_locked',           False),
        ('w:latentStyles{w:defQFormat=on}',
         'default_to_quick_style',      True),
        ('w:latentStyles{w:defUnhideWhenUsed=false}',
         'default_to_unhide_when_used', False),
    ])
    def bool_prop_get_fixture(self, request):
        latentStyles_cxml, prop_name, expected_value = request.param
        latent_styles = LatentStyles(element(latentStyles_cxml))
        return latent_styles, prop_name, expected_value

    @pytest.fixture(params=[
        ('w:latentStyles', 'default_to_hidden',           True,
         'w:latentStyles{w:defSemiHidden=1}'),
        ('w:latentStyles', 'default_to_locked',           False,
         'w:latentStyles{w:defLockedState=0}'),
        ('w:latentStyles', 'default_to_quick_style',      True,
         'w:latentStyles{w:defQFormat=1}'),
        ('w:latentStyles', 'default_to_unhide_when_used', False,
         'w:latentStyles{w:defUnhideWhenUsed=0}'),
        ('w:latentStyles{w:defSemiHidden=0}',  'default_to_hidden', 'Foo',
         'w:latentStyles{w:defSemiHidden=1}'),
        ('w:latentStyles{w:defLockedState=1}', 'default_to_locked', None,
         'w:latentStyles{w:defLockedState=0}'),
    ])
    def bool_prop_set_fixture(self, request):
        latentStyles_cxml, prop_name, value, expected_cxml = request.param
        latent_styles = LatentStyles(element(latentStyles_cxml))
        expected_xml = xml(expected_cxml)
        return latent_styles, prop_name, value, expected_xml

    @pytest.fixture(params=[
        ('w:latentStyles',             None),
        ('w:latentStyles{w:count=42}', 42),
    ])
    def count_get_fixture(self, request):
        latentStyles_cxml, expected_value = request.param
        latent_styles = LatentStyles(element(latentStyles_cxml))
        return latent_styles, expected_value

    @pytest.fixture(params=[
        ('w:latentStyles',             42,   'w:latentStyles{w:count=42}'),
        ('w:latentStyles{w:count=24}', 42,   'w:latentStyles{w:count=42}'),
        ('w:latentStyles{w:count=24}', None, 'w:latentStyles'),
    ])
    def count_set_fixture(self, request):
        latentStyles_cxml, value, expected_cxml = request.param
        latent_styles = LatentStyles(element(latentStyles_cxml))
        expected_xml = xml(expected_cxml)
        return latent_styles, value, expected_xml

    @pytest.fixture(params=[
        ('w:lsdException{w:name=Ab},w:lsdException,w:lsdException', 'Ab', 0),
        ('w:lsdException,w:lsdException{w:name=Cd},w:lsdException', 'Cd', 1),
        ('w:lsdException,w:lsdException,w:lsdException{w:name=Ef}', 'Ef', 2),
        ('w:lsdException{w:name=heading 1}', 'Heading 1', 0),
    ])
    def getitem_fixture(self, request):
        cxml, name, idx = request.param
        latentStyles_cxml = 'w:latentStyles/(%s)' % cxml
        latentStyles = element(latentStyles_cxml)
        lsdException = latentStyles[idx]
        latent_styles = LatentStyles(latentStyles)
        return latent_styles, name, lsdException

    @pytest.fixture
    def getitem_raises_fixture(self):
        latent_styles = LatentStyles(element('w:latentStyles'))
        return latent_styles, 'Foobar'

    @pytest.fixture(params=[
        ('w:latentStyles',                                  0),
        ('w:latentStyles/w:lsdException',                   1),
        ('w:latentStyles/(w:lsdException,w:lsdException)',  2),
    ])
    def iter_fixture(self, request):
        latentStyles_cxml, count = request.param
        latent_styles = LatentStyles(element(latentStyles_cxml))
        return latent_styles, count

    @pytest.fixture(params=[
        ('w:latentStyles',                                  0),
        ('w:latentStyles/w:lsdException',                   1),
        ('w:latentStyles/(w:lsdException,w:lsdException)',  2),
    ])
    def len_fixture(self, request):
        latentStyles_cxml, count = request.param
        latent_styles = LatentStyles(element(latentStyles_cxml))
        return latent_styles, count

    @pytest.fixture(params=[
        ('w:latentStyles',                     None),
        ('w:latentStyles{w:defUIPriority=42}', 42),
    ])
    def priority_get_fixture(self, request):
        latentStyles_cxml, expected_value = request.param
        latent_styles = LatentStyles(element(latentStyles_cxml))
        return latent_styles, expected_value

    @pytest.fixture(params=[
        ('w:latentStyles',                     42,
         'w:latentStyles{w:defUIPriority=42}'),
        ('w:latentStyles{w:defUIPriority=24}', 42,
         'w:latentStyles{w:defUIPriority=42}'),
        ('w:latentStyles{w:defUIPriority=24}', None,
         'w:latentStyles'),
    ])
    def priority_set_fixture(self, request):
        latentStyles_cxml, value, expected_cxml = request.param
        latent_styles = LatentStyles(element(latentStyles_cxml))
        expected_xml = xml(expected_cxml)
        return latent_styles, value, expected_xml
