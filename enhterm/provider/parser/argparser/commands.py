# -*- coding: utf-8 -*-
"""
Predefined commands.
"""
import logging
import os
import re

from enhterm.provider.queue_provider import QueueProvider

from enhterm.errors import QuitError

logger = logging.getLogger('et.argparser')


def do_quit(command):
    raise QuitError


def do_prefix(command, modifiers, show=False):
    if show:
        command.term.info(f"Current prefix is: {command.term.provider.parser.prefix}")
        command.term.info(f"Current suffix is: {command.term.provider.parser.suffix}")
        return

    if len(modifiers) > 2:
        command.term.error(f"Two modifiers at most are accepted: "
                           f"the prefix and the suffix; you "
                           f"provided {len(modifiers)} modifiers.")
        return
    if len(modifiers) == 2:
        prefix = modifiers[0].lstrip()
        suffix = modifiers[1].rstrip()
    elif len(modifiers) == 1:
        prefix = modifiers[0].lstrip()
        suffix = ''
    else:
        prefix = ''
        suffix = ''
    command.term.provider.parser.prefix = prefix
    command.term.provider.parser.suffix = suffix


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


def do_prompt(command, content):
    command.term.prompt = content


def do_cd(command, directory):
    if len(directory):
        try:
            os.chdir(directory)
        except FileNotFoundError:
            command.term.error("Directory {0} does not exist".format(directory))
        except NotADirectoryError:
            command.term.error("{0} is not a directory".format(directory))
        except PermissionError:
            command.term.error("You do not have permissions to change to {0}".format(directory))


def do_variables(command, pattern=None):
    if pattern:
        pattern = re.compile(pattern)
        for key, value in command.term.items():
            if pattern.search(key):
                command.term.info(f'{key}: {value}')
    else:
        for key, value in command.term.items():
            command.term.info(f'{key}: {value}')


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
        epilog="To only add a suffix provide an empty string as first parameter"
    )
    parser_prefix.add_argument(
        dest='modifiers',
        nargs='*',
        metavar='modifier',
        help="Provide one argument to indicate the prefix; provide two to change prefix and suffix"
    )
    parser_prefix.add_argument(
        '--show', '-s',
        action='store_true',
        help="Print current prefix and suffix"
    )
    parser_prefix.set_defaults(func=do_prefix)

    parser_execute = subparsers.add_parser(
        'execute', aliases=['exec'],
        help="Read the content of a file and execute it",
        description="Reads the file and executes the command one by one",
        epilog="Comments are lines that start with a # character."
    )
    parser_execute.add_argument(
        dest='files',
        nargs='+',
        metavar='file',
        help="The path of the file to execute"
    )
    parser_execute.set_defaults(func=do_execute)

    parser_prompt = subparsers.add_parser(
        'prompt',
        help="Change the prompt displayed on the command line",
        description="Reads the file and executes the command one by one",
        epilog="To use a variable in the prompt use the ${var} notation.\n"
               "Following variables are available:\n"
               "- cd: current directory (full path)\n"
               "- cdn: current directory (only the name)\n"
    )
    parser_prompt.add_argument(
        dest='content',
        help="The new prompt"
    )
    parser_prompt.set_defaults(func=do_prompt)

    parser_cd = subparsers.add_parser(
        'cd',
        help="Change current directory on the local machine",
        description="Changes current directory on the local machine"
    )
    parser_cd.add_argument(
        dest='directory',
        help="The path of the directory to make current"
    )
    parser_cd.set_defaults(func=do_cd)

    parser_variables = subparsers.add_parser(
        'variables',
        help="List variables",
        description="Present variables defined inside the terminal"
    )
    parser_cd.add_argument(
        '--pattern', '-p',
        default=None,
        help="Only print variables that match the pattern"
    )
    parser_variables.set_defaults(func=do_variables)

