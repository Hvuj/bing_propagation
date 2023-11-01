"""
BigQueryClient class for extracting data from BigQuery.
"""
import logging
from typing import List, Dict, Any
from google.cloud.bigquery.exceptions import BigQueryError
from google.cloud import bigquery
from src.models.validators import BQFieldstValidator


class EmptyTableException(Exception):
    pass


# bq client instead and bqauth put in this file
class BigQueryClient:
    """
    Extracts data from BigQuery.
    """

    def __init__(
        self, project_id: str = None, dataset_id: str = None, table_name: str = None
    ) -> None:
        """
        Initializes a new instance of the Extractor class.

        Args:
            project_id (str, optional): The ID of the Google Cloud project. Defaults to None.
        """
        self._project_id = project_id
        self._dataset_id = dataset_id
        self._table_name = table_name
        self._client = self.__bq_client()

    @property
    def project_id(self) -> str:
        """
        Get the project ID.

        Returns:
            str: The project ID.
        """
        return self._project_id

    @project_id.setter
    def project_id(self, value: str) -> None:
        """
        Set the project ID.

        Args:
            value (str): The project ID to set.
        """
        self._project_id = value

    @property
    def dataset_id(self):
        """
        Get the Dataset ID.

        Returns:
            str: The Dataset ID.
        """
        return self._dataset_id

    @dataset_id.setter
    def dataset_id(self, value):
        """
        Set the Dataset ID.

        Args:
            value (str): The Dataset ID to set.
        """
        self._dataset_id = value

    @property
    def table_name(self):
        """
        Get the Table Name.

        Returns:
            str: The Table Name.
        """
        return self._table_name

    @table_name.setter
    def table_name(self, value):
        """
        Set the Table Name.

        Args:
            value (str): The Table Name to set.
        """
        self._table_name = value

    @property
    def query(self) -> str:
        """
        Get the current query.

        Returns:
            str: The current query.
        """
        return f"select * from `{self.project_id}.{self.dataset_id}.{self.table_name}` order by conversion_time desc"

    def __bq_client(self) -> bigquery.Client:
        """
        Creates and returns a BigQuery client with authentication.

        Returns:
            google.cloud.bigquery.client.Client:
            A BigQuery client instance authenticated with the project ID.
        """
        try:
            return bigquery.Client(self.project_id)
        except Exception as bigquery_auth_error:
            # Handle any exceptions that might occur during client creation
            raise BigQueryError(
                f"Failed to create BigQuery client: {str(bigquery_auth_error)}"
            ) from bigquery_auth_error

    def extract_data(self) -> List[Dict[str, Any]]:
        """
        Extracts data from BigQuery and returns the results as a list of rows.

        Returns:
            List[Dict[str, Any]]: The results of the query as a list of rows.

        Raises:
            BigQueryError: If there is an error executing the query or if the query returns no data.
        """
        try:
            query_job = self._client.query(self.query)
            logging.info("Data extracted from BigQuery successfully")
            results = query_job.result()

            if results.total_rows == 0:
                error_msg = "The query returned no data"
                logging.error(error_msg)
                raise EmptyTableException("No data found in the table.")

            data = [dict(row.items()) for row in results]
            BQFieldstValidator(**data[0])
            return data

        except BigQueryError as error:
            error_msg = "An error occurred while extracting data from BigQuery"
            logging.exception(error_msg)
            raise BigQueryError(error_msg) from error
