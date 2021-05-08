# -*- coding: utf-8 -*-
"""
"""
import logging
from unittest import TestCase
from unittest.mock import MagicMock
from uuid import UUID

from p2p0mq.concerns.manager import ConcernsManager
from p2p0mq.constants import MESSAGE_TYPE_REQUEST
from p2p0mq.message import Message
from p2p0mq.peer import Peer

from enhterm.command import Command
from enhterm.impl.p2p.p2p_concern import RemoteConcern
from enhterm.ser_deser import SerDeSer

logger = logging.getLogger('')


class TestRemoteConcern(TestCase):
    def setUp(self):
        self.app = MagicMock(spec=ConcernsManager)
        self.app.uuid = '123456'
        self.app.tick = 1570447226
        self.encoder = MagicMock(spec=SerDeSer)
        self.provider = MagicMock(spec=SerDeSer)
        self.testee = RemoteConcern(
            app=self.app, encoder=self.encoder, provider=self.provider)

    def tearDown(self):
        self.testee = None

    def test_init(self):
        self.assertIsNotNone(self.testee.encoder)
        self.assertIsNotNone(self.testee.provider)
        self.assertDictEqual(self.testee.sent_messages, {})
        self.assertDictEqual(self.testee.received_commands, {})
        self.assertEqual(self.testee.name, 'terminal')
        self.assertEqual(self.testee.command_id, b'et')

    def test_str(self):
        self.assertIn('RemoteConcern', '%s' % self.testee)
        self.assertIn('RemoteConcern', '%r' % self.testee)

    def test_compose(self):
        peer = MagicMock(spec=Peer)
        peer.uuid = '09876'
        command = MagicMock(spec=Command)
        self.encoder.pack_command.return_value = 'RETVAL'

        result = self.testee.compose(peer, command)
        self.assertIsInstance(result, Message)
        self.assertEqual(len(self.testee.sent_messages), 1)
        self.assertEqual(result.source, '123456')
        self.assertEqual(result.to, '09876')
        self.assertIsNone(result.previous_hop)
        self.assertEqual(result.next_hop, '09876')
        self.assertEqual(result.command, b'et')
        self.assertEqual(result.kind, MESSAGE_TYPE_REQUEST)
        self.assertEqual(result.handler, self.testee)
        self.assertEqual(result.payload['command_content'], 'RETVAL')

    def test_process_request(self):
        message = MagicMock(spec=Message)
        self.testee.process_request(message=message)

    def test_post_reply(self):
        messages = [MagicMock(spec=Message), MagicMock(spec=Message)]
        command = MagicMock(spec=Command)
        self.testee.post_reply(command, messages)

    def test_process_reply(self):
        message = MagicMock(spec=Message)
        self.testee.process_reply(message=message)

    def test_get_reply(self):
        message = MagicMock(spec=Message)
        self.testee.get_reply(message=message, remove_on_success=True)

        message = MagicMock(spec=Message)
        self.testee.get_reply(message=message, remove_on_success=False)
