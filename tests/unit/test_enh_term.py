# -*- coding: utf-8 -*-
"""
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
from unittest import TestCase
from unittest.mock import MagicMock

from enhterm import EnhTerm
from enhterm.command import Command
from enhterm.provider import Provider
from enhterm.runner import Runner
from enhterm.ser_deser import SerDeSer
from enhterm.term import INITIAL_STATE, POST_LOOP_STATE, GET_COMMAND_STATE, PRE_COMMAND_STATE, EXEC_COMMAND_STATE
from enhterm.watcher import Watcher
from enhterm.watcher.echo import EchoWatcher

logger = logging.getLogger('')


class TestEnhTerm(TestCase):
    def setUp(self):
        self.testee = EnhTerm()

    def tearDown(self):
        self.testee = None

    def test_init(self):
        testee = EnhTerm()
        self.assertFalse(testee.should_stop)
        self.assertEqual(testee.prompt, "> ")
        self.assertIsInstance(testee.runner, Runner)
        self.assertIsInstance(testee.serdeser, SerDeSer)
        self.assertListEqual(testee.provider_stack, [])
        self.assertEqual(len(testee.watchers), 1)
        self.assertIsInstance(testee.watchers[0], EchoWatcher)
        self.assertEqual(testee.state, INITIAL_STATE)

        runner = MagicMock(spec=Runner)
        runner.term = None
        testee = EnhTerm(runner=runner)
        self.assertEqual(testee.runner, runner)
        self.assertEqual(runner.term, testee)

        registry = MagicMock(spec=SerDeSer)
        registry.term = None
        testee = EnhTerm(serdeser=registry)
        self.assertEqual(testee.serdeser, registry)
        self.assertEqual(registry.term, testee)

        providers = [MagicMock(), MagicMock()]
        testee = EnhTerm(providers=providers)
        self.assertListEqual(testee.provider_stack, providers)
        self.assertEqual(providers[0].term, testee)
        self.assertEqual(providers[1].term, testee)

        providers = (MagicMock(), MagicMock())
        testee = EnhTerm(providers=providers)
        self.assertListEqual(testee.provider_stack, list(providers))
        self.assertEqual(providers[0].term, testee)
        self.assertEqual(providers[1].term, testee)

        provider = MagicMock(spec=Provider)
        testee = EnhTerm(providers=provider)
        self.assertListEqual(testee.provider_stack, [provider])
        self.assertEqual(provider.term, testee)

        with self.assertRaises(ValueError):
            EnhTerm(providers=MagicMock())

        watchers = [MagicMock(), MagicMock()]
        testee = EnhTerm(watchers=watchers)
        self.assertListEqual(testee.watchers, watchers)
        self.assertEqual(watchers[0].term, testee)
        self.assertEqual(watchers[1].term, testee)

        watchers = (MagicMock(), MagicMock())
        testee = EnhTerm(watchers=watchers)
        self.assertListEqual(testee.watchers, list(watchers))
        self.assertEqual(watchers[0].term, testee)
        self.assertEqual(watchers[1].term, testee)

        watcher = MagicMock(spec=Watcher)
        testee = EnhTerm(watchers=watcher)
        self.assertListEqual(testee.watchers, [watcher])
        self.assertEqual(watcher.term, testee)

        with self.assertRaises(ValueError):
            EnhTerm(watchers=MagicMock())

    def test_str(self):
        self.assertIn('EnhTerm', '%s' % self.testee)
        self.assertIn('EnhTerm', '%r' % self.testee)

    def test_provider(self):
        self.testee.provider_stack = []
        with self.assertRaises(IndexError):
            self.testee.provider

        p1 = MagicMock(spec=Provider)
        self.testee.provider_stack = [p1]
        self.assertEqual(p1, self.testee.provider)

        p2 = MagicMock(spec=Provider)
        self.testee.provider_stack = [p1, p2]
        self.assertEqual(p2, self.testee.provider)

    def test_cmd_loop(self):
        self.testee.pre_loop = MagicMock()
        self.testee.post_loop = MagicMock()
        self.testee.should_stop = True
        self.testee.cmd_loop()
        self.assertEqual(self.testee.state, POST_LOOP_STATE)
        self.testee.pre_loop.assert_called_once()
        self.testee.post_loop.assert_called_once()

        self.testee.should_stop = False
        called = [0]

        def one_loop():
            called[0] = called[0] + 1
            self.testee.should_stop = True

        self.testee.one_loop = one_loop
        self.testee.cmd_loop()
        self.assertEqual(called[0], 1)

    def test_one_loop(self):
        self.testee.should_stop = False
        self.testee.get_command = MagicMock(return_value=None)
        self.assertFalse(self.testee.one_loop())
        self.assertTrue(self.testee.should_stop)
        self.assertEqual(self.testee.state, GET_COMMAND_STATE)

        self.testee.should_stop = False
        command = MagicMock(spec=Command)
        self.testee.get_command = MagicMock(return_value=command)
        self.testee.pre_cmd = MagicMock(return_value=None)
        self.assertFalse(self.testee.one_loop())
        self.assertTrue(self.testee.should_stop)
        self.assertEqual(self.testee.state, PRE_COMMAND_STATE)

        self.testee.should_stop = False
        command = MagicMock(spec=Command)
        self.testee.get_command = MagicMock(return_value=command)
        self.testee.pre_cmd = MagicMock(return_value=command)
        self.testee.execute_command = MagicMock(return_value='x')
        self.testee.post_cmd = MagicMock(return_value=False)
        self.assertFalse(self.testee.one_loop())
        self.assertTrue(self.testee.should_stop)
        self.assertEqual(self.testee.state, EXEC_COMMAND_STATE)

        self.testee.should_stop = False
        command = MagicMock(spec=Command)
        self.testee.get_command = MagicMock(return_value=command)
        self.testee.pre_cmd = MagicMock(return_value=command)
        self.testee.execute_command = MagicMock(return_value='x')
        self.testee.post_cmd = MagicMock(return_value=True)
        self.assertTrue(self.testee.one_loop())
        self.assertFalse(self.testee.should_stop)
        self.assertEqual(self.testee.state, EXEC_COMMAND_STATE)
        self.assertEqual(command.result, 'x')

    def test_pre_loop(self):
        w1 = MagicMock(spec=Watcher)
        w2 = MagicMock(spec=Watcher)
        self.testee.watchers = [w1, w2]
        self.testee.pre_loop()
        w1.pre_loop.assert_called_once()

        w2 = MagicMock(spec=Watcher)
        self.testee.watchers = [w1, w2]
        w2.pre_loop.side_effect = SystemExit
        with self.assertRaises(SystemExit):
            self.testee.pre_loop()

        w2 = MagicMock(spec=Watcher)
        self.testee.handle_watcher_exception = MagicMock()
        self.testee.watchers = [w1, w2]
        ie = IndexError()
        w2.pre_loop.side_effect = ie
        self.testee.pre_loop()
        self.testee.handle_watcher_exception.assert_called_once_with(
            w2, 'pre_loop', ie)

    def test_post_loop(self):
        w1 = MagicMock(spec=Watcher)
        w2 = MagicMock(spec=Watcher)
        self.testee.watchers = [w1, w2]
        self.testee.post_loop()
        w1.post_loop.assert_called_once()

        w2 = MagicMock(spec=Watcher)
        self.testee.watchers = [w1, w2]
        w2.post_loop.side_effect = SystemExit
        with self.assertRaises(SystemExit):
            self.testee.post_loop()

        w2 = MagicMock(spec=Watcher)
        self.testee.handle_watcher_exception = MagicMock()
        self.testee.watchers = [w1, w2]
        ie = IndexError()
        w2.post_loop.side_effect = ie
        self.testee.post_loop()
        self.testee.handle_watcher_exception.assert_called_once_with(
            w2, 'post_loop', ie)

    def test_pre_cmd(self):
        command = MagicMock(spec=Command)

        w1 = MagicMock(spec=Watcher)
        w2 = MagicMock(spec=Watcher)
        self.testee.watchers = [w1, w2]
        self.assertEqual(self.testee.pre_cmd(command), command)
        w1.pre_cmd.assert_called_once()

        w2 = MagicMock(spec=Watcher)
        self.testee.watchers = [w1, w2]
        w2.pre_cmd.side_effect = SystemExit
        with self.assertRaises(SystemExit):
            self.testee.pre_cmd(command)

        w2 = MagicMock(spec=Watcher)
        self.testee.handle_watcher_exception = MagicMock()
        self.testee.watchers = [w1, w2]
        ie = IndexError()
        w2.pre_cmd.side_effect = ie
        self.assertEqual(self.testee.pre_cmd(command), command)
        self.testee.handle_watcher_exception.assert_called_once_with(
            w2, 'pre_cmd', ie)

    def test_post_cmd(self):
        command = MagicMock(spec=Command)

        w1 = MagicMock(spec=Watcher)
        w2 = MagicMock(spec=Watcher)
        self.testee.watchers = [w1, w2]
        self.assertTrue(self.testee.post_cmd(command))
        w1.post_cmd.assert_called_once()

        w2 = MagicMock(spec=Watcher)
        self.testee.watchers = [w1, w2]
        w2.post_cmd.side_effect = SystemExit
        with self.assertRaises(SystemExit):
            self.testee.post_cmd(command)

        w2 = MagicMock(spec=Watcher)
        self.testee.handle_watcher_exception = MagicMock()
        self.testee.watchers = [w1, w2]
        ie = IndexError()
        w2.post_cmd.side_effect = ie
        self.assertTrue(self.testee.post_cmd(command))
        self.testee.handle_watcher_exception.assert_called_once_with(
            w2, 'post_cmd', ie)

    def test_get_command(self):
        self.fail()

    def test_execute_command(self):
        self.fail()

    def test_install_provider(self):
        self.fail()

    def test_uninstall_provider(self):
        self.fail()

    def test_handle_watcher_exception(self):
        self.fail()

    def test_handle_provider_exception(self):
        self.fail()

    def test_pre_loop_state(self):
        self.fail()

    def test_get_command_state(self):
        self.fail()

    def test_pre_command_state(self):
        self.fail()

    def test_execute_command_state(self):
        self.fail()

    def test_post_loop_state(self):
        self.fail()

    def test_info(self):
        self.fail()

    def test_warning(self):
        self.fail()

    def test_error(self):
        self.fail()

    def test_issue_message(self):
        self.fail()
