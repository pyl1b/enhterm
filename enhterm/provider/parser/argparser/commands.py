# -*- coding: utf-8 -*-
"""
Predefined commands.
"""
import logging
from enhterm.errors import QuitError

logger = logging.getLogger('et.argparser')


def do_quit(command):
    raise QuitError


def register_commands(subparsers):
    parser_q = subparsers.add_parser(
        'quit', aliases=['q', 'exit'],
        help = "Quit the program",
        description="Quits the interpreter",
        epilog=None
    )
    parser_q.set_defaults(func=do_quit)
