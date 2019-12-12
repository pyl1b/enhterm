# -*- coding: utf-8 -*-
"""
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
from unittest import TestCase

from enhterm.provider.parser import Parser

logger = logging.getLogger('')


class TestParser(TestCase):
    def setUp(self):
        self.testee = Parser()

    def tearDown(self):
        self.testee = None

    def test_init(self):
        self.assertIsNone(self.testee.agent)
        self.assertDictEqual(self.testee.opaque_data, {})
        self.assertIsNone(self.testee.store_id)

    def test_str(self):
        self.assertIn('Parser', '%s' % self.testee)
        self.assertIn('Parser', '%r' % self.testee)

    def test_parse(self):
        self.fail()
