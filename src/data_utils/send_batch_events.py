"""
SendBatchEvents class for sending data to Facebook.
"""
import logging
from typing import List, Mapping, Final
from bingads.v13.bulk.bulk_service_manager import BulkServiceManager
from bingads.v13.bulk import *
from src.models.workers import EventMapperThreadedWorker
from src.data_utils.event_creator import EventCreator


class SendBatchEvents:
    """Class for sending batch events."""

    def __init__(self, data_to_send: List[Mapping[List, str]]):
        self.__data_to_send = data_to_send
        self.__file_directory = "/tmp"
        self.__download_file_name = "download.csv"
        self.__upload_file_name = "upload.csv"
        self.__result_file_name = "result.csv"
        self.__file_type = "csv"
        self.__time_out_in_seconds = 3600000

    def send_batch_events(self, **kwargs):
        """
        Send batch events.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            List[EventRequestAsync]: List of event responses.

        Raises:
            ValueError: If `data_to_send` is empty.
            KeyError: If `customer_id` is not provided in kwargs.
            KeyError: If `client` is not provided in kwargs.
            Exception: If an error occurs during the event processing.
        """
        return EventMapperThreadedWorker(
            task_func=self.__send_events, data_to_process=self.__data_to_send, **kwargs
        ).run_threaded_tasks()

    def __send_events(self, data, **kwargs) -> List[Mapping]:
        """
        Send batch events asynchronously.

        Args:
            data (List[Mapping[List, str]]): List of data to send.
            kwargs: Additional keyword arguments.

        Returns:
            List: List of event responses.

        Raises:
            ValueError: If `data` is empty.
            KeyError: If `client` is not provided in kwargs.
            Exception: If an error occurs during the event processing.
        """
        if not data:
            raise ValueError("Data to send is empty.")
        logging.info("Received data: %s. Sending conversions", data)

        client = kwargs["client"]

        try:
            download_entities = self.write_entities_and_upload_file(
                bulk_service_manager=BulkServiceManager(client),
                upload_entities=data,
            )
            return download_entities
        except Exception as error:
            logging.error("Error occurred during event processing: %s", error)
            raise RuntimeError("Error occurred during event processing.") from error

    def write_entities_and_upload_file(self, bulk_service_manager, upload_entities):
        # Writes the specified entities to a local file and uploads the file. We could have uploaded directly
        # without writing to file. This example writes to file as an exercise so that you can view the structure
        # of the bulk records being uploaded as needed.
        # C:\Users\elisi\OneDrive\Desktop\work\bing_propagation\src\tmp
        writer = BulkFileWriter(
            os.path.join(
                os.path.relpath(self.__file_directory), self.__upload_file_name
            )
        )
        for entity in upload_entities:
            writer.write_entity(entity)
        writer.close()

        file_upload_parameters = FileUploadParameters(
            result_file_directory=os.path.relpath(self.__file_directory),
            compress_upload_file=True,
            result_file_name=os.path.relpath(self.__result_file_name),
            overwrite_result_file=True,
            upload_file_path=os.path.join(
                os.path.relpath(self.__file_directory), self.__upload_file_name
            ),
            rename_upload_file_to_match_request_id=False,
            response_mode="ErrorsAndResults",
        )

        bulk_file_path = bulk_service_manager.upload_file(file_upload_parameters)

        download_entities = []
        entities_generator = self.read_entities_from_bulk_file(
            file_path=bulk_file_path,
            result_file_type=ResultFileType.upload,
            file_type=self.__file_type,
        )
        for entity in entities_generator:
            download_entities.append(entity)

        return download_entities

    def read_entities_from_bulk_file(self, file_path, result_file_type, file_type):
        with BulkFileReader(
            file_path=file_path, result_file_type=result_file_type, file_type=file_type
        ) as reader:
            for entity in reader:
                yield entity
