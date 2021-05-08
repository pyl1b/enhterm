# -*- coding: utf-8 -*-
"""
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
from unittest import TestCase
from unittest.mock import MagicMock

from p2p0mq.app.local_peer import LocalPeer

from enhterm.impl.p2p.p2p_provider import RemoteProvider
from enhterm.impl.p2p.p2p_watcher import RemoteWatcher

logger = logging.getLogger('')


class TestRemoteProvider(TestCase):
    def setUp(self):
        self.app = MagicMock(spec=LocalPeer)
        self.app.concerns = {b'et': 'test'}

        self.testee = RemoteProvider(
            zmq_app=self.app)

    def tearDown(self):
        self.testee = None

    def test_init(self):
        self.assertIsInstance(self.testee.watcher, RemoteWatcher)

    def test_str(self):
        self.assertIn('RemoteProvider', '%s' % self.testee)
        self.assertIn('RemoteProvider', '%r' % self.testee)

    def test_concern(self):
        self.assertEquals(self.testee.concern, 'test')
