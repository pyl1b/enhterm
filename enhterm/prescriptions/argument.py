import logging
import sys
from argparse import ArgumentTypeError
from typing import List, Union, Any, Tuple, TYPE_CHECKING, Optional

from enhterm.message import TextParagraph, Message

if TYPE_CHECKING:
    from enhterm.prescriptions.context import PrescriptionContext

from enhterm.prescriptions.errors import (
    PreviousArgumentException, NextArgumentException, FirstArgumentException,
    ExitArgumentsException, PreviousInListException, NextInListException,
    FirstInListException, EndOfListException,
    RemoveListItemException,
    ShowChoicesException, RetryThisStepException)
from enhterm.prescriptions.mixins import (
    IntArgMixin, FloatArgMixin, BoolArgMixin, MinMaxMixin, MinMaxStrMixin
)


class IArgument:
    """
    One of the arguments in a prescription.
    """

    @property
    def name(self) -> str:
        """
        The string that indicates in a word or two what this argument does.

        It should only be used for labelling. Use the key to identify arguments.
        """
        raise NotImplementedError

    @property
    def key(self) -> str:
        """
        Uniquely identify this argument amongst others.
        """
        raise NotImplementedError

    @property
    def argument(self) -> str:
        """
        The argument to use in the actual command.
        """
        return self.key

    @property
    def short(self) -> Union[str, None]:
        """
        The short argument to use in the actual command.
        """
        return None

    @property
    def optional(self) -> bool:
        """
        Weather this argument is optional or required.

        This decides if this is a positional argument or one prefixed by a double-dash.
        """
        return True

    @property
    def description(self) -> str:
        """
        Describes the argument to the final user.
        """
        raise NotImplementedError

    @property
    def action(self):
        """
        The basic type of action to be taken when this argument
        is encountered at the command line.

        - store: This just stores the argument’s value. This is the default action.
        - store_const: This stores the value specified by the const keyword argument.
        - store_true: Stores True if the argument is encountered.
        - store_false: Stores False if the argument is encountered.
        - append: This stores a list, and appends each argument value to the list.
        - append_const: This stores a list, and appends the value specified
            by the const keyword argument to the list. (Note that the const
            keyword argument defaults to None.) The 'append_const' action
            is typically useful when multiple arguments need to store
            constants to the same list.
        - count: This counts the number of times a keyword argument occurs.
            For example, this is useful for increasing verbosity levels.

        """
        return 'store'

    @property
    def nargs(self) -> str:
        """
        The number of command-line arguments that should be consumed.

        Possible values:
        - N A number indicating the exact number of values expected
        - ? One argument will be consumed from the command line if possible,
          and produced as a single item. If no command-line argument is
          present, the value from default will be produced.
          Note that for optional arguments, there is an additional case -
          the option string is present but not followed by a
          command-line argument. In this case the value from
          const will be produced.
        - * All command-line arguments present are gathered into a list.
        - + All command-line arguments present are gathered into a list
          but at least one is required
        """
        raise NotImplementedError

    @property
    def const(self):
        """
        A constant value required by some action and nargs selections.
        """
        raise NotImplementedError

    @property
    def default(self):
        """
        The value produced if the argument is absent from the
        command line and if it is absent from the namespace object.
        """
        raise NotImplementedError

    @property
    def metavar(self):
        """
        A name for the argument in usage messages.
        """
        return None

    @property
    def dest(self):
        """
        The destination member where it should be stored.
        """
        return self.key

    @property
    def choices(self):
        """
        Allowable values for the argument.

        These values are immediately available and are present both
        in direct mode and in interactive mode.

        If this field provides choices and `get_choices_label()`
        returns None the result of this property will be returned by
        `get_choices()`.

        However, if `get_choices_label()` does return a label
        then the values in this member will be ignored
        and those returend by `retrieve_choices()` will be used
        when the users asks using ? code.
        """
        raise NotImplementedError

    @property
    def get_choices_label(self):
        """
        The label that indicates to the user that aa list of
        possible values can be presented on demand.

        This is useful when the list of choices is expensive to obtain.

        Note that the argument must then implement get_choices() method.
        """
        return None

    def retrieve_choices(self, context: 'PrescriptionContext') -> List[Any]:
        """
        Implement this function to retrieve choices on demand.

        The `show_choices()` method will call this one if the
        choices are not in cache or we're forced to do direct call.

        Note that this method is only called if `get_choices_label()` returns
        something other than None, otherwise it is assumed that
        there in no implementation for `retrieve_choices()`.
        """
        raise NotImplementedError

    def get_choices(
            self,
            context: 'PrescriptionContext',
            use_cache: bool = True,
            only_cache: bool = False
    ) -> Union[List[str], None]:
        """
        Retrieve the choices either from cache of by asking the retrieve_choices implementation.

        :param context: The context of the command.
        :param use_cache: Are we allowed to use the cached values or we should
            retrieve them anew?
        :param only_cache: prevent the retrieval of choices.
        :returns: The list of choices or None if there anren't any.
        """
        choices: Union[List[str], None] = None
        if self.get_choices_label:
            if use_cache:
                choices = context.choices.get(self.key, None)
            if choices is None and not only_cache:
                choices = self.retrieve_choices(context)
                context.choices[self.key] = choices
        else:
            choices = self.choices
        return choices

    def value_factory(self, value):
        """
        The raw value will be passed through this method.
        """
        return str(value)

    def candidates(self) -> List[str]:
        """
        Retrieves candidate values for filling in this argument.

        :return: A list of options that will be presented to the user to choose from.
        """
        raise NotImplementedError

    def prompt_header(self, context: 'PrescriptionContext', i_arg: int):
        """
        Present the user with a prompt for the argument.
        """
        paragraphs = [
            TextParagraph(),
            TextParagraph(),
            TextParagraph(f'## {i_arg + 1}.  {self.name}'),
            TextParagraph(),
            TextParagraph('|')
        ]

        for part in self.description.splitlines():
            paragraphs.append(
                TextParagraph(f'|  {part}'),
            )
        paragraphs.append(TextParagraph('|'))

        get_choices_label = self.get_choices_label
        if get_choices_label:
            for part in get_choices_label.splitlines():
                paragraphs.append(
                    TextParagraph(f'|  {part}'),
                )
            paragraphs.append(TextParagraph('|'))

        paragraphs.append(TextParagraph())
        context.term.issue_message(Message(
            severity=logging.INFO,
            paragraphs=paragraphs
        ))

    def install_in_argparse(self, parser):
        """
        Installs this argument as an argparse argument.

        :param parser: the result of parser.subparsers.add_parser()
        """
        args = []
        kwargs = {}

        if self.optional:
            # If the argument is required the name gets
            # passed down as a keyword argument.
            args.append(f'--{self.argument}')

            dest = self.dest
            if dest is not None:
                kwargs['dest'] = dest

            short = self.short
            if short is not None:
                args.append(f'-{short}')
        else:
            args.append(self.argument)

        action = self.action
        if action is not None:
            kwargs['action'] = action

        nargs = self.nargs
        if nargs is not None:
            kwargs['nargs'] = nargs

        const = self.const
        if const is not None:
            kwargs['const'] = const

        choices = self.choices
        if choices is not None:
            kwargs['choices'] = choices

        metavar = self.metavar
        if metavar is not None:
            kwargs['metavar'] = metavar

        default = self.default
        if default is not None:
            kwargs['default'] = default

        parser.add_argument(
            *args,
            help=self.description,
            type=self.value_factory,
            **kwargs,
        )

    @property
    def is_list(self) -> bool:
        """
        Determine if the value of this argument is a list or a single value.
        :return: True if it is a list.
        """
        nargs = self.nargs
        if nargs is None:
            action = self.action
            return action not in (None, 'store', 'store_const', 'store_true', 'store_false', 'count')
        elif nargs == '?':
            return False
        else:
            return True

    @property
    def min_max_count(self) -> Tuple[int, int]:
        """
        Get the minimum and maximum number of values that this argument can take.
        """
        nargs = self.nargs
        if nargs is None:
            action = self.action
            if action in (None, 'store', 'store_const', 'store_true', 'store_false', 'count'):
                return 0 if self.optional else 1, 1
            else:
                return 0 if self.optional else 1, sys.maxsize
        elif nargs == '?':
            return 0, 1
        elif nargs in ('+', '*'):
            return 1, sys.maxsize
        else:
            nargs = int(nargs)
            return nargs, nargs

    def interactive_prompt(
            self,
            context: 'PrescriptionContext',
            i_arg: int,
            first_time_prompt: bool,
            list_current_value: Tuple[int, Any] = None
    ):
        """
        Compute the prompt to show to the user before asking for a value.

        :param context: The context for this call.
        :param i_arg: The index of this argument in the list
        :param first_time_prompt: Is this the first time that the user is
            asked to enter a value here?
        :param list_current_value: When editing a list value this will be set to current value
        :returns: The value to be stored in the context for this argument.
        """
        is_list = self.is_list

        if first_time_prompt:
            self.prompt_header(context, i_arg)
            input_prompt = '   Your input'
        else:
            input_prompt = f'   {self.name}'

        if is_list:
            input_prompt = f'{input_prompt}[#{list_current_value[0]}]'

        # Print choices in the prompt if present.
        choices = self.choices
        if choices:
            input_prompt = f'{input_prompt} [{" | ".join(choices)}]'

        # Default value is either previously entered value
        # or default set in the argument instance.
        default = None
        if not is_list:
            crt_val = context.args[self.key]
            if crt_val is not None:
                default = crt_val
            elif self.default is not None:
                default = self.default
        else:
            default = list_current_value[1]

        # Show the default in prompt if it exists.
        if default is not None:
            input_prompt = f'{input_prompt} <{default}>: '
        else:
            input_prompt = f'{input_prompt}: '

        return input_prompt

    def resolve_escape_codes(self, result, context: 'PrescriptionContext') -> str:
        """
        The funct`ion will handle some input as navigation commands:
        - `<` indicates that the prompt should go to the previous argument;
        - `>` indicates that the prompt should go to the next argument;
        - `!<` indicates that the prompt should go to the first argument;
        - `>!` indicates that the prompt should exit argument retrieval loop.

        To enter these values for an argument prefix the value with a backlash
        (`\\<`, `\\>`, `\\!<`, `\\>!`).
        :param result: Initial result
        :param context: The context (used for choices)
        :return: result after processing
        """
        if not isinstance(result, str):
            return result
        is_list = self.is_list

        match_option = context.option_pattern.match(result)
        if match_option:
            index = int(match_option.group(1))
            choices = context.choices.get(self.key, None)
            if choices is None:
                context.term.error(f"There are no choices for {self.name}")
                raise RetryThisStepException
            if index < 0 or index >= len(choices):
                context.term.error(
                    f"Valid indexes are between 0 and {len(choices)-1} for {self.name} choices"
                )
                raise ShowChoicesException
            choice = choices[index]

            # The choice can be None, a string or a tuple of
            # two items, first being the key and second being the label.
            if choice:
                if not isinstance(choice, str):
                    choice = choice[0]
            return choice

        match_option = context.escaped_option_pattern.match(result)
        if match_option:
            return match_option.group(1)

        if result == context.show_options_opcode:
            if self.get_choices_label:
                raise ShowChoicesException
        elif result == '\\' + context.show_options_opcode:
            result = context.show_options_opcode
        elif result == context.prev_item_opcode:
            if is_list:
                raise PreviousInListException
            else:
                raise PreviousArgumentException
        elif result == '\\' + context.prev_item_opcode:
            result = context.prev_item_opcode
        elif result == context.next_item_opcode:
            if is_list:
                raise NextInListException
            else:
                raise NextArgumentException
        elif result == '\\' + context.next_item_opcode:
            result = context.next_item_opcode
        elif result == context.first_item_opcode:
            raise FirstArgumentException
        elif result == '\\' + context.first_item_opcode:
            result = context.first_item_opcode
        elif result == context.last_item_opcode:
            raise ExitArgumentsException
        elif result == '\\' + context.last_item_opcode:
            result = context.last_item_opcode
        elif self.is_list:
            if result == context.first_list_item_opcode:
                raise FirstInListException
            elif result == '\\' + context.first_list_item_opcode:
                result = context.first_list_item_opcode
            elif result == context.last_list_item_opcode:
                raise EndOfListException
            elif result == '\\' + context.last_list_item_opcode:
                result = context.last_list_item_opcode
            elif result == context.remove_list_item_opcode:
                raise RemoveListItemException
            elif result == '\\' + context.remove_list_item_opcode:
                result = context.remove_list_item_opcode
        return result

    def interactive_input(
            self,
            context: 'PrescriptionContext',
            i_arg: int,
            first_time_prompt: bool,
            list_current_value: Tuple[int, Any] = None
    ):
        """
        Retrieve the input from the user.

        :param context: The context for this call.
        :param i_arg: The index of this argument in the list
        :param first_time_prompt: Is this the first time that the user is
            asked to enter a value here?
        :param list_current_value: When editing a list value this will be set to current value
        :returns: The value to be stored in the context for this argument.
        """
        result = input(self.interactive_prompt(
            context,
            i_arg,
            first_time_prompt,
            list_current_value
        ))

        # Either use the entered value or, if missing, the default
        result = result.strip()
        if not result:
            if self.is_list:
                result = list_current_value[1]
            else:
                crt_val = context.args[self.key]
                if crt_val is not None:
                    result = crt_val
                elif self.default is not None:
                    result = self.default
                else:
                    result = None

        result = self.resolve_escape_codes(result, context)

        # If we have choices then validate against them
        # We could do
        #       choices = self.get_choices(context, only_cache=True)
        # but the choices may actually be a list of stuff to avoid
        # so we should implement a flag that indicates wether the choices
        # are to be inforced or not.
        #
        choices = self.choices
        if choices is not None and result is not None:
            choices = [
                (choice if isinstance(choice, str) else choice[0])
                for choice in choices
            ]
            if result not in choices:
                paragraphs = [
                    TextParagraph(),
                    TextParagraph('The input must be one of the allowable choices:')
                ]
                for choice in choices:
                    if isinstance(choice, str):
                        paragraphs.append(TextParagraph(f'- {choice}'))
                    else:
                        paragraphs.append(TextParagraph(f'- {choice[0]} ({choice[1]})'))
                context.term.issue_message(Message(
                    severity=logging.ERROR,
                    paragraphs=paragraphs
                ))
                raise RetryThisStepException

        if result is not None:
            try:
                result = self.value_factory(result)
            except ArgumentTypeError as exc:
                context.term.error(f"Invalid input. {exc}")
                raise RetryThisStepException
        return result

    def retrieve_list_interactive(self, context: 'PrescriptionContext', i_arg: int) -> Any:
        """
        Retrieve the value of an argument that expects a list by asking the user.

        :param context: The context for this call.
        :param i_arg: The index of this argument in the list
        :returns: The value to be stored in the context for this argument.
        """
        min_count, max_count = self.min_max_count
        crt_val = context.args[self.key]
        new_list = [] if crt_val is None else list(crt_val)
        i_list = len(new_list)
        first_time_prompt = True
        show_choices = False

        while True:
            result = None
            try:
                if show_choices:
                    show_choices = False
                    self.show_choices(context)

                result = self.interactive_input(
                    context=context,
                    i_arg=i_arg,
                    first_time_prompt=first_time_prompt,
                    list_current_value=(
                        i_list,
                        new_list[i_list] if i_list < len(new_list) else None
                    )
                )
            except RetryThisStepException:
                continue
            except ShowChoicesException:
                show_choices = True
                continue
            except PreviousInListException:
                if i_list > 0:
                    i_list = i_list - 1
                else:
                    context.args[self.key] = new_list
                    raise PreviousArgumentException
                continue
            except NextInListException:
                if i_list < len(new_list):
                    i_list = i_list + 1
                else:
                    context.args[self.key] = new_list
                    raise NextArgumentException
                continue
            except FirstInListException:
                i_list = 0
                continue
            except EndOfListException:
                i_list = len(new_list)
                continue
            except RemoveListItemException:
                if i_list < len(new_list):
                    del new_list[i_list]
                else:
                    context.term.error(
                        'Nothing to delete; you need to be editing '
                        'an item for this command to work'
                    )
                continue
            except (
                    PreviousArgumentException,
                    NextArgumentException,
                    FirstArgumentException,
                    ExitArgumentsException
            ) as exc:
                context.args[self.key] = new_list
                raise exc
            finally:
                first_time_prompt = False

            # Empty input.
            if not result:
                if len(new_list) < min_count:
                    if min_count == 1:
                        context.term.error(
                            f'At least one value is required by the {self.name}'
                        )
                    else:
                        context.term.error(
                            f'At least {min_count} values are required by the {self.name}'
                        )
                    continue
                else:
                    return new_list

            # Non-empty input that replaces a previous value
            if i_list < len(new_list):
                new_list[i_list] = result
            else:
                new_list.append(result)
            i_list = i_list + 1

    def retrieve_interactive(
            self,
            context: 'PrescriptionContext',
            i_arg: int,
            show_prompt: bool = True
    ) -> Any:
        """
        Retrieve the value of an argument by asking the user.

        :param context: The context for this call.
        :param i_arg: The index of this argument in the list
        :returns: The value to be stored in the context for this argument.
        """
        if self.is_list:
            return self.retrieve_list_interactive(context, i_arg)

        min_count = self.min_max_count[0]
        first_time_prompt = show_prompt
        while True:
            # Finally ask the user for input.
            result = self.interactive_input(context, i_arg, first_time_prompt)
            first_time_prompt = False

            # See if this argument is required.
            if not result:
                if min_count:
                    # No value is unacceptable so ask again
                    context.term.error(f'A value is required for {self.name}')
                    continue
                else:
                    # No value is acceptable so exit
                    return None

            return result

    def show_choices(
            self,
            context: 'PrescriptionContext',
            use_cache: bool = True
    ):
        """
        The user asks us to present the choices.

        :param context: The context of the command.
        :param use_cache: Are we allowed to use the cached values or we should
            retrieve them anew?
        """
        choices: Optional[List[str]] = self.get_choices(context, use_cache)
        if not choices:
            context.term.error(f"There are no choices for {self.name}")
            return

        options_paragraphs = []
        for i, choice in enumerate(choices):
            if isinstance(choice, str):
                options_paragraphs.append(TextParagraph(f'- [{i}]: {choice}'))
            else:
                options_paragraphs.append(TextParagraph(f'- [{i}]: {choice[0]} ({choice[1]})'))

        context.term.issue_message(
            Message(
                term=context.term,
                severity=logging.INFO,
                paragraphs=options_paragraphs
            )
        )


