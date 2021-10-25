import os
from typing import Dict, Callable, Any, List


class VariablesMixin:
    def __init__(self, variables: Dict[str, Callable] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.variables = variables if variables else {}

    def variable_value(self, name: str, default=None, raise_if_missing=None):
        """
        Retrieve the value of a variable.

        :param name: The name of the variable to retrieve.
        :param default: The value to return if the variable is not inside.
        :param raise_if_missing: The error to throw if the variable is not present;
            if None the default value will be returned (this can be KeyError).
        :return:
        """
        result = self.variables.get(name, None)
        if result is None:
            if raise_if_missing is None:
                return default
            else:
                raise raise_if_missing(f'No such variable: {name}')
        return result()

    def add_variables(self, variables: Dict[str, Callable]):
        """
        Add multiple variables.

        :param variables: A dictionary mapping names to functions that retrieve values.
        """
        for name, func in variables.items():
            self.variables[name] = func

    def add_variable(self, name: str, retriever: Callable):
        """
        Add a variable or replace previous definition.

        :param name: The name of the variable to add/change.
        :param retriever: The function to call to retrieve the value of this variable.
        """
        self.variables[name] = retriever

    def rem_variable(self, name: str):
        """
        Remove a variable from the internal list.

        :param name: The name of the variable to remove
        """
        del self.variables[name]

    def values(self) -> Dict[str, Any]:
        """
        Retrieves the values of all variables as a dictionary.
        """
        result = {}
        for name in self.variables:
            result[name] = self.variables[name]()
        return result

    def clear_variables(self):
        """
        Remove all variables.
        """
        self.variables = {}

    def get(self, name: str, default: Any = None) -> Any:
        """ Return the value for key if key is in the dictionary, else default. """
        result = self.variables.get(name, None)
        if result is None:
            return default
        return result()

    def items_list(self):
        """ A set-like object providing a view on D's items """
        result = []
        for name in self.variables:
            result.append((name, self.variables[name]()))
        return result

    def items(self):
        """ A set-like object providing a view on D's items """
        for name in self.variables:
            yield name, self.variables[name]()

    def keys(self) -> List[str]:
        """ D.keys() -> a set-like object providing a view on D's keys """
        return [name for name in self.variables]

    def __contains__(self, name: str):
        """ Tell if a certain variable is inside. """
        return name in self.variables

    def __delitem__(self, name: str):
        """
        Remove a variable from the internal list.

        :param name: The name of the variable to remove
        """
        del self.variables[name]

    def __getitem__(self, name: str) -> Any:
        """
        Retrieve a value by the name of the variable. Raise if not found.
        :param name: The variable's name.
        :return:
        """
        result = self.variables.get(name, None)
        if result is None:
            raise KeyError(f'No variable named {name}')
        return result()

    def __len__(self) -> int:
        """
        The number of variables inside.
        """
        return len(self.variables)

    def replace_in_string(self, format_string: str, raise_if_missing=False):
        """
        Returns a string where {key} occurrences are replaced by self[key].

        Please note that the algorithm is not efficient when it comes
        to missing keys.

        :param format_string: The string to format.
        :param raise_if_missing: Should we raise an error when the key is missing?
        :return: The format_string with variables replaced.
        """
        values = self.values()
        if raise_if_missing:
            return format_string.format_map(values)
        else:
            while True:
                try:
                    return format_string.format_map(values)
                except KeyError as exc:
                    values[str(exc)[1:-1]] = ''


def add_cd_variable(inst: VariablesMixin):
    """
    Adds a variable called cd that returns the path of current working directory.
    """
    inst.add_variable('cd', os.getcwd)


def add_cdn_variable(inst: VariablesMixin):
    """
    Adds a variable called cd that returns the name of current working directory.
    """
    inst.add_variable('cdn', lambda: os.path.basename(os.getcwd()))
