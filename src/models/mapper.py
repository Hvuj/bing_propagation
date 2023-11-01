"""
Abstract class for mapping data based on key-value pairs.
"""
from abc import ABC, abstractmethod


class Mapper(ABC):
    """
    Abstract class for mapping data based on key-value pairs.
    """

    @abstractmethod
    def map_data(self):
        """
        Abstract method for mapping data.

        Returns:
            dict: Mapped data as a dictionary.

        Raises:
            KeyError: If a key specified in the mapping does not exist in the data.
        """
        pass

    @abstractmethod
    def _validate_data(self):
        """
        Abstract method to validate the input data.

        Args:
            data (dict): Input data.

        Raises:
            ValueError: If the data fails validation.
        """
        pass

    @abstractmethod
    def _log_mapping_completion(self):
        """
        Abstract method to log the completion of the mapping process.
        """
        pass
