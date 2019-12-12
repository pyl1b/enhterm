# -*- coding: utf-8 -*-
"""
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
from unittest import TestCase

from enhterm.provider.parser_provider import ParserProvider

logger = logging.getLogger('')


class TestParserProvider(TestCase):
    def setUp(self):
        self.testee = ParserProvider()

    def tearDown(self):
        self.testee = None

    def test_init(self):
        self.assertIsNone(self.testee.agent)
        self.assertDictEqual(self.testee.opaque_data, {})
        self.assertIsNone(self.testee.store_id)

    def test_str(self):
        self.assertIn('ParserProvider', '%s' % self.testee)
        self.assertIn('ParserProvider', '%r' % self.testee)

    def test_get_command(self):
        self.fail()

    def test_get_text(self):
        self.fail()
