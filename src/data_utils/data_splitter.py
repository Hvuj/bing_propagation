"""
DataSplitter class for splitting data into chunks.
"""
import logging
from typing import List, Any
from src.models.workers import DataSplitterThreadedWorker


class DataSplitter:
    """Class for splitting data into chunks."""

    def __init__(self, data_to_split: List[Any], num_of_splits: int = 2000):
        """
        Initialize the DataSplitter with input data and number of splits.

        Args:
            data_to_split (List[Any]): The data to split into chunks.
            num_of_splits (int, optional):
            The number of chunks to split the data into. Default is 2000.

        Raises:
            ValueError: If the input data is not a list.
            ValueError: If the number of chunks is less than or equal to 0.
        """
        self.__data_to_split = data_to_split
        self.__num_of_splits = num_of_splits
        self.__validate_input()

    @property
    def data_to_split(self) -> List[Any]:
        """Get the data to split."""
        return self.__data_to_split

    @property
    def num_of_splits(self) -> int:
        """Get the number of splits."""
        return self.__num_of_splits

    def split_data_into_chunks(self):
        """
        Split the data into specified number of chunks.

        Returns:
            List[List[Any]]: The chunks of data as a list of lists.

        Raises:
            ValueError: If there is no data to split.
        """
        return DataSplitterThreadedWorker(
            task_func=self.__split_data, data_to_process=self.__data_to_split
        ).run_threaded_tasks()

    def __split_data(self, data_to_split: List[Any]) -> List[List[Any]]:
        """
        Split the input data into specified number of chunks.

        Args:
            data_to_split (List[Any]): The data to split into chunks.

        Returns:
            List[List[Any]]: The chunks of data as a list of lists.

        Raises:
            ValueError: If there is no data to split.
        """
        list_of_chunks: List[List[Any]] = []
        try:
            logging.info("Received data: %s. Splitting data.", data_to_split)

            if hasattr(data_to_split, "__getitem__"):
                list_of_chunks.extend(
                    data_to_split[start_num : start_num + self.num_of_splits]
                    for start_num in range(0, len(data_to_split), self.num_of_splits)
                )
            else:
                list_of_chunks.extend(
                    self.data_to_split[start_num : start_num + self.num_of_splits]
                    for start_num in range(
                        0, len(self.data_to_split), self.num_of_splits
                    )
                )

            if not list_of_chunks:
                logging.warning("There is no data to split - please check input data")
                raise ValueError("There is no data to split - please check input data")

            logging.info("This is the data we chunked: %s", list_of_chunks)
            return list_of_chunks

        except Exception as split_data_into_chunks_error:
            logging.warning(split_data_into_chunks_error)
            raise split_data_into_chunks_error

    def __validate_input(self):
        """
        Validate the input data and number of splits.

        Raises:
            ValueError: If the input data is not a list.
            ValueError: If the number of chunks is less than or equal to 0.
        """
        if not isinstance(self.data_to_split, list):
            raise ValueError("Input data must be a list.")

        if self.num_of_splits <= 0:
            raise ValueError("Number of splits must be greater than 0.")
