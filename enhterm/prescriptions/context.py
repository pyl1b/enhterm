import logging
import re
from dataclasses import dataclass
from typing import Optional, Dict, Union, List, Pattern

from enhterm.message import Message, TextParagraph

from enhterm.command import Command

from enhterm import EnhTerm
from enhterm.prescriptions.prescription import PrescriptionBase


@dataclass
class PrescriptionContext:
    """
    When running a prescription a context is created and passed around with actual values.

    Attributes
    ----------

    term:
        The terminal that runs this prescription
    cmd:
        The command that triggered this prescription, if any
    pre:
        The prescription that is being executed.
    args:
        The values for arguments. the keys are the argument keys. Values can be:
        - None if the user did not fill that argument
        - a list if the argument is a list argument
        - a string otherwise
    choices:
        Choices retrieved on demand.
    """
    term: EnhTerm
    cmd: Optional[Command]
    pre: PrescriptionBase
    args: Dict[str,Union[str, None, List[str]]]
    choices: Dict[str,Union[str, None, List[str]]]

    show_options_opcode: str = '?'
    prev_item_opcode: str = '<'
    next_item_opcode: str = '>'
    first_item_opcode: str = '!<'
    last_item_opcode: str = '>!'
    first_list_item_opcode: str = '[<'
    last_list_item_opcode: str = '>]'
    remove_list_item_opcode: str = '[x]'
    option_pattern: Pattern = re.compile(r'^\[([0-9]+)\]')
    escaped_option_pattern: Pattern = re.compile(r'^\\(\[[0-9]+\])')

    def final_confirmation(self):
        """
        Presents the values stored in the context and asks for the go-ahead.
        :returns: opcode for first, opcode for previous or an empty string
        :raises KeyboardInterrupt: to terminate the command
        """

        if not self.pre.arguments:
            return

        paragraphs = [
            TextParagraph(f'## {self.pre.name}'),
            TextParagraph(),
        ]

        for arg in self.pre.arguments:
            value = self.args[arg.key]
            if arg.is_list:
                paragraphs.append(
                    TextParagraph(f'  {arg.name}:')
                )
                for list_item in value:
                    paragraphs.append(
                        TextParagraph(f'   - {list_item}')
                    )
            else:
                paragraphs.append(
                    TextParagraph(f'  {arg.name}: {value}')
                )
        self.term.issue_message(
            Message(
                severity=logging.INFO,
                paragraphs=paragraphs
            )
        )
        while True:
            result = input(
                f'Proceed [y | yes | n | no | {self.prev_item_opcode} | {self.first_item_opcode} | CTRL+C] <yes>? '
            ).lower()
            valid_options = (
                self.prev_item_opcode,
                self.first_item_opcode,
                '',
                'y',
                'yes',
                'ok',
                'n',
                'no'
            )
            if result in valid_options:
                if result in ('y', 'yes', 'ok'):
                    result = ''
                elif result in ('n', 'no'):
                    raise KeyboardInterrupt
                return result
            self.term.issue_message(
                Message(
                    severity=logging.ERROR,
                    paragraphs=[
                        TextParagraph('Invalid choice. Valid options are:'),
                        TextParagraph('- empty to use the default'),
                        TextParagraph('- y or yes to explicitly indicate you choice'),
                        TextParagraph('- n or no or CTRL+C to exit the command without submit'),
                        TextParagraph(f'- {self.first_item_opcode} to edit first argument'),
                        TextParagraph(f'- {self.prev_item_opcode} to edit last argument'),
                    ]
                )
            )
