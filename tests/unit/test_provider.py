# -*- coding: utf-8 -*-
"""
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
from unittest import TestCase

from enhterm.provider import Provider

logger = logging.getLogger('')


class TestProvider(TestCase):
    def setUp(self):
        self.testee = Provider()

    def tearDown(self):
        self.testee = None

    def test_init(self):
        self.assertIsNone(self.testee.agent)
        self.assertDictEqual(self.testee.opaque_data, {})
        self.assertIsNone(self.testee.store_id)

    def test_str(self):
        self.assertIn('Provider', '%s' % self.testee)
        self.assertIn('Provider', '%r' % self.testee)

    def test_start(self):
        self.fail()

    def test_stop(self):
        self.fail()

    def test_pause(self):
        self.fail()

    def test_unpause(self):
        self.fail()

    def test_get_command(self):
        self.fail()
