"""
Abstract ThreadedWorkers class handles running tasks concurrently using threads.
"""
import logging
import time
import concurrent.futures as cf
from abc import ABC, abstractmethod
from typing import Callable, List, Any


class ThreadedWorkers(ABC):
    """
    ThreadedWorkers class handles running tasks concurrently using threads.
    """

    @abstractmethod
    def run_threaded_tasks(self) -> List[Any]:
        """
        Abstract method to define the execution of threaded tasks.

        Returns:
            A list of results from the threaded tasks.
        """
        pass

    @abstractmethod
    def log_completion(self):
        """
        Abstract method to log the completion of a process.
        """
        pass


class DataSplitterThreadedWorker(ThreadedWorkers):
    """
    DataSplitterThreadedWorker class handles running tasks concurrently using threads.
    """

    def __init__(self, task_func: Callable, data_to_process):
        super().__init__()
        self._data_to_process = data_to_process
        self._task_func = task_func

    def run_threaded_tasks(self) -> List[Any]:
        """
        Run threaded tasks concurrently using a thread pool executor.

        Returns:
            List[Any]: List of results from the executed tasks.

        Raises:
            RuntimeError: If an error occurs during task execution.
        """
        start_time: float = time.perf_counter()
        try:
            logging.info(
                "Received data: %s. Running threaded tasks.", self._data_to_process
            )
            with cf.ThreadPoolExecutor() as executor:
                logging.info(
                    "Received data: %s. Running function: %s.",
                    self._data_to_process,
                    self._task_func,
                )
                result_future: cf.Future = executor.submit(
                    self._task_func, self._data_to_process
                )

            end_time: float = time.perf_counter()
            print(
                f"Done tasks, took {round(end_time - start_time, 2)} second(s) to finish."
            )

            return result_future.result()

        except Exception as error:
            print(error)
            logging.warning("An error occurred: %s", error)
            raise RuntimeError(f"Some error: {error}") from error

    def log_completion(self):
        """
        Abstract method to log the completion of a process.
        """
        pass


class DataMapperThreadedWorker(ThreadedWorkers):
    """
    DataMapperThreadedWorker class handles running tasks concurrently using threads.
    """

    def __init__(self, task_func: Callable, data_to_process):
        super().__init__()
        self._data_to_process = data_to_process
        self._task_func = task_func

    def run_threaded_tasks(self) -> List[Any]:
        """
        Run threaded tasks concurrently using a thread pool executor.

        Returns:
            List[Any]: List of results from the executed tasks.

        Raises:
            RuntimeError: If an error occurs during task execution.
        """
        start_time: float = time.perf_counter()
        try:
            logging.info(
                "Received data: %s. Running threaded tasks.", self._data_to_process
            )
            with cf.ThreadPoolExecutor() as executor:
                logging.info(
                    "Received data: %s. Running function: %s.",
                    self._data_to_process,
                    self._task_func,
                )
                result_futures: List[cf.Future] = [
                    executor.submit(self._task_func, data)
                    for data in self._data_to_process
                ]

            end_time: float = time.perf_counter()
            print(
                f"Done tasks, took {round(end_time - start_time, 2)} second(s) to finish."
            )

            return [f.result() for f in cf.as_completed(result_futures)]

        except Exception as error:
            print(error)
            logging.warning("An error occurred: %s", error)
            raise RuntimeError(f"Some error: {error}") from error

    def log_completion(self):
        """
        Abstract method to log the completion of a process.
        """
        pass


class EventMapperThreadedWorker(ThreadedWorkers):
    """
    EventMapperThreadedWorker class handles running tasks concurrently using threads.
    """

    def __init__(self, task_func: Callable, data_to_process, **kwargs):
        super().__init__()
        self._data_to_process = data_to_process
        self._task_func = task_func
        self._kwargs = kwargs

    def run_threaded_tasks(self) -> List[Any]:
        """
        Run threaded tasks concurrently using a thread pool executor.

        Returns:
            List[Any]: List of results from the executed tasks.

        Raises:
            RuntimeError: If an error occurs during task execution.
        """
        start_time: float = time.perf_counter()
        try:
            logging.info(
                "Received data: %s. Running threaded tasks.", self._data_to_process
            )
            with cf.ThreadPoolExecutor() as executor:
                logging.info(
                    "Received data: %s. Running function: %s.",
                    self._data_to_process,
                    self._task_func,
                )
                result_futures: List[cf.Future] = [
                    executor.submit(self._task_func, data, **self._kwargs)
                    for data in self._data_to_process
                ]

            end_time: float = time.perf_counter()
            print(
                f"Done tasks, took {round(end_time - start_time, 2)} second(s) to finish."
            )

            return [f.result() for f in cf.as_completed(result_futures)]

        except Exception as error:
            print(error)
            logging.warning("An error occurred: %s", error)
            raise RuntimeError(f"Some error: {error}") from error

    def log_completion(self):
        """
        Abstract method to log the completion of a process.
        """
        pass
