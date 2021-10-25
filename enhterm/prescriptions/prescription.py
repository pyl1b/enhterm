import logging
from typing import List, Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from enhterm.prescriptions.context import PrescriptionContext

from enhterm.message import TextParagraph, Message

from enhterm.command import Command
from enhterm.prescriptions.argument import IArgument
from enhterm.prescriptions.errors import (
    PreviousArgumentException, FirstArgumentException, NextArgumentException,
    ExitArgumentsException,
    ShowChoicesException, RetryThisStepException)


class PrescriptionBase:
    """
    A prescription helps you define a text command that the user can
    access either interactively or statically.


    """
    @property
    def name(self) -> str:
        """
        The string that indicates in a word or two what this command does.

        It should only be used for labelling. Use the key to identify commands.
        """
        raise NotImplementedError

    @property
    def key(self) -> str:
        """
        Uniquely identify this prescription amongst others.
        """
        raise NotImplementedError

    @property
    def command(self) -> str:
        """
        The command inserted into the string.
        """
        return self.key

    @property
    def help(self) -> str:
        """
        A one-liner that describes the prescription.
        """
        raise NotImplementedError

    @property
    def description(self) -> str:
        """
        A longer description for the prescription.

        By default this is the same as the help message.
        """
        return self.help

    @property
    def arguments(self) -> List[IArgument]:
        raise NotImplementedError

    def handle_direct_call(self, command: Command, *args, **kwargs):
        """
        Argparse handler invoked by the direct (non-interactive) command.

        :param command: EnhTerm's command instance that is being executed.
        :param args: Received positional arguments.
        :param kwargs: Received keywords arguments.
        """
        raise NotImplementedError

    def prompt_header(self, context: 'PrescriptionContext'):
        """
        Present the user with a prompt for the argument.
        """
        paragraphs = [
            TextParagraph(),
            TextParagraph(),
            TextParagraph(f'# {self.name}'),
            TextParagraph(),
            TextParagraph('|')
        ]

        for part in self.description.splitlines():
            paragraphs.append(
                TextParagraph(f'|  {part}'),
            )
        paragraphs.append(TextParagraph('|'))

        context.term.issue_message(Message(
            severity=logging.INFO,
            paragraphs=paragraphs
        ))

    def handle_interactive_call(self, command: Command, *args, **kwargs):
        """
        Argparse handler invoked by the interactive command.

        The function creates a context for this operation then iterates the arguments
        and asks each instance to retrieve the value for itself from the user.

        The retrieve_interactive method is expected to return the value that is then stored
        inside the context. It can also control the iteration in the arguments by
        raising control exceptions.

        When the user CTRL+C the handler is exited and the user returns to normal prompt.

        To actually perform the acton represented by this prescription the function
        calls handle_direct_call() with collected arguments.

        :param command: EnhTerm's command instance that is being executed.
        :param args: Received positional arguments.
        :param kwargs: Received keywords arguments.
        """
        from enhterm.prescriptions.context import PrescriptionContext
        context = PrescriptionContext(
            term=command.term,
            cmd=command,
            pre=self,
            args=dict((arg.key, None) for arg in self.arguments),
            choices=dict((arg.key, None) for arg in self.arguments),
        )
        self.prompt_header(context)

        i_arg, arg, show_choices, show_prompt = 0, None, False, True
        while True:
            while self.arguments:
                try:
                    arg = self.arguments[i_arg]

                    if show_choices:
                        show_choices = False
                        show_prompt = False
                        arg.show_choices(context)

                    context.args[arg.key] = arg.retrieve_interactive(
                        context=context,
                        i_arg=i_arg,
                        show_prompt=show_prompt
                    )
                except ShowChoicesException:
                    show_choices = True
                    continue
                except PreviousArgumentException:
                    if i_arg > 0:
                        i_arg = i_arg - 1
                    continue
                except NextArgumentException:
                    pass # Handled below
                except FirstArgumentException:
                    i_arg = 0
                    continue
                except ExitArgumentsException:
                    break
                except KeyboardInterrupt:
                    return
                except RetryThisStepException:
                    continue
                finally:
                    show_prompt = True

                i_arg = i_arg + 1
                if i_arg >= len(self.arguments):
                    break

            # Asking for the final confirmation.
            try:
                op = context.final_confirmation()
            except KeyboardInterrupt:
                return

            if op == '':
                break
            elif op == context.prev_item_opcode:
                i_arg = len(self.arguments) - 1
            elif op == context.first_item_opcode:
                i_arg = 0
            else:
                assert False, f'{op} is not an allowed response'

        self.handle_direct_call(*args, command=command, **context.args, **kwargs)

    def install_in_argparse(self, subparsers):
        """
        Installs this prescription as an argparse sub-command.

        :param subparsers: the result of parser.add_subparsers()
        """

        # Create a command.
        parser = subparsers.add_parser(
            self.command,
            help=self.help,
            description=self.description,
        )

        for arg in self.arguments:
            arg.install_in_argparse(parser)

        # Indicate the handler above.
        parser.set_defaults(
            func=self.handle_direct_call,
        )

    def install_interactive(self, subparsers):
        # Create the interactive command.
        i_parser = subparsers.add_parser(
            self.command,
            help=self.help,
            description=self.description,
        )

        # Indicate the handler above.
        i_parser.set_defaults(
            func=self.handle_interactive_call,
        )


class Prescription(PrescriptionBase):
    """
    A prescription helps you define a text command that the user can
    access either interactively or statically.
    """
    def __init__(
            self,
            name: str,
            key: Optional[str] = None,
            help: Optional[str] = None,
            description: Optional[str] = None,
            arguments: Optional[List[IArgument]] = None
    ):
        super().__init__()
        self._name: str = name
        self._key = key if key else name
        self._help = help
        self._description = description if description else help
        self._arguments = arguments if len(arguments) else []

    @property
    def name(self) -> str:
        """
        The string that indicates in a word or two what this command does.

        It should only be used for labelling. Use the key to identify commands.
        """
        return self._name

    @property
    def key(self) -> str:
        """
        Uniquely identify this prescription amongst others.
        """
        return self._key

    @property
    def help(self) -> str:
        """
        A one-liner that describes the prescription.
        """
        return self._help

    @property
    def description(self) -> str:
        """
        A longer description for the prescription.

        By default this is the same as the help message.
        """
        return self._description

    @property
    def arguments(self) -> List[IArgument]:
        return self._arguments
