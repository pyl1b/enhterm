# enhterm

enhterm is Cmd-based framework for writing line-oriented command interpreters.

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
    