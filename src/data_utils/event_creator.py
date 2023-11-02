"""
EventCreator class for creating Event objects from input data.
"""
import logging
from bingads.v13.bulk.entities.bulk_offline_conversion import BulkOfflineConversion
from bingads import ServiceClient
from src.models.mapper import Mapper
from src.models.workers import DataMapperThreadedWorker
from src.data_utils.api import BingAdsApiVersion


class EventCreator(Mapper):
    """
    A class for creating Event objects from input data.

    Args:
        data (Dict[str, str]): The input data used for creating events.
    """

    def __init__(self, data, client, **kwargs):
        """
        Initialize the EventCreator instance.

        Args:
            data (Dict[str, str]): The input data used for creating events.
        """
        super().__init__()
        self.__data = data
        self._validate_data()
        self.__client = client
        self.__kwargs = kwargs
        self.__version = BingAdsApiVersion().version
        self.__enviorment = "production"
        self.__service = "CampaignManagementService"
        self.__bulk_service = "BulkService"

    @property
    def client(self):
        return ServiceClient(
            service=self.__service,
            version=self.__version,
            authorization_data=self.__client,
            environment=self.__enviorment,
        )

    @property
    def bulk_client(self):
        return ServiceClient(
            service=self.__bulk_service,
            version=self.__version,
            authorization_data=self.__client,
            environment=self.__enviorment,
        )

    @property
    def __auth_data(self):
        return self.__client

    def map_data(self):
        """
        Map the input data to Event objects.

        Returns:
            List[Event]: The mapped Event objects.
        """
        return DataMapperThreadedWorker(
            task_func=self.__mapper, data_to_process=self.__data
        ).run_threaded_tasks()

    def __mapper(self, data):
        """
        Map the input data to an Event object.

        Returns:
            Event: The mapped Event object.

        Raises:
            ValueError: If the required data is missing or invalid.
        """
        try:
            logging.info("Received data: %s. Creating events.", data)
            bulk_offline_conversion = BulkOfflineConversion()
            offline_conversion = self.client.factory.create("OfflineConversion")
            # If you do not specify an offline conversion currency code,
            # then the 'CurrencyCode' element of the goal's 'ConversionGoalRevenue' is used.
            offline_conversion.ConversionCurrencyCode = data["currency"]
            # The conversion name must match the 'Name' of the 'OfflineConversionGoal'.
            # If it does not match you won't observe any error, although the offline
            # conversion will not be counted.
            offline_conversion.ConversionName = data["conversion_name"]
            # The date and time must be in UTC, should align to the date and time of the
            # recorded click (MicrosoftClickId), and cannot be in the future.
            offline_conversion.ConversionTime = data["conversion_time"]
            # If you do not specify an offline conversion value,
            # then the 'Value' element of the goal's 'ConversionGoalRevenue' is used.
            offline_conversion.ConversionValue = data["value"]
            offline_conversion.MicrosoftClickId = data["click_id"]
            bulk_offline_conversion.offline_conversion = offline_conversion

            # response = self.bulk_client.UploadEntityRecords(
            #     AccountId=self.__auth_data.customer_id,
            #     EntityRecords=[bulk_offline_conversion],
            #     ResponseMode="ErrorsAndResults",
            # )

            logging.info("Sending conversion data: %s", offline_conversion)
            return bulk_offline_conversion

        except Exception as error:
            logging.exception("An error occurred while creating events: %s", str(error))
            raise ValueError(f"Error in creating events: {str(error)}") from error

    def _validate_data(self) -> None:
        """
        Validate the input data.

        Args:
            data (Dict[str, str]): The input data to validate.

        Raises:
            ValueError: If the input data is not a dictionary.
        """
        if not isinstance(self.__data, list):
            raise ValueError("Input data must be a dictionary.")

    def _log_mapping_completion(self) -> None:
        """
        Log the completion of the mapping process.
        """
        logging.info("Mapping process completed.")
