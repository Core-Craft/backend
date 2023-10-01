import os

from dotenv import load_dotenv

from app.db.base import DataBase


class User:
    """
    Represents a user data management utility.

    This class provides methods for interacting with a user-related database table. It loads database configuration from environment variables and utilizes the `DataBase` class for performing common database operations such as saving, retrieving, filtering, updating, and deleting user data.

    Attributes:
        - __db_url (str): The database connection URL obtained from the environment variables.
        - __db_name (str): The name of the database obtained from the environment variables.
        - __table_name (str): The name of the user table obtained from the environment variables.
        - __db (DataBase): An instance of the `DataBase` class for handling database operations.

    Methods:
        - save(data: dict): Inserts user data into the database table.
        - get(user_uuid: int): Retrieves user data by user UUID from the database table.
        - get_all(): Retrieves all user data from the database table.
        - filter(filter: dict): Retrieves user data based on a filter criteria from the database table.
        - update(data: dict): Updates user data in the database table.
        - delete(filter: dict): Deletes user data based on a filter criteria from the database table.

    Note:
        - The class initializes database-related attributes from environment variables loaded via `load_dotenv()`.
        - It relies on the `DataBase` class for executing database operations.
    """

    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        self.__db_url = os.environ.get("DB_URL")
        self.__db_name = os.environ.get("DB_NAME")
        self.__table_name = os.environ.get("USER_TABLE_NAME")
        self.__db = DataBase(db_url=self.__db_url)

    def save(self, data: dict):
        """
        Inserts user data into the database table.

        Args:
            data (dict): The user data to be saved.

        Returns:
            response: The response code from the database operation.
        """
        return self.__db.upload(
            db_name=self.__db_name, table_name=self.__table_name, data=data
        )

    def get(self, user_uuid: int):
        """
        Retrieves user data by user UUID from the database table.

        Args:
            user_uuid (int): The user UUID for identifying the user.

        Returns:
            response: The user data retrieved from the database.
        """
        return self.__db.query(
            db_name=self.__db_name,
            table_name=self.__table_name,
            filter={"user_uuid": user_uuid},
        )

    def get_all(self):
        """
        Retrieves all user data from the database table.

        Returns:
            response: A list of all user data retrieved from the database.
        """
        return list(
            self.__db.query(
                db_name=self.__db_name, table_name=self.__table_name, bulk=True
            )
        )

    def filter(self, filter: dict):
        """
        Retrieves user data based on a filter criteria from the database table.

        Args:
            filter (dict): The filter criteria for querying user data.

        Returns:
            response: A list of user data that matches the filter criteria.
        """
        return list(
            self.__db.query(
                db_name=self.__db_name,
                table_name=self.__table_name,
                filter=filter,
                bulk=True,
            )
        )

    def update(self, data: dict):
        """
        Updates user data in the database table.

        Args:
            data (dict): The user data to be updated.

        Returns:
            response: The response code from the database operation.
        """
        return self.__db.update(
            db_name=self.__db_name, table_name=self.__table_name, data=data
        )

    def delete(self, filter: dict):
        """
        Deletes user data based on a filter criteria from the database table.

        Args:
            filter (dict): The filter criteria for deleting user data.

        Returns:
            response: The response code from the database operation.
        """
        return self.__db.delete(
            db_name=self.__db_name, table_name=self.__table_name, filter=filter
        )
