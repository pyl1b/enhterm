# enhterm

enhterm is Cmd-based framework for writing line-oriented command interpreters.

[![Build Status](https://travis-ci.org/pyl1b/enhterm.svg?branch=master)](https://travis-ci.org/pyl1b/enhterm)

It provides a class that extends [cmd.Cmd](https://docs.python.org/3/library/cmd.html) 
and which is also intended to be inherited by a user class to create a shell.

Functionality provided by this package is split among mixins, allowing you
to construct your own base class if EnhTerm is not suitable.

As with [cmd.Cmd](https://docs.python.org/3/library/cmd.html), the class
constructed as described above can be used like so:

    from enhterm import EnhTerm
    class ExampleShell(EnhTerm):
        pass
    
    if __name__ == '__main__':
        ExampleShell().cmdloop()

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
