"""
DataMop - Custom Exceptions

Centralized exception classes used throughout DataMop.
"""


class DataMopError(Exception):
    """
    Base exception for all DataMop errors.
    """

    pass


class DataMopInputError(DataMopError):
    """
    Raised when user input is invalid.
    """

    pass


class DataMopFileError(DataMopError):
    """
    Raised when a dataset file cannot be loaded.
    """

    pass


class DataMopDataError(DataMopError):
    """
    Raised when the dataset itself is invalid.
    """

    pass


class DataMopConfigurationError(DataMopError):
    """
    Raised when DataMop configuration is invalid.
    """

    pass