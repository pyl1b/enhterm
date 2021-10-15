# -*- coding: utf-8 -*-
"""
Predefined commands.
"""
import logging

from enhterm.provider.queue_provider import QueueProvider

from enhterm.errors import QuitError

logger = logging.getLogger('et.argparser')


def do_quit(command):
    raise QuitError


def do_prefix(command, modifiers):
    if len(modifiers) > 2:
        command.term.error(f"Two modifiers at most are accepted: "
                           f"the prefix and the suffix; you "
                           f"provided {len(modifiers)} modifiers.")
        return
    if len(modifiers) == 2:
        prefix = modifiers[0].strip()
        suffix = modifiers[1].strip()
    else:
        prefix = modifiers[0].strip()
        suffix = ''
    if len(prefix):
        prefix = ' ' + prefix
    if len(suffix):
        suffix = ' ' + suffix
    command.term.provider.parser.prefix = prefix
    command.term.provider.parser.prefix = suffix


def do_execute(command, files):
    commands = []
    for file in files:
        with open(file, 'r', encoding='utf-8') as fin:
            for line in fin.readlines():
                line = line.strip()
                if line.startswith('#'):
                    continue
                commands.append(command.term.provider.parser.parse())
    if commands:
        command.term.install_provider(
            QueueProvider(initial=commands, block=False, close_on_empty=True)
        )


def register_commands(subparsers):
    parser_q = subparsers.add_parser(
        'quit', aliases=['q', 'exit'],
        help = "Quit the program",
        description="Quits the interpreter",
        epilog=None
    )
    parser_q.set_defaults(func=do_quit)

    parser_prefix = subparsers.add_parser(
        'wrap-commands', aliases=['wcs'],
        help = "Prefix and/or suffix for commands",
        description="Put a prefix and/or a suffix to all commands executed after this one",
        epilog=None
    )
    parser_prefix.add_argument(
        'modifier',
        narg='+',
        help="Provide one argument to indicate the prefix; provide two to change prefix and suffix"
    )
    parser_prefix.set_defaults(func=do_prefix)

    parser_execute = subparsers.add_parser(
        'execute', aliases=['exec'],
        help="Read the content of a file and execute it",
        description="Reads the file and executes the command one by one",
        epilog="Comments are lines that start with a # character."
    )
    parser_execute.add_argument(
        'files',
        narg='+',
        help="The path of the file to execute"
    )
    parser_execute.set_defaults(func=do_execute)

