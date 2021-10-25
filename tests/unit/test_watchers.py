import logging
import sys
from unittest import TestCase
from unittest.mock import MagicMock

from enhterm.command import Command

from enhterm.message import Message
from enhterm.watcher import Watcher

from enhterm.watcher.echo import EchoWatcher


class TestWatcher(TestCase):
    def setUp(self):
        self.testee = Watcher(
            term=MagicMock(),
        )

    def tearDown(self):
        self.testee = None

    def test_init(self):
        testee = Watcher()
        self.assertIsNone(testee.term)

        testee = Watcher(term="123")
        self.assertEqual(testee.term, "123")

    def test_str(self):
        self.assertEqual(str(self.testee), 'Watcher()')

    def test_repr(self):
        self.assertEqual(repr(self.testee), 'Watcher()')

    def test_nothing(self):
        self.testee.pre_loop()
        self.testee.post_loop()
        self.testee.pre_cmd(command=MagicMock(spec=Command))
        self.testee.post_cmd(command=MagicMock(spec=Command))
        self.testee.message_issued(message=MagicMock(spec=Message))


class TestEchoWatcher(TestCase):
    def setUp(self):
        self.testee = EchoWatcher(
            term=MagicMock(),
            low_stream=MagicMock(),
            high_stream=MagicMock(),
            cutoff=2
        )

    def tearDown(self):
        self.testee = None

    @staticmethod
    def create_paras():
        par1 = MagicMock()
        par1.__str__ = MagicMock(return_value='x')
        par2 = MagicMock()
        par2.__str__ = MagicMock(return_value='y')
        return [
            par1, par2
        ]

    def test_init(self):
        testee = EchoWatcher()
        self.assertEqual(testee.low_stream, sys.stdout)
        self.assertEqual(testee.high_stream, sys.stderr)
        self.assertEqual(testee.cutoff, logging.WARNING)
        self.assertIsNone(testee.term)

        testee = EchoWatcher(
            low_stream='a',
            high_stream='b',
            cutoff=100
        )
        self.assertEqual(testee.low_stream, 'a')
        self.assertEqual(testee.high_stream, 'b')
        self.assertEqual(testee.cutoff, 100)
        self.assertIsNone(testee.term)

    def test_str(self):
        self.assertEqual(str(self.testee), 'EchoWatcher()')

    def test_repr(self):
        self.assertEqual(repr(self.testee), 'EchoWatcher()')

    def test_message_issued_low(self):
        message = MagicMock(spec=Message)
        message.severity = 1
        message.paragraphs = TestEchoWatcher.create_paras()

        self.testee.message_issued(message)
        self.testee.low_stream.write.assert_any_call('x\n')
        self.testee.low_stream.write.assert_any_call('y\n')
        self.testee.high_stream.write.assert_not_called()

    def test_message_issued_high(self):
        message = MagicMock(spec=Message)
        message.severity = 3
        message.paragraphs = TestEchoWatcher.create_paras()

        self.testee.message_issued(message)
        self.testee.high_stream.write.assert_any_call('x\n')
        self.testee.high_stream.write.assert_any_call('y\n')
        self.testee.low_stream.write.assert_not_called()

    def test_message_issued_equal(self):
        message = MagicMock(spec=Message)
        message.severity = 2
        message.paragraphs = TestEchoWatcher.create_paras()

        self.testee.message_issued(message)
        self.testee.high_stream.write.assert_any_call('x\n')
        self.testee.high_stream.write.assert_any_call('y\n')
        self.testee.low_stream.write.assert_not_called()

    def test_result_none(self):
        command = MagicMock(spec=Command)
        command.result = None

        self.testee.post_cmd(command)
        self.testee.high_stream.write.assert_not_called()
        self.testee.low_stream.write.assert_not_called()

    def test_result_something(self):
        command = MagicMock(spec=Command)
        command.result = "123abc"

        self.testee.post_cmd(command)
        self.testee.high_stream.write.assert_not_called()
        self.testee.low_stream.write.assert_called_once_with("123abc\n")
