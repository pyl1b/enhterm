# -*- coding: utf-8 -*-
"""
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
from unittest import TestCase
from unittest.mock import MagicMock

from mock import call
from p2p0mq.app.local_peer import LocalPeer
from p2p0mq.peer import Peer

from enhterm import EnhTerm
from enhterm.command import Command
from enhterm.command.text import TextCommand
from enhterm.impl.p2p.p2p_concern import RemoteConcern
from enhterm.impl.p2p.p2p_runner import RemoteRunner
from enhterm.message import Message

logger = logging.getLogger('')


class TestRemoteRunner(TestCase):
    def setUp(self):
        self.app = MagicMock(spec=LocalPeer)
        self.app.sender = MagicMock()
        self.app.sender.medium_queue = MagicMock()
        self.term = MagicMock(spec=EnhTerm)

        self.concern = MagicMock(spec=RemoteConcern)
        rc = RemoteConcern(MagicMock(), MagicMock())
        self.app.concerns = {rc.command_id: self.concern}
        self.peer = MagicMock(spec=Peer)
        self.peer.uuid = '123456'
        self.testee = RemoteRunner(
            zmq_app=self.app, timeout=5, peer=self.peer,
            term=self.term
        )

    def tearDown(self):
        self.testee = None

    def test_init(self):
        testee = RemoteRunner(zmq_app=self.app)
        self.assertIsNone(testee.peer)
        self.assertIsNone(testee.term)
        self.assertEqual(testee.timeout, 4)

        testee = RemoteRunner(zmq_app=self.app, peer=self.peer)
        self.assertEqual(testee.peer, self.peer)

        self.app.peers = {'123456': self.peer}
        testee = RemoteRunner(zmq_app=self.app, peer='123456')
        self.assertEqual(testee.peer, self.peer)

    def test_str(self):
        self.assertIn('RemoteRunner', '%s' % self.testee)
        self.assertIn('RemoteRunner', '%r' % self.testee)

    def test_concern(self):
        self.assertEquals(self.testee.concern, self.concern)


    def test_timed_out(self):
        with self.assertRaises(TimeoutError):
            self.testee.timed_out()

    def test_call(self):
        command = MagicMock(spec=Command)
        self.testee(command)
        command.execute.assert_called_once()

        command = MagicMock(spec=TextCommand)
        command.result = 998
        message = MagicMock(spec=Message)
        reply = command, None
        self.testee.concern.get_reply = MagicMock(return_value=reply)
        self.concern.compose = MagicMock(return_value=message)
        self.assertEqual(self.testee(command), 998)
        command.execute.assert_not_called()
        self.app.sender.medium_queue.enqueue.assert_called_once_with(message)

    def test_call_messages(self):
        self.testee.timed_out = MagicMock()
        command = MagicMock(spec=TextCommand)
        command.result = 998
        message = MagicMock(spec=Message)
        messages = [1, 2]
        reply = command, messages
        self.testee.concern.get_reply = MagicMock(return_value=reply)
        self.concern.compose = MagicMock(return_value=message)
        self.assertEqual(self.testee(command), 998)
        command.execute.assert_not_called()
        self.app.sender.medium_queue.enqueue.assert_called_once_with(message)
        self.testee.term.issue_message.assert_has_calls([call(1), call(2)])
        self.testee.timed_out.assert_not_called()

    def test_call_timeout(self):
        self.testee.timeout = 0.5
        self.testee.timed_out = MagicMock()
        command = MagicMock(spec=TextCommand)
        command.result = 998
        message = MagicMock(spec=Message)
        # The reply never comes so it will timeout
        self.testee.concern.get_reply = MagicMock(return_value=None)
        self.concern.compose = MagicMock(return_value=message)
        self.assertIsNone(self.testee(command))
        command.execute.assert_not_called()
        self.app.sender.medium_queue.enqueue.assert_called_once_with(message)
        self.testee.term.issue_message.assert_not_called()
        self.testee.timed_out.assert_called_once()
