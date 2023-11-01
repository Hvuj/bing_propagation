"""
BingAdsApiVersion class Encapsulates sdk __version__
"""
import os


class BingAdsApiVersion(object):

    """
    Encapsulates sdk __version__.
    Attributes:
        SDK_VERSION (class): indicating sdk version.
    """

    def __init__(self):
        """Initializes the api instance."""

    @property
    def version(self):
        return self.__get_version()

    @staticmethod
    def __get_version():
        """
        Retrieves the version number from the '__init__.py' file in the current directory.

        Returns:
            str: The version number extracted from the '__init__.py' file.

        Raises:
            ValueError: If the version information cannot be found in the file.
        """

        this_dir = os.path.dirname(os.path.abspath(__file__))
        package_init_filename = os.path.join(this_dir, "__init__.py")

        if os.path.exists(package_init_filename):
            version = None
            with open(package_init_filename, "r", encoding="UTF-8") as handle:
                file_content = handle.read()
                globals_dict = {}
                exec(file_content, globals_dict)
                version = globals_dict.get("__version__")

            if version:
                return version

        raise ValueError("Cannot find version information")
