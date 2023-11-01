"""
CredentialsParser class that parses validated secret data into a dictionary of credentials.
CredentialsValidator class for validating credentials.
SecretRetriever class for retrieving secrets from Google Cloud Secret Manager.
CredentialsManagerClient class for managing credentials retrieved from Google Secret Manager.
"""
import json
import google_crc32c
from google.cloud import secretmanager
from secret_env_client import GoogleSecretManagerClient


class SecretRetriever:
    """
    A class for retrieving secrets from Google Cloud Secret Manager.

    Attributes:
    -----------
    secret_data : bytes
        The secret data retrieved from the specified location.

    Methods:
    --------
    __init__(self, secret_location: str)
        Initializes a new instance of the SecretRetriever class.

        Parameters:
        -----------
        secret_location : str
            The resource name of the secret version to access, in the format:
            `projects/*/secrets/*/versions/*`.

    __retrieve_secret(secret_location: str) -> bytes
        Retrieves the secret data from the specified location using the
        Secret Manager service client.

        Parameters:
        -----------
        secret_location : str
            The resource name of the secret version to access, in the format:
            `projects/*/secrets/*/versions/*`.

        Returns:
        --------
        bytes
            The secret data retrieved from the specified location.
    """

    def __init__(self, secret_location: str):
        """
        Initializes a new instance of the SecretRetriever class.

        Parameters:
        -----------
        secret_location : str
            The resource name of the secret version to access, in the format:
            `projects/*/secrets/*/versions/*`.
        """
        self.secret_data = self.__retrieve_secret(secret_location)

    @staticmethod
    def __retrieve_secret(
        secret_location: str,
    ) -> secretmanager.AccessSecretVersionResponse:
        """
        Retrieves the secret data from the specified location using the
        Secret Manager service client.

        Parameters:
        -----------
        secret_location : str
            The resource name of the secret version to access, in the format:
            `projects/*/secrets/*/versions/*`.

        Returns:
        --------
        AccessSecretVersionResponse
            The secret data retrieved from the specified location.
        """
        # Create the Secret Manager client.
        client = secretmanager.SecretManagerServiceClient()
        return client.access_secret_version(request={"name": secret_location})


class CredentialsValidator:
    """
    A class for validating credentials.

    This class takes a payload containing credentials and validates them
    using a checksum. It raises a ValueError if the payload is corrupted.

    Attributes:
        validated_credentials (dict): A dictionary containing validated
            credentials.

    Methods:
        __init__(self, payload): Initializes a new CredentialsValidator instance
            with the given payload.
        __validate_credentials(payload): A private method that validates the
            given payload and returns the validated credentials dictionary.
    """

    def __init__(self, payload):
        """
        Initializes a new CredentialsValidator instance with the given payload.

        Args:
            payload (obj): The payload containing the credentials to validate.

        Returns:
            None.
        """
        self.validated_credentials = self.__validate_credentials(payload)

    @staticmethod
    def __validate_credentials(payload):
        """
        A private method that validates the given payload and returns the
        validated credentials dictionary.

        Args:
            payload (obj): The payload containing the credentials to validate.

        Returns:
            dict: A dictionary containing the validated credentials.

        Raises:
            ValueError: If the payload is corrupted.
        """
        # Verify payload checksum.
        crc32c = google_crc32c.Checksum()
        crc32c.update(payload.payload.data)
        if payload.payload.data_crc32c != int(crc32c.hexdigest(), 16):
            print(payload)
            raise ValueError("Data corruption detected.")
        return payload


class CredentialsParser:
    """
    A class that parses validated secret data into a dictionary of credentials.

    Attributes:
        parsed_secret_data (dict): A dictionary containing the parsed credentials.

    Methods:
        __init__(self, validated_secret_data):
            Initializes a new CredentialsParser instance with the provided validated secret data.
            This data should be in the form of a payload object,
            that has been validated for security purposes.
            The parsed credentials are stored in the 'parsed_secret_data' attribute.

        __parse_credentials(validated_secret_data):
            A static method that parses validated secret data,
            into a dictionary of credentials.
            The provided data should be a payload object,
            that has been validated for security purposes.
            This method returns a dictionary containing the parsed credentials.
    """

    def __init__(self, validated_secret_data):
        self.parsed_secret_data = self.__parse_credentials(validated_secret_data)

    @staticmethod
    def __parse_credentials(validated_secret_data):
        """
        A static method that parses validated secret data into a dictionary of credentials.

        Args:
            validated_secret_data (Payload):
            A payload object that, has been validated for security purposes.

        Returns:
            dict: A dictionary containing the parsed credentials.
        """
        return json.loads(
            str(validated_secret_data.payload.data.decode("utf-8")).replace("'", '"')
        )


class CredentialsManagerClient(GoogleSecretManagerClient):
    """
    A class for managing credentials retrieved from Google Secret Manager.

    Attributes:
    -----------
    _cached_credentials: None
        A class variable used to cache credentials.

    Methods:
    --------
    __init__(self)
        Initializes a new instance of the CredentialsManagerClient class.

    __load_payload(self)
        Private method that loads credentials from the secret location.

    credentials(self)
        A property that returns the parsed secret data from Google Secret Manager.
        If the payload is not yet loaded, the method first loads it using
        the __load_payload() method.

    """

    def __init__(self):
        """
        Initializes a new instance of the CredentialsManagerClient class.
        """
        super().__init__()

    def __load_payload(self):
        """
        Private method that loads credentials from the secret location.
        """
        secret_retriever = SecretRetriever(secret_location=super().secret_location)
        raw_secret_data = secret_retriever.secret_data
        validated_secret_data = CredentialsValidator(
            raw_secret_data
        ).validated_credentials
        return CredentialsParser(validated_secret_data).parsed_secret_data

    @property
    def credentials(self):
        """
        A property that returns the parsed secret data from Google Secret Manager.
        If the payload is not yet loaded, the method first loads it using
        the __load_payload() method.
        """
        return self.__load_payload()
