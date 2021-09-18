# -*- coding: utf-8 -*-
"""
"""
from __future__ import unicode_literals
from __future__ import print_function

import logging
from unittest import TestCase
from unittest.mock import MagicMock

from argparse import Namespace

from enhterm import EnhTerm
from enhterm.command.error import ErrorCommand
from enhterm.command.noop import NoOpCommand
from enhterm.provider.parser.argparser import ArgParser, ArgParseCommand
from enhterm.provider.parser_provider import ParserProvider

logger = logging.getLogger('')


class TestArgParser(TestCase):
    def setUp(self):
        self.term = MagicMock(spec=EnhTerm)
        self.prov = MagicMock(spec=ParserProvider)
        self.testee = ArgParser(provider=self.prov)
        self.prov.term = self.term
        self.testee.provider = self.prov

    def tearDown(self):
        self.testee = None

    def test_init(self):
        testee = ArgParser(provider=self.prov)
        # ============== ArgumentParser ==============
        self.assertEqual(testee.add_help, True)
        self.assertEqual(testee.allow_abbrev, True)
        self.assertEqual(testee.conflict_handler, 'error')
        self.assertEqual(testee.prefix_chars, '-')
        self.assertIsInstance(testee.prog, str)
        self.assertIsNone(testee._subparsers)
        self.assertIsNone(testee.argument_default)
        self.assertIsNone(testee.description)
        self.assertIsNone(testee.epilog)
        self.assertIsNone(testee.fromfile_prefix_chars)
        self.assertIsNone(testee.usage)
        # ================== Parser ==================
        # self.assertIsNone(testee.provider)

    def test_str(self):
        self.assertIn('ArgParser', '%s' % self.testee)
        self.assertIn('ArgParser', '%r' % self.testee)

    def test_parse_wrong_type(self):
        self.testee.add_argument(
            'integers', metavar='int', nargs='+', type=int,
            help='an integer to be summed')

        def do_some_action(command, arguments):
            self.fail()

        self.testee.set_defaults(func=do_some_action)
        result = self.testee.parse("abc")
        self.assertIsInstance(result, ErrorCommand)
        self.term.error.assert_called_once_with(
            "argument int: invalid int value: 'abc'")

    def test_parse(self):
        self.testee.add_argument(
            'integers', metavar='int', nargs='+', type=int,
            help='an integer to be summed')
        check_called = [0]

        def do_some_action(command, integers):
            self.assertIsInstance(command, ArgParseCommand)
            self.assertIsInstance(integers, list)
            check_called[0] = check_called[0] + 1
            return sum(integers)

        self.testee.set_defaults(func=do_some_action)
        result = self.testee.parse('1 2 3')
        self.assertIsInstance(result, ArgParseCommand)
        self.term.error.assert_not_called()
        the_sum = result.execute()
        self.assertEqual(check_called[0], 1)
        self.assertEqual(the_sum, 6)

    def test_help(self):
        self.testee.add_argument(
            'integers', metavar='int', nargs='+', type=int,
            help='an integer to be summed')
        result = self.testee.parse('--help')
        self.assertIsInstance(result, NoOpCommand)
        self.term.info.assert_called_once()

    def test_subparsers(self):

        def do_add(command, integers):
            return sum(integers)
        parser_add = self.testee.add_parser('add')
        parser_add.add_argument(
            'integers', metavar='int', nargs='+', type=int,
            help='an integer to be summed')
        parser_add.set_defaults(func=do_add)

        def do_mul(command, integers):
            value = 1
            for param in integers:
                value = value * param
            return value
        parser_mul = self.testee.add_parser('mul')
        parser_mul.add_argument(
            'integers', metavar='int', nargs='+', type=int,
            help='an integer to be multiplied')
        parser_mul.set_defaults(func=do_mul)

        self.testee.parse('add -h')
        self.term.info.assert_called_once()

        result = self.testee.parse('add 1 2 3')
        self.assertIsInstance(result, ArgParseCommand)
        exec_result = result.execute()
        self.assertEqual(exec_result, 6)

        result = self.testee.parse('mul 10 20 30')
        self.assertIsInstance(result, ArgParseCommand)
        exec_result = result.execute()
        self.assertEqual(exec_result, 6000)


