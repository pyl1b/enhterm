from argparse import ArgumentTypeError


class CustomDestinationMixin:
    """
    Add to your class the ability to change the destination variable to a
    customizable value.
    """
    def __init__(self, dest=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dest = dest

    @property
    def dest(self):
        """
        The destination member where it should be stored.
        """
        return self._dest


class CustomMetavarMixin:
    """
    Add to your class the ability to change the meta variable to a
    customizable value.
    """
    def __init__(self, metavar=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._metavar = metavar

    @property
    def metavar(self):
        """
        A name for the argument in usage messages.
        """
        return self._metavar


truthy = ('ON', 'YES', 'TRUE', 'Y', 'T', '1')
falsly = ('OFF', 'NO', 'FALSE', 'N', 'F', '0')


class BoolArgMixin:
    """
    Makes sure that the value passed is an integer.
    """
    def value_factory(self, value):
        """
        The raw value will be passed through this method.
        """
        if isinstance(value, str):
            if len(value) == 0:
                value = False
            else:
                value = value.strip().upper()
                if value in truthy:
                    value = True
                elif value in falsly:
                    value = False
                else:
                    raise ArgumentTypeError(
                        f'{self.name} must be a boolean value like {falsly} and {truthy}; {value} is not'
                    )
        else:
            try:
                value = bool(value)
            except (TypeError, ValueError):
                raise ArgumentTypeError(
                    f'{self.name} must be a boolean value; {value} is not'
                )
        return value


class IntArgMixin:
    """
    Makes sure that the value passed is an integer.
    """
    def value_factory(self, value):
        """
        The raw value will be passed through this method.
        """
        try:
            return int(value)
        except (TypeError, ValueError):
            raise ArgumentTypeError(f'{self.name} must be a valid integer; {value} is not')


class FloatArgMixin:
    """
    Makes sure that the value passed is a real number (floating-point).
    """
    def value_factory(self, value):
        """
        The raw value will be passed through this method.
        """
        try:
            return float(value)
        except (TypeError, ValueError):
            raise ArgumentTypeError(f'{self.name} must be a valid real number; {value} is not')


class MinMaxStrMixin:
    """
    Stores the minimum and maximum length of the string and compares against them in factory.
    """
    def __init__(self, minimum=None, maximum=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._minimum = minimum
        self._maximum = maximum

    def value_factory(self, value):
        """
        The raw value will be passed through this method.
        """
        value = str(value)
        if self._minimum:
            if len(value) < self._minimum:
                raise ArgumentTypeError(
                    f'{self.name} must be longer than {self._minimum} characters; {value} is not'
                )
        if self._maximum:
            if len(value) > self._maximum:
                raise ArgumentTypeError(
                    f'{self.name} must be shorter than {self._maximum} characters; {value} is not'
                )
        return value


class MinMaxMixin:
    """
    Stores the minimum and maximum values and compares against them in factory.

    Apply this on top of a numeric type like FloatArgMixin or IntArgMixin.
    """
    def __init__(self, minimum=None, maximum=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._minimum = minimum
        self._maximum = maximum

    def value_factory(self, value):
        """
        The raw value will be passed through this method.
        """
        value = super().value_factory(value)
        if self._minimum:
            if value < self._minimum:
                raise ArgumentTypeError(
                    f'{self.name} must be larger than {self.minimum}; {value} is not'
                )
        if self._maximum:
            if value > self._maximum:
                raise ArgumentTypeError(
                    f'{self.name} must be smaller than {self.minimum}; {value} is not'
                )
        return value
