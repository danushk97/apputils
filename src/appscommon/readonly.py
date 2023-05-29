"""
This module holds the constants.
"""

class ReadOnlyMetaClass(type):
    def __setattr__(cls, key, value):
        """
        Ignoring assignment statement
        """

class ReadOnly(metaclass=ReadOnlyMetaClass):
    """
    Instance of ReadOnlyMetaClass
    """
