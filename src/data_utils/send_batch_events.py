"""
SendBatchEvents class for sending data to Facebook.
"""
import logging
from typing import List, Mapping, Final, Tuple
from src.models.workers import EventMapperThreadedWorker
from src.data_utils.event_creator import EventCreator


class SendBatchEvents:
    """Class for sending batch events."""

    def __init__(self, data_to_send: List[Mapping[List, str]]):
        self.__data_to_send = data_to_send

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
        customer_id = kwargs["customer_id"]

        try:
            i = 0
            # while we have not accepted clicks it will continue to try until success
            while True:
                conversion_upload_service = client.get_service(
                    "ConversionUploadService"
                )
                request = client.get_type("UploadClickConversionsRequest")
                request.customer_id = customer_id
                request.conversions = data
                request.partial_failure = True
                conversion_upload_response = (
                    conversion_upload_service.upload_click_conversions(request=request)
                )
                # list of accepted clicks
                clicks: Final[List[str]] = [
                    str(click.gclid)
                    for click in conversion_upload_response.results
                    if click.gclid
                ]

                attempted_clicks = self.__map_not_accepted_clicks(
                    data=data, clicks=clicks
                )

                clicks_to_send_again, partial_errors_list = self.__prase_faliures(
                    client=client,
                    attempted_clicks=attempted_clicks,
                    conversion_upload_response=conversion_upload_response,
                )

                # if length is equal then all clicks were accepted today and / or before
                if len(attempted_clicks) == len(data) and not clicks_to_send_again:
                    return {
                        "partial_errors_list": partial_errors_list,
                        "conversion_upload_response_results": conversion_upload_response.results,
                    }

                data = EventCreator(
                    data=clicks_to_send_again,
                    client=client,
                    customer_id=customer_id,
                    retry=True,
                ).map_data()

                clicks_to_send_again.clear()
                i += 1
                if i == 50:
                    print(f"Retrying...{i}")

                    return {
                        "partial_errors_list": partial_errors_list,
                        "conversion_upload_response_results": conversion_upload_response.results,
                    }
        except Exception as error:
            logging.error("Error occurred during event processing: %s", error)
            raise RuntimeError("Error occurred during event processing.") from error

    def __is_partial_failure_error_present(self, response) -> bool:
        """Checks whether a response message has a partial failure error.

        In Python the partial_failure_error attr is always present on a response
        message and is represented by a google.rpc.Status message. So we can't
        simply check whether the field is present, we must check that the code is
        non-zero. Error codes are represented by the google.rpc.Code proto Enum:
        https://github.com/googleapis/googleapis/blob/master/google/rpc/code.proto

        Args:
            response:  A MutateResponse message instance.

        Returns: A boolean, whether or not the response message has a partial
            failure error.
        """
        partial_failure = getattr(response, "partial_failure_error", None)
        code = getattr(partial_failure, "code", None)
        return code != 0

    def __prase_faliures(
        self, client, attempted_clicks, conversion_upload_response
    ) -> Tuple[List[Mapping], List[Mapping]]:
        """
        Parse the failures in the conversion upload response.

        Args:
            client: The Google Ads client.
            attempted_clicks: The list of attempted clicks.
            conversion_upload_response: The conversion upload response.

        Returns:
            A tuple of (clicks_to_send_again, partial_errors_list).
            clicks_to_send_again is the list of clicks that failed with the error
            "conversion_date_time that precedes the click".
            partial_errors_list is the list of partial errors.
        """
        # list of partial errors
        partial_errors_list = []
        # list of clicks with error "conversion_date_time that precedes the click" to retry
        clicks_to_send_again = []

        # Check for existence of any partial failures in the response.
        if self.__is_partial_failure_error_present(conversion_upload_response):
            # Prints the details of the partial failure errors.
            partial_failure = getattr(
                conversion_upload_response, "partial_failure_error", None
            )

            # partial_failure_error.details is a repeated field and iterable
            error_details = getattr(partial_failure, "details", [])

            for error_detail in error_details:
                # Retrieve an instance of the GoogleAdsFailure class from the client
                failure_message = client.get_type("GoogleAdsFailure")
                # Parse the string into a GoogleAdsFailure message instance.
                # To access class-only methods on the message we retrieve its type.
                GoogleAdsFailure = type(failure_message)
                failure_object = GoogleAdsFailure.deserialize(error_detail.value)
                for error in failure_object.errors:
                    # Construct and print a string that details which element
                    # as well as the error message and error code.
                    if (
                        error.message
                        == "The imported event has a conversion_date_time that precedes the click. Make sure your conversion_date_time is correct and try again."
                    ):
                        clicks_to_send_again.append(
                            attempted_clicks[
                                int(error.location.field_path_elements[0].index)
                            ]
                        )

                    partial_errors_list.append(
                        {
                            "A partial failure at index": f"{int(error.location.field_path_elements[0].index)+1} occurred",
                            "Error message": error.message,
                            "Error code": error.error_code,
                        }
                    )
        return clicks_to_send_again, partial_errors_list

    def __map_not_accepted_clicks(self, data, clicks):
        """
        Map the clicks that are not accepted in the conversion upload request
        to a list of dictionaries.

        Args:
            data: The list of clicks.
            clicks: The list of accepted clicks.

        Returns:
            A list of dictionaries, where each dictionary represents a click
            that is not accepted.
        """
        attempted_clicks = []

        # Create a set of accepted click gclids for faster lookup
        accepted_click_gclids = set(clicks)

        for click in data:
            if click.gclid not in accepted_click_gclids:
                data_to_retry = {
                    "value": click.conversion_value,
                    "date": click.conversion_date_time,
                    "conversion_action_id": click.conversion_action.split("/")[3],
                    "click_id": click.gclid,
                    "gbraid": click.gbraid,
                    "wbraid": click.wbraid,
                    "currency": click.currency_code,
                    "order_id": click.order_id,
                    "email": None,
                    "phone": None,
                }

                for identifier in click.user_identifiers:
                    if identifier.hashed_email:
                        data_to_retry["email"] = identifier.hashed_email
                    else:
                        data_to_retry["phone"] = identifier.hashed_phone_number

                attempted_clicks.append(data_to_retry)

        return attempted_clicks
