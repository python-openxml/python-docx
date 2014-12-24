# encoding: utf-8

"""
Test suite for the docx.shared module
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from docx.opc.part import XmlPart
from docx.shared import ElementProxy

from .unitutil.cxml import element
from .unitutil.mock import instance_mock


class DescribeElementProxy(object):

    def it_knows_when_its_equal_to_another_proxy_object(self, eq_fixture):
        proxy, proxy_2, proxy_3, not_a_proxy = eq_fixture

        assert (proxy == proxy_2) is True
        assert (proxy == proxy_3) is False
        assert (proxy == not_a_proxy) is False

        assert (proxy != proxy_2) is False
        assert (proxy != proxy_3) is True
        assert (proxy != not_a_proxy) is True

    def it_knows_its_element(self, element_fixture):
        proxy, element = element_fixture
        assert proxy.element is element

    def it_knows_its_part(self, part_fixture):
        proxy, part_ = part_fixture
        assert proxy.part is part_

    # fixture --------------------------------------------------------

    @pytest.fixture
    def element_fixture(self):
        p = element('w:p')
        proxy = ElementProxy(p)
        return proxy, p

    @pytest.fixture
    def eq_fixture(self):
        p, q = element('w:p'), element('w:p')
        proxy = ElementProxy(p)
        proxy_2 = ElementProxy(p)
        proxy_3 = ElementProxy(q)
        not_a_proxy = 'Foobar'
        return proxy, proxy_2, proxy_3, not_a_proxy

    @pytest.fixture
    def part_fixture(self, other_proxy_, part_):
        other_proxy_.part = part_
        proxy = ElementProxy(None, other_proxy_)
        return proxy, part_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def other_proxy_(self, request):
        return instance_mock(request, ElementProxy)

    @pytest.fixture
    def part_(self, request):
        return instance_mock(request, XmlPart)