class Argument(IArgument):
    """
    One of the arguments in a prescription.
    """
    def __init__(
            self,
            name: str,
            key: str = '',
            short: str = None,
            description: str = '',
            optional: bool = True,
            action: str = 'store',
            nargs: str = None,
            const: str = None,
            default: Any = None,
            choices: List[str] = None,
            get_choices_label: str = None
    ):
        super().__init__()
        self._name: str = name
        self._key: str = key if key else name
        self._short: str = short
        self._optional: bool = optional
        self._description: str = description
        self._action: str = action
        self._nargs: str = nargs
        self._const: str = const
        self._default: str = default
        self._choices: List[str] = choices
        self._get_choices_label: str = get_choices_label

    @property
    def name(self) -> str:
        """
        The string that indicates in a word or two what this argument does.

        It should only be used for labelling. Use the key to identify arguments.
        """
        return self._name

    @property
    def key(self) -> str:
        """
        Uniquely identify this argument amongst others.
        """
        return self._key

    @property
    def short(self) -> str:
        """
        The short argument to use in the actual command.
        """
        return self._short

    @property
    def optional(self) -> bool:
        """
        Weather this argument is optional or required.
        """
        return self._optional

    @property
    def description(self) -> str:
        """
        Describes the argument to the final user.
        """
        return self._description

    @property
    def action(self):
        return self._action

    @property
    def nargs(self) -> str:
        """
        The number of command-line arguments that should be consumed.
        """
        return self._nargs

    @property
    def const(self):
        """
        A constant value required by some action and nargs selections.
        """
        return self._const

    @property
    def default(self):
        """
        The value produced if the argument is absent from the
        command line and if it is absent from the namespace object.
        """
        return self._default

    @property
    def choices(self):
        """
        A container of the allowable values for the argument.
        """
        return self._choices

    @property
    def get_choices_label(self):
        """
        The label that indicates to the user that aa list of
        possible values can be presented on demand.

        This is useful when the list of choices is expensive to obtain.

        Note that the argument must then implement get_choices() method.
        """
        return self._get_choices_label

    def to_string(self, value):
        """
        Convert the argument back to string.

        :param value: The value for the argument.
        :return: String representation in the command line.
        """
        if value is None:
            return ''

        quote = '"'
        escaped_quote = r'\"'
        if self.optional:
            if isinstance(value, (list, set, tuple)):

                return ' '.join([
                    f'--{self.key} "{str(sub_value).replace(quote, escaped_quote)}"'
                    for sub_value in value
                ])
            else:
                return f'--{self.key} "{str(value).replace(quote, escaped_quote)}"'
        else:
            return f'"{str(value).replace(quote, escaped_quote)}"'


class IntArgument(IntArgMixin, Argument):
    """
    An argument that expects an integer.
    """
    pass


class FloatArgument(FloatArgMixin, Argument):
    """
    An argument that expects an integer.
    """
    pass


class LimitedIntArgument(MinMaxMixin, IntArgMixin, Argument):
    """
    An argument that expects an integer.
    """
    pass


class LimitedFloatArgument(MinMaxMixin, FloatArgMixin, Argument):
    """
    An argument that expects an integer.
    """
    pass


class BoolArgument(BoolArgMixin, Argument):
    """
    An argument that expects an integer.
    """
    pass


class LimitedStringArgument(MinMaxStrMixin, Argument):
    """
    An argument that expects an integer.
    """
    pass
