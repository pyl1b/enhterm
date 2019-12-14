# -*- coding: utf-8 -*-
"""
Contains the definition of the Serializable class.
"""


class Serializable(object):
    """
    Defines the methods that need to be implemented by serializable classes.
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        super().__init__(*args, **kwargs)

    def encode(self):
        """
        Called when a class instance needs to be serialized.

        .. note:
           The `result` and `uuid` members should not be serialized
           in case of :class:`~Command`.
        """
        raise NotImplementedError

    def decode(self, raw_data):
        """
        Apply raw data to this instance.

        It is asserted that correct class has already been constructed
        and that it has `result` and `uuid` members set in case of
        :class:`~Command`..

        Raises:
            DecodeError:
                The implementation should raise this class or a
                subclass of it.

        Arguments:
            raw_data (bytes):
                The data to apply.
        """
        raise NotImplementedError

    @classmethod
    def class_id(cls):
        """
        A unique identifier of the class.

        This value is used as a key when a constructor needs to
        be associated with a string
        (see :class:`enhterm.ser_deser.dsds.DictSerDeSer`).
        """
        return f"{cls.__module__}.{cls.__name__}"
