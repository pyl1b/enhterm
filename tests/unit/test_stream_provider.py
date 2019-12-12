# -*- coding: utf-8 -*-
"""
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
from unittest import TestCase

from enhterm.provider.stream_provider import StreamProvider

logger = logging.getLogger('')


class TestStreamProvider(TestCase):
    def setUp(self):
        self.testee = StreamProvider()

    def tearDown(self):
        self.testee = None

    def test_init(self):
        self.assertIsNone(self.testee.agent)
        self.assertDictEqual(self.testee.opaque_data, {})
        self.assertIsNone(self.testee.store_id)

    def test_str(self):
        self.assertIn('StreamProvider', '%s' % self.testee)
        self.assertIn('StreamProvider', '%r' % self.testee)

    def test_get_text(self):
        self.fail()
