# -*- coding: utf-8 -*-
"""
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
from unittest import TestCase

from enhterm.provider.queue_provider import QueueProvider

logger = logging.getLogger('')


class TestQueueProvider(TestCase):
    def setUp(self):
        self.testee = QueueProvider()

    def tearDown(self):
        self.testee = None

    def test_init(self):
        self.assertIsNone(self.testee.agent)
        self.assertDictEqual(self.testee.opaque_data, {})
        self.assertIsNone(self.testee.store_id)

    def test_str(self):
        self.assertIn('QueueProvider', '%s' % self.testee)
        self.assertIn('QueueProvider', '%r' % self.testee)

    def test_get_command(self):
        self.fail()
