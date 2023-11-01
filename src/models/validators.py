"""
DataValidator class for validating data from BigQuery.
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class BQFieldstValidator(BaseModel):
    """
    Represents an event.

    Attributes:
        conversion_time (datetime): The conversion_time of the event.
        transaction_id (int): The Transaction ID of the event.
        email (str): The email associated with the event.
        phone (str): The phone number associated with the event.
        conversion_name (str): The ID of the event.
        currency (str): The currency of the value of the event.
        click_id (str): The click ID associated with the event.
        value (float): The value of the event.

    """

    conversion_time: datetime
    transaction_id: int
    email: str
    phone: str
    conversion_name: str
    currency: str
    click_id: Optional[str] = None
    value: float


class ServiceValidator(BaseModel):
    """
    A data validator for the Service class.

    Args:
        project_id (str): The ID of the project.
        dataset_id (str): The ID of the dataset.
        table_name (str): The name of the table.

    Attributes:
        project_id (str): The ID of the project.
        dataset_id (str): The ID of the dataset.
        table_name (str): The name of the table.
    """

    project_id: str
    dataset_id: str
    table_name: str
