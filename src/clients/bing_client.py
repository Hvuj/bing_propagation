"""
BGClient class for handling Bing client authentication using credentials.
"""
from typing import Dict, Any
from bingads import AuthorizationData, OAuthAuthorization, OAuthWebAuthCodeGrant
from bingads.exceptions import OAuthTokenRequestException, TimeoutException
from src.clients.secrets_manager_client import CredentialsManagerClient


class BGClient(CredentialsManagerClient):
    """
    BGClient class handles Bing client authentication using credentials.

    It inherits from the CredentialsManagerClient class and provides methods to authenticate
    a client using the BingAdsApi and retrieve account information.
    """

    def __init__(self, project: str):
        """
        Initialize the BGClient instance with the project ID.

        Args:
            project: The project ID associated with the Bing client.
        """
        super().__init__()
        self.__project_id = project
        self.__account_id = self._get_account_id(project)
        self.__config_dict = self.__get_config_data()
        self.__developer_token = self.__get_developer_token(project)
        self.__client_id = self.__get_client_id(project)
        self.__client_secret = self.__get_client_secret(project)
        self.__refresh_token = self.__get_refresh_token(project)
        self.__customer_id = self.__get_customer_id(project)
        self.__redirect_uri = self.__get_redirect_uri(project)

    @property
    def project(self) -> str:
        """
        Get the project ID associated with the Bing client.

        Returns:
            The project ID.
        """
        return self.__project_id

    @property
    def account_id(self) -> str:
        """
        Get the Account ID associated with the Bing client.

        Returns:
            The Account ID.
        """
        return self.__account_id

    @property
    def config_dict(self) -> str:
        """
        Get the config dict associated with the Bing client.

        Returns:
            The Config Dict.
        """
        return self.__config_dict

    @property
    def developer_token(self) -> str:
        """
        Get the Developer Token associated with the Bing client.

        Returns:
            The Developer Token.
        """
        return self.__developer_token

    @property
    def client_id(self) -> str:
        """
        Get the Client ID associated with the Bing client.

        Returns:
            The Client ID.
        """
        return self.__client_id

    @property
    def client_secret(self) -> str:
        """
        Get the Client Secret associated with the Bing client.

        Returns:
            The Client Secret.
        """
        return self.__client_secret

    @property
    def refresh_token(self) -> str:
        """
        Get the Rrefresh Token associated with the Bing client.

        Returns:
            The Rrefresh Token.
        """
        return self.__refresh_token

    @property
    def customer_id(self) -> str:
        """
        Get the customer ID associated with the Bing client.

        Returns:
            The customer ID.
        """
        return self.__customer_id

    @property
    def redirect_uri(self) -> str:
        """
        Get the Redirect URI associated with the Bing client.

        Returns:
            The Redirect URI.
        """
        return self.__redirect_uri

    def auth_client(self) -> None:
        """
        Authenticate the Bing client using the provided credentials.

        Raises:
            ValueError: If the required credentials are missing or invalid.
            Exception: If there is an error initializing the BingAdsApi.
        """
        if not self.config_dict or not self.customer_id:
            raise ValueError(
                "Customer ID and/or Credentials are required for authentication."
            )

        try:
            oauth_web_auth_code_grant = OAuthWebAuthCodeGrant(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirection_uri=self.redirect_uri,
            )
            oauth_tokens = (
                oauth_web_auth_code_grant.request_oauth_tokens_by_refresh_token(
                    self.refresh_token
                )
            )

            return AuthorizationData(
                developer_token=self.developer_token,
                customer_id=self.customer_id,
                account_id=self.account_id,
                authentication=OAuthAuthorization(
                    client_id=oauth_web_auth_code_grant.client_id,
                    oauth_tokens=oauth_tokens,
                ),
            )

        except (OAuthTokenRequestException, TimeoutException) as ex:
            print(
                "You need to provide consent for the application to access your Bing Ads accounts. "
                "After you have granted consent in the web browser for the application to access your Bing Ads accounts, "
                "please enter the response URI that includes the authorization 'code' parameter: \n"
            )
            raise ex

    def _get_account_id(self, project: str) -> Dict[str, Any]:
        """
        Retrieve the credentials associated with the specified project.

        Args:
            project: The project ID associated with the Bing client.

        Returns:
            The credentials for the specified project.

        Raises:
            ValueError: If the specified project ID is not found.
        """
        if credentials := self.credentials["project_id"][project]["account_id"]:
            return credentials
        else:
            raise ValueError(f"Credentials not found for project: {project}")

    def __get_developer_token(self, project: str) -> Dict[str, Any]:
        """
        Retrieve the credentials associated with the specified project.

        Args:
            project: The project ID associated with the Bing client.

        Returns:
            The credentials for the specified project.

        Raises:
            KeyError: If the specified project ID is not found.
        """
        try:
            print()
            if developer_token := self.config_dict["developer_token"]:
                return developer_token
        except KeyError as error:
            raise KeyError(
                f"developer_token not found for project: {project}"
            ) from error

    def __get_client_id(self, project: str) -> Dict[str, Any]:
        """
        Retrieve the credentials associated with the specified project.

        Args:
            project: The project ID associated with the Bing client.

        Returns:
            The credentials for the specified project.

        Raises:
            KeyError: If the specified project ID is not found.
        """
        try:
            if client_id := self.config_dict["client_id"]:
                return client_id
        except KeyError as error:
            raise KeyError(f"client_id not found for project: {project}") from error

    def __get_client_secret(self, project: str) -> Dict[str, Any]:
        """
        Retrieve the credentials associated with the specified project.

        Args:
            project: The project ID associated with the Bing client.

        Returns:
            The credentials for the specified project.

        Raises:
            KeyError: If the specified project ID is not found.
        """
        try:
            if client_secret := self.config_dict["client_secret"]:
                return client_secret
        except KeyError as error:
            raise KeyError(f"client_secret not found for project: {project}") from error

    def __get_refresh_token(self, project: str) -> Dict[str, Any]:
        """
        Retrieve the credentials associated with the specified project.

        Args:
            project: The project ID associated with the Bing client.

        Returns:
            The credentials for the specified project.

        Raises:
            KeyError: If the specified project ID is not found.
        """
        try:
            if refresh_token := self.config_dict["refresh_token"]:
                return refresh_token
        except KeyError as error:
            raise KeyError(f"refresh_token not found for project: {project}") from error

    def __get_customer_id(self, project: str) -> Dict[str, Any]:
        """
        Retrieve the credentials associated with the specified project.

        Args:
            project: The project ID associated with the Bing client.

        Returns:
            The credentials for the specified project.

        Raises:
            KeyError: If the specified project ID is not found.
        """
        try:
            if customer_id := self.config_dict["customer_id"]:
                return customer_id
        except KeyError as error:
            raise KeyError(f"customer_id not found for project: {project}") from error

    def __get_redirect_uri(self, project: str) -> Dict[str, Any]:
        """
        Retrieve the credentials associated with the specified project.

        Args:
            project: The project ID associated with the Bing client.

        Returns:
            The credentials for the specified project.

        Raises:
            KeyError: If the specified project ID is not found.
        """
        try:
            if redirect_uri := self.config_dict["redirect_uri"]:
                return redirect_uri
        except KeyError as error:
            raise KeyError(f"redirect_uri not found for project: {project}") from error

    def __get_config_data(self) -> Dict[str, Any]:
        """
        Retrieve the credentials associated with the specified project.

        Args:
            project: The project ID associated with the Bing client.

        Returns:
            The credentials for the specified project.

        Raises:
            ValueError: If the specified project ID is not found.
        """
        return self.credentials["credentials"]
