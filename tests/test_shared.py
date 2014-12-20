# encoding: utf-8

"""
Test suite for the docx.shared module
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import pytest

from docx.shared import ElementProxy

from .unitutil.cxml import element


class DescribeElementProxy(object):

    def it_knows_when_its_equal_to_another_proxy_object(self, eq_fixture):
        proxy, proxy_2, proxy_3, not_a_proxy = eq_fixture

        assert (proxy == proxy_2) is True
        assert (proxy == proxy_3) is False
        assert (proxy == not_a_proxy) is False

        assert (proxy != proxy_2) is False
        assert (proxy != proxy_3) is True
        assert (proxy != not_a_proxy) is True

    # fixture --------------------------------------------------------

    @pytest.fixture
    def eq_fixture(self):
        p, q = element('w:p'), element('w:p')
        proxy = ElementProxy(p)
        proxy_2 = ElementProxy(p)
        proxy_3 = ElementProxy(q)
        not_a_proxy = 'Foobar'
        return proxy, proxy_2, proxy_3, not_a_proxy
