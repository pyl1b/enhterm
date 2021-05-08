# -*- coding: utf-8 -*-
"""
"""
import logging
from unittest import TestCase
from unittest.mock import MagicMock
from uuid import UUID

from enhterm import EnhTerm
from enhterm.command import Command
from enhterm.command.error import ErrorCommand
from enhterm.command.noop import NoOpCommand
from enhterm.command.quit import QuitCommand
from enhterm.command.text import TextCommand
from enhterm.command.unknown import UnknownCommand

logger = logging.getLogger('')


class TestCommand(TestCase):
    def setUp(self):
        self.testee = Command()

    def tearDown(self):
        self.testee = None

    def test_init(self):
        self.assertIsNone(self.testee.term)
        self.assertIsNone(self.testee.provider)
        self.assertIsNone(self.testee.result)
        self.assertIsInstance(self.testee.uuid, UUID)

    def test_str(self):
        self.assertIn('Command', '%s' % self.testee)
        self.assertIn('Command', '%r' % self.testee)

    def test_execute(self):
        with self.assertRaises(NotImplementedError):
            self.testee.execute()


class TestErrorCommand(TestCase):
    def setUp(self):
        self.testee = ErrorCommand(message='xyz')
        self.testee.term = MagicMock(spec=EnhTerm)

    def tearDown(self):
        self.testee = None

    def test_init(self):
        self.assertIsNotNone(self.testee.term)
        self.assertIsNone(self.testee.provider)
        self.assertIsNone(self.testee.result)
        self.assertIsInstance(self.testee.uuid, UUID)
        self.assertEqual(self.testee.message, 'xyz')
        testee = ErrorCommand()
        self.assertEqual(testee.message, '')

    def test_str(self):
        self.assertIn('ErrorCommand', '%s' % self.testee)
        self.assertIn('ErrorCommand', '%r' % self.testee)

    def test_encode(self):
        self.assertEqual(self.testee.encode(), 'xyz')
        self.testee.message = ''
        self.assertEqual(self.testee.encode(), '')

    def test_decode(self):
        self.testee.decode('44')
        self.assertEqual(self.testee.message, '44')
        with self.assertRaises(AssertionError):
            self.testee.decode(44)

    def test_class_id(self):
        self.assertEqual(ErrorCommand.class_id(), 'error')
        self.assertEqual(self.testee.class_id(), 'error')

    def test_execute(self):
        self.assertIsNone(self.testee.execute())
        self.testee.term.error.assert_called_once_with('xyz')


class TestNoOpCommand(TestCase):
    def setUp(self):
        self.testee = NoOpCommand()
        self.testee.term = MagicMock(spec=EnhTerm)

    def tearDown(self):
        self.testee = None

    def test_init(self):
        self.assertIsNotNone(self.testee.term)
        self.assertIsNone(self.testee.provider)
        self.assertIsNone(self.testee.result)
        self.assertIsInstance(self.testee.uuid, UUID)

    def test_str(self):
        self.assertIn('NoOpCommand', '%s' % self.testee)
        self.assertIn('NoOpCommand', '%r' % self.testee)

    def test_encode(self):
        self.assertIsNone(self.testee.encode())

    def test_decode(self):
        self.testee.decode(None)
        with self.assertRaises(AssertionError):
            self.testee.decode(44)

    def test_class_id(self):
        self.assertEqual(NoOpCommand.class_id(), 'noop')
        self.assertEqual(self.testee.class_id(), 'noop')

    def test_execute(self):
        self.assertIsNone(self.testee.execute())


class TestQuitCommand(TestCase):
    def setUp(self):
        self.testee = QuitCommand(reason='xyz')
        self.testee.term = MagicMock(spec=EnhTerm)

    def tearDown(self):
        self.testee = None

    def test_init(self):
        self.assertIsNotNone(self.testee.term)
        self.assertIsNone(self.testee.provider)
        self.assertIsNone(self.testee.result)
        self.assertIsInstance(self.testee.uuid, UUID)
        self.assertEqual(self.testee.reason, 'xyz')
        testee = QuitCommand()
        self.assertIsNone(testee.reason)

    def test_str(self):
        self.assertIn('QuitCommand', '%s' % self.testee)
        self.assertIn('QuitCommand', '%r' % self.testee)

    def test_encode(self):
        self.assertEqual(self.testee.encode(), 'xyz')
        self.testee.reason = ''
        self.assertEqual(self.testee.encode(), '')

    def test_decode(self):
        self.testee.decode('44')
        self.assertEqual(self.testee.reason, '44')

    def test_class_id(self):
        self.assertEqual(QuitCommand.class_id(), 'quit')
        self.assertEqual(self.testee.class_id(), 'quit')

    def test_execute(self):
        self.assertIsNone(self.testee.execute())


class TestTextCommand(TestCase):
    def setUp(self):
        self.testee = TextCommand(content='xyz')
        self.testee.term = MagicMock(spec=EnhTerm)

    def tearDown(self):
        self.testee = None

    def test_init(self):
        self.assertIsNotNone(self.testee.term)
        self.assertIsNone(self.testee.provider)
        self.assertIsNone(self.testee.result)
        self.assertIsInstance(self.testee.uuid, UUID)
        self.assertEqual(self.testee.content, 'xyz')
        testee = TextCommand()
        self.assertEqual(testee.content, '')

    def test_str(self):
        self.assertIn('TextCommand', '%s' % self.testee)
        self.assertIn('TextCommand', '%r' % self.testee)

    def test_encode(self):
        self.assertEqual(self.testee.encode(), 'xyz')
        self.testee.content = ''
        self.assertEqual(self.testee.encode(), '')

    def test_decode(self):
        self.testee.decode('44')
        self.assertEqual(self.testee.content, '44')

    def test_class_id(self):
        self.assertEqual(TextCommand.class_id(), 'text')
        self.assertEqual(self.testee.class_id(), 'text')

    def test_execute(self):
        self.assertIsNone(self.testee.execute())


class TestUnknownCommand(TestCase):
    def setUp(self):
        self.testee = UnknownCommand(unknown_content='xyz')
        self.testee.term = MagicMock(spec=EnhTerm)

    def tearDown(self):
        self.testee = None

    def test_init(self):
        self.assertIsNotNone(self.testee.term)
        self.assertIsNone(self.testee.provider)
        self.assertIsNone(self.testee.result)
        self.assertIsInstance(self.testee.uuid, UUID)
        self.assertEqual(self.testee.unknown_content, 'xyz')
        testee = UnknownCommand()
        self.assertIsNone(testee.unknown_content)

    def test_str(self):
        self.assertIn('UnknownCommand', '%s' % self.testee)
        self.assertIn('UnknownCommand', '%r' % self.testee)

    def test_encode(self):
        self.assertEqual(self.testee.encode(), 'xyz')
        self.testee.unknown_content = ''
        self.assertEqual(self.testee.encode(), '')

    def test_decode(self):
        self.testee.decode('44')
        self.assertEqual(self.testee.unknown_content, '44')

    def test_class_id(self):
        self.assertEqual(UnknownCommand.class_id(), 'unknown')
        self.assertEqual(self.testee.class_id(), 'unknown')

    def test_execute(self):
        self.assertIsNone(self.testee.execute())
