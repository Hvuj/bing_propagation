"""
SecretEnvLoader class that loads environment variables from a `.env` file
GoogleSecretManagerClient class for loading secrets from Google Secret Manager.
"""
import os
from pathlib import Path
from dotenv import load_dotenv


class SecretEnvLoader:
    """
    A class that loads environment variables from a `.env` file
    and provides getters and setters for `PROJECT_ID`
    and `SECRET_ID` environment variables.

    Attributes:
    -----------
    project_id : str, optional
        The value to use for the `PROJECT_ID` environment variable.
        If not set explicitly, the value is read from the
        environment using `os.environ.get()`.
    secret_id : str, optional
        The value to use for the `SECRET_ID` environment variable.
        If not set explicitly, the value is read from the
        environment using `os.environ.get()`.

    Methods:
    --------
    __init__():
        Initializes a new instance of the `SecretEnvLoader` class.
        Loads environment variables from a `.env` file
        using the `__load_env_variables()` method.

    __load_env_variables():
        Loads environment variables from a `.env` file
        using the `load_dotenv()` function from the `python-dotenv`
        library.

    project_id():
        Getter method for the `project_id` attribute.
        Returns the value of the `project_id` attribute if it has been set
        explicitly using the `project_id` setter method.
        Otherwise, returns the value of the `PROJECT_ID` environment
        variable by calling `os.environ.get()`.

    project_id(value: str):
        Setter method for the `project_id` attribute.
        Sets the value of the `project_id` attribute to the specified
        value.

    secret_id():
        Getter method for the `secret_id` attribute.
        Returns the value of the `secret_id` attribute if it has been set
        explicitly using the `secret_id` setter method.
        Otherwise, returns the value of the `SECRET_ID` environment
        variable by calling `os.environ.get()`.

    secret_id(value: str):
        Setter method for the `secret_id` attribute.
        Sets the value of the `secret_id` attribute to the specified value.
    """

    def __init__(self):
        """
        Initializes a new object of the class with project_id and secret_id set to None.
        Calls __load_env_variables() method to load environment variable.
        required for authentication.
        """
        self.__project_id = None
        self.__secret_id = None
        self.__load_env_variables()

    @staticmethod
    def __load_env_variables():
        """
        A static method that loads the environment variables required for authentication.
        If the .env file is not found in the directory, it raises a FileNotFoundError.
        """
        try:
            env_path = Path(__file__).resolve().parents[2] / ".env"
            load_dotenv(dotenv_path=env_path, override=True)
        except FileNotFoundError as file_not_found:
            print("Could not find .env file")
            raise file_not_found

    @property
    def project_id(self):
        """
        A property method that returns the project_id.
        If project_id is not set, it returns the value of the PROJECT_ID environment variable.
        """
        if self.__project_id is not None:
            return self.__project_id
        return os.environ.get("PROJECT_ID")

    @project_id.setter
    def project_id(self, value):
        """
        A property method that sets the value of project_id.
        """
        self.__project_id = value

    @property
    def secret_id(self):
        """
        A property method that returns the secret_id.
        If secret_id is not set, it returns the value of the SECRET_ID environment variable.
        """
        if self.__secret_id is not None:
            return self.__secret_id
        return os.environ.get("SECRET_ID")

    @secret_id.setter
    def secret_id(self, value):
        """
        A property method that sets the value of secret_id.
        """
        self.__secret_id = value


if __name__ == "__main__":
    print(Path(__file__).resolve().parents[2] / ".env")


class GoogleSecretManagerClient(SecretEnvLoader):
    """
    A class for loading secrets from Google Secret Manager.

    Attributes:
    -----------
    secret_location : str
        The location of the secret in Google Secret Manager.

    Methods:
    --------
    __init__():
        Initializes a new instance of the GoogleSecretManagerClient class
        with secret_location set to None.
        Calls the constructor of the base class.

    secret_location():
        Returns the location of the secret in Google Secret Manager.

        Returns:
        --------
        str:
            The secret location in Google Secret Manager.
    """

    def __init__(self):
        """
        Initializes a new instance of the GoogleSecretManagerClient class.
        """
        super().__init__()
        self.__project_id = self.project_id
        self.__secret_id = self.secret_id

    @property
    def secret_location(self) -> str:
        """
        Returns the secret location in Google Secret Manager.

        Returns:
        --------
        str:
            The secret location in Google Secret Manager.
        """
        return (
            f"projects/{self.__project_id}/secrets/{self.__secret_id}/versions/latest"
        )

    @secret_location.setter
    def secret_location(self, value):
        """
        Set the secret_location property to a new value.

        This method raises an AttributeError,
        because the secret_location property is not accessible.

        Parameters:
        -----------
        value : str
            The new value for the secret_location property.

        Raises:
        -------
        AttributeError:
            Always raised, because the secret_location property is not accessible.
        """
        print(f"Current Value is: {value}")
        raise AttributeError("This property is not accessible")
