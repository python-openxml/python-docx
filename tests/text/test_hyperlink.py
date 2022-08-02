import pytest

from docx.text.hyperlink import Hyperlink
from docx.text.run import Run
from docx.api import Document as OpenDocument
from docx.enum.style import WD_STYLE_TYPE

from ..unitutil.cxml import element, xml
from ..unitutil.mock import (
    property_mock
)


class DescribeHyperlink:
    def it_knows_its_relationship_id(self, relationship_id_fixture):
        hyperlink, expected_relationship_id = relationship_id_fixture
        assert hyperlink.relationship_id == expected_relationship_id

    def it_can_set_relationship_id(self, relationship_id_setter_fixture):
        hyperlink, set_value, expected_xml = relationship_id_setter_fixture
        hyperlink.relationship_id = set_value
        assert expected_xml == hyperlink._element.xml

    def it_knows_its_target(self, target_fixture):
        hyperlink, expected_target, _ = target_fixture
        assert hyperlink.target == expected_target

    def it_knows_if_target_is_external(self, target_fixture):
        hyperlink, _, expected_is_external = target_fixture
        assert hyperlink.is_external == expected_is_external

    def it_provides_access_to_the_runs_it_contains(self, runs_fixture):
        hyperlink, expected_runs_text = runs_fixture
        assert len(expected_runs_text) == len(hyperlink.runs)
        for i, run in enumerate(hyperlink.runs):
            assert isinstance(run, Run)
            assert run.text == expected_runs_text[i]

    def it_can_add_a_run_to_itself(self, add_run_fixture):
        hyperlink, text, style, style_prop_, expected_xml = add_run_fixture
        run = hyperlink.add_run(text, style)
        assert hyperlink._element.xml == expected_xml
        assert isinstance(run, Run)
        assert run._r is hyperlink._element.r_lst[0]
        if style:
            style_prop_.assert_called_once_with(style)

    def it_can_remove_its_content_while_preserving_target(self, clear_fixture):
        hyperlink, expected_xml = clear_fixture
        _hyperlink = hyperlink.clear()
        assert hyperlink._element.xml == expected_xml
        assert _hyperlink is hyperlink

    def it_knows_the_text_it_contains(self, text_get_fixture):
        hyperlink, expected_text = text_get_fixture
        assert hyperlink.text == expected_text

    def it_can_replace_the_text_it_contains(self, text_set_fixture):
        hyperlink, text, expected_text = text_set_fixture
        hyperlink.text = text
        assert hyperlink.text == expected_text

    def it_can_add_hyperlink_style(self):
        doc = OpenDocument()
        styles = doc.styles
        with pytest.raises(KeyError):
            assert styles["Hyperlink"]
        Hyperlink.add_hyperlink_styles(doc)
        hyperlink_style = styles["Hyperlink"]
        assert hyperlink_style.type == WD_STYLE_TYPE.CHARACTER
        assert hyperlink_style.name == "Hyperlink"
        assert hyperlink_style.font.underline
        assert hyperlink_style.font.color is not None
        assert hyperlink_style.base_style.name == "Default Paragraph Font"

    @pytest.fixture(params=[
        ('w:hyperlink', None,     None,     'w:hyperlink/w:r'),
        ('w:hyperlink', 'foobar', None,     'w:hyperlink/w:r/w:t"foobar"'),
        ('w:hyperlink', None,     'Strong', 'w:hyperlink/w:r'),
        ('w:hyperlink', 'foobar', 'Strong', 'w:hyperlink/w:r/w:t"foobar"'),
    ])
    def add_run_fixture(self, request, run_style_prop_):
        before_cxml, text, style, after_cxml = request.param
        hyperlink = Hyperlink(element(before_cxml), None)
        expected_xml = xml(after_cxml)
        return hyperlink, text, style, run_style_prop_, expected_xml

    @pytest.fixture(params=[
        ('w:hyperlink/(w:r/w:t"foo", w:r/w:t"bar")', ["foo", "bar"]),
    ])
    def runs_fixture(self, request):
        hyperlink_cxml, expected_runs_text = request.param
        return Hyperlink(element(hyperlink_cxml), None), expected_runs_text

    @pytest.fixture(params=[
        ('w:hyperlink{r:d=d}', None, False),
        ('w:hyperlink{r:id=rId1}', 'rId1', True),
        ('w:hyperlink{r:anchor=bookmark}', 'bookmark', False),
        ('w:hyperlink{r:anchor=bookmark,r:id=rId1}', 'rId1', True),
    ])
    def target_fixture(self, request):
        hyperlink_cxml, expected_target, expected_is_external = request.param
        return (Hyperlink(element(hyperlink_cxml), None),
                expected_target,
                expected_is_external)

    @pytest.fixture(params=[
        ('w:hyperlink{r:id=rId1}', 'rId1'),
        ('w:hyperlink', None)
    ])
    def relationship_id_fixture(self, request):
        hyperlink_cxml, expected_relationship_id = request.param
        return Hyperlink(element(hyperlink_cxml), None), expected_relationship_id

    @pytest.fixture(params=[
        ('w:hyperlink{r:d=d}', None, 'w:hyperlink{r:d=d}'),
        ('w:hyperlink{r:d=d}', 'rId1', 'w:hyperlink{r:id=rId1,r:d=d}'),
        ('w:hyperlink{r:id=rId1}', 'rId2', 'w:hyperlink{r:id=rId2}'),
        ('w:hyperlink{r:id=rId1,r:d=d}', None, 'w:hyperlink{r:d=d}')
    ])
    def relationship_id_setter_fixture(self, request):
        """
        Dummy attributes {r:d=d} introduced to ensure that namespace definitions
        in cxml are correctly handled
        """
        og_hyperlink_cxml, set_value, expected_hyperlink_cxml = request.param
        return (Hyperlink(element(og_hyperlink_cxml), None),
                set_value,
                xml(expected_hyperlink_cxml))

    @pytest.fixture
    def run_style_prop_(self, request):
        return property_mock(request, Run, 'style')

    @pytest.fixture(params=[
        ('w:hyperlink', 'w:hyperlink'),
        ('w:hyperlink/w:r/w:t"foobar"', 'w:hyperlink'),
        ('w:hyperlink{r:id=rId1}/w:r/w:t"foobar"', 'w:hyperlink{r:id=rId1}'),
    ])
    def clear_fixture(self, request):
        initial_cxml, expected_cxml = request.param
        hyperlink = Hyperlink(element(initial_cxml), None)
        expected_xml = xml(expected_cxml)
        return hyperlink, expected_xml

    @pytest.fixture(params=[
        ('w:hyperlink', ''),
        ('w:hyperlink/w:r', ''),
        ('w:hyperlink/w:r/w:t', ''),
        ('w:hyperlink/w:r/w:t"foo"', 'foo'),
        ('w:hyperlink/w:r/(w:t"foo", w:t"bar")', 'foobar'),
        ('w:hyperlink/w:r/(w:t"fo ", w:t"bar")', 'fo bar'),
        ('w:hyperlink/w:r/(w:t"foo", w:tab, w:t"bar")', 'foo\tbar'),
        ('w:hyperlink/w:r/(w:t"foo", w:br,  w:t"bar")', 'foo\nbar'),
        ('w:hyperlink/w:r/(w:t"foo", w:cr,  w:t"bar")', 'foo\nbar'),
    ])
    def text_get_fixture(self, request):
        p_cxml, expected_text_value = request.param
        hyperlink = Hyperlink(element(p_cxml), None)
        return hyperlink, expected_text_value

    @pytest.fixture
    def text_set_fixture(self):
        paragraph = Hyperlink(element('w:hyperlink'), None)
        paragraph.add_run('must not appear in result')
        new_text_value = 'foo\tbar\rbaz\n'
        expected_text_value = 'foo\tbar\nbaz\n'
        return paragraph, new_text_value, expected_text_value
