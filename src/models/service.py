"""
Service class for data extraction, transformation, and loading to Facebook.
"""
import logging
from functools import lru_cache
from src.clients.bigquery_client import BigQueryClient
from src.data_utils.data_splitter import DataSplitter
from src.clients.bing_client import BGClient
from src.data_utils.send_batch_events import SendBatchEvents
from src.data_utils.event_creator import EventCreator
from src.models.validators import ServiceValidator


class Service:
    """
    Service class for data extraction, transformation, and loading to Facebook.

    This class provides a simplified interface to
    extract data, transform it and load it to Facebook
    using various components from the `src` module.

    Args:
        project_id (str): The project ID for the Extractor.
        query (str): The query to run for data extraction.
    """

    def __init__(
        self, project_id: str = None, dataset_id: str = None, table_name: str = None
    ):
        """
        Service class for data extraction, transformation, and loading to Facebook.

        Args:
            project_id (str): The project ID for the Extractor.
            query (str): The query to run for data extraction.
        """
        ServiceValidator(
            project_id=project_id, dataset_id=dataset_id, table_name=table_name
        )
        logging.basicConfig(level=logging.ERROR)
        self.__project_id = project_id
        self.__dataset_id = dataset_id
        self.__table_name = table_name
        self.extractor = BigQueryClient(
            project_id=self.__project_id,
            dataset_id=self.__dataset_id,
            table_name=self.__table_name,
        )

    @property
    def client(self):
        return self.__authenticated_client()

    @lru_cache(maxsize=1)
    def __client(self):
        return BGClient(project=self.extractor.project_id)

    def read_data(self):
        """
        Reads data from the data source based on the specified query.

        Returns:
            data: The extracted data.
        """
        return self.extractor.extract_data()

    @lru_cache(maxsize=1)
    def __authenticated_client(self):
        return self.__client().auth_client()

    def transform_data(self, data):
        """
        Transforms the given data by mapping and creating events.

        Args:
            data: The data to be transformed.

        Returns:
            splitted_data: The transformed and split data.
        """

        events = EventCreator(data=data, client=self.client).map_data()
        return DataSplitter(
            data_to_split=events, num_of_splits=2000
        ).split_data_into_chunks()

    def load_data(self, splitted_data):
        """
        Loads the splitted data to Facebook using the authenticated client.

        Args:
            splitted_data: The splitted data to be loaded.

        Returns:
            loader: The result of the data loading process.
        """
        return SendBatchEvents(data_to_send=splitted_data).send_batch_events(
            client=self.client
        )
