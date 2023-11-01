"""
    Test class TestExtractedDataValidation for validating extracted data against the schema.
"""
from faker import Faker
from src.models.validators import BQFieldstValidator

fake = Faker()


class TestExtractedDataValidation:
    """
    Test class for validating extracted data against the schema.

    This test class contains a single test method that
    validates the extracted data against the defined schema using
    the BQFieldstValidator class.
    It asserts that the validated data matches the original extracted data.

    Attributes:
        fake (Faker): An instance of the Faker class for generating fake data.

    """

    def test_extracted_data_validation(self):
        """
        Test case to validate the extracted data against the schema.

        It generates fake extracted data using the Faker library,
        validates the data against the BQFieldstValidator
        schema, and asserts that the validated data matches the original extracted data.

        Raises:
            AssertionError: If the validated data does not match the extracted data.

        """
        # Generate fake extracted data
        extracted_data = {
            "date": fake.date(),
            "email": fake.email(),
            "value": fake.pyfloat(),
            "event_id": fake.random_int(),
            "event_name": fake.word(),
            "zipcode": fake.zipcode(),
            "last_name": fake.last_name(),
            "first_name": fake.first_name(),
            "country": fake.country(),
            "fb_phone": fake.phone_number(),
            "fb_click_id": fake.random_element([None, fake.uuid4()]),
            "client_user_agent": fake.user_agent(),
            "client_ip_address": fake.ipv4(),
            "event_source_url": fake.url(),
        }

        # Validate the extracted data against the schema
        validated_data = BQFieldstValidator(**extracted_data)

        # Assert that the validated data matches the original extracted data
        assert validated_data.dict() == extracted_data
