# enhterm

enhterm is an [open source](https://github.com/pyl1b/enhterm.git),
MIT licensed, [Cmd-based](https://docs.python.org/3/library/cmd.html)
framework for writing command interpreters.

[![Build Status](https://travis-ci.org/pyl1b/enhterm.svg?branch=master)](https://travis-ci.org/pyl1b/enhterm)
[![Documentation Status](https://readthedocs.org/projects/enhterm/badge/?version=latest)](https://enhterm.readthedocs.io/en/latest/?badge=latest)

enhterm provides a class that extends 
[cmd.Cmd](https://docs.python.org/3/library/cmd.html) 
and which is also intended to be inherited by a user class,
with the end purpose being to create a shell.

Functionality provided by this package is split among mixins, allowing you
to construct your own base class if EnhTerm is not suitable.

As with [cmd.Cmd](https://docs.python.org/3/library/cmd.html), the class
constructed as described above can be used like so:


    from enhterm import EnhTerm

    from enhterm.provider.parser.argparser import ArgParser
    from enhterm.provider.parser.argparser.commands import register_commands
    from enhterm.provider.stream_provider import StreamProvider

    # The stream provider by default reads the input from console.
    provider = StreamProvider()
    
    # The text entered by the user then needs to be interpreted.
    # Here we use an interpreter based on argparse.
    provider.parser = ArgParser(provider=provider)
    subparsers = provider.parser.add_subparsers()
    
    # Add built-in commands.
    register_commands(subparsers)

    # Define you own handler.
    def do_add(command, integers):
        return sum(integers)

    # Add this command to the argparse library.
    parser_add = subparsers.add_parser('add')
    parser_add.add_argument(
         'integers', metavar='int', nargs='+', type=int,
         help='integers to be summed (space separated list)')
    parser_add.set_defaults(func=do_add)


    # Construct the terminal.
    class MyShell(EnhTerm):
        """
        Simple terminal.
        
        Has a command that can add integers and another one
        that quits the interpreter.
        """
        def __init__(self):
            super().__init__(providers=provider)


    if __name__ == '__main__':
        print("Type 'add 1 2 3 4 5 6 7 8 9' and you should get back 45")
        print("Type '-h' to get back the usage")
        MyShell().cmd_loop()


Install
-------

    pip install enhterm

You can also download/clone the source, in which case you have to:

    git clone https://github.com/pyl1b/enhterm.git
    python setup.py install
        
To contribute a patch clone the repo, create a new branch, install in
develop mode:
        
    python setup.py develop

What is included
----------------

Each of the elements below are implemented in a distinct "mixin" class,
which mean that you can create your own combination using EnhTerm class as
a template.

### Command

Allows python strings to be executed as if the user typed the input at the
prompt. This is the base for executing commands in a file.

### Exit

Provides the `exit` command that terminates command loop.

### Help

Provides the `help` command which prints information about
the use of the command while accounting for custom commands 
and shortcuts.

### Log Level

Allows changing logging verbosity by issuing commands like 
`set loglevel debug`. 

### Macro

Can record, remove, list and execute previously recorded commands.

### Messages

Does not expose any commands but provides the class with a standardized
way of issuing messages distinct from the logging mechanism.

### Run

Allows executing multiple commands from a string or from a file.

### Sub-commands

Commands are usually identified by using the first word the user types.
This mixin allows for a more natural way of issuing commands like 
`new macro` instead of `macro new`. Other mixins then add subcommands
in their `__init__` method.
