import pymongo

from app.exceptions.custom_exceptions import MissingAttributeError


class DataBase:
    """
    Provides a MongoDB database interaction utility.

    This class allows you to interact with a MongoDB database using methods for connecting, validating input data, uploading, querying, updating, and deleting data.

    Args:
        db_url (str, optional): The database connection URL. If provided, the class will establish a connection to the specified MongoDB instance.

    Attributes:
        database_url (str): The database connection URL.
        mongod (pymongo.MongoClient): The MongoDB client instance established using the provided URL.

    Methods:
        - connect(): Establishes a connection to the MongoDB instance.
        - validate(): Validates input data and raises errors for missing or invalid attributes.
        - upload(): Inserts data into the specified database and collection.
        - query(): Retrieves data from the specified database and collection based on provided filters.
        - update(): Updates data in the specified database and collection based on provided filters.
        - delete(): Deletes data from the specified database and collection based on provided filters.

    Note:
        - The class is designed to be used for MongoDB database interactions.
        - You can connect to a MongoDB instance by providing the `db_url` parameter during initialization.
        - The provided methods handle data validation and various database operations.
    """

    def __init__(self, db_url=None):
        """_summary_
        initiate mongodb instance

        Args:
            db_url (str): database connection url
        Response:
            self.mongod: mongodb instance
        """
        if not db_url:
            raise MissingAttributeError("db_url required")
        else:
            if not isinstance(db_url, str):
                raise TypeError(
                    f"Expected a str for 'db_url' but received a {type(db_url).__name__}."
                )

        self.database_url = db_url
        self.mongod = self.connect()

    def connect(self):
        """_summary_
        acts as middleware while connecting to mongo instance

        Returns:
            obj: mongo client
        """
        return pymongo.MongoClient(self.database_url)

    def validate(
        self,
        db_name=None,
        table_name=None,
        data_opt=False,
        data=None,
        filter_opt=False,
        filter=None,
        bulk=False,
    ):
        """_summary_

        Acts as middleware (serializer)
        accepts multiple arguments and raise MissingAttributeError & TypeError if missing/invalid
        """
        if not db_name:
            raise MissingAttributeError("db_name required")
        else:
            if not isinstance(db_name, str):
                raise TypeError(
                    f"Expected a str for 'db_name' but received a {type(db_name).__name__}."
                )

        if not table_name:
            raise MissingAttributeError("table_name required")
        else:
            if not isinstance(table_name, str):
                raise TypeError(
                    f"Expected a str for 'table_name' but received a {type(table_name).__name__}."
                )

        if data_opt:
            if not data:
                raise MissingAttributeError("data required")
            else:
                if not (isinstance(data, dict) or isinstance(data, list)):
                    raise TypeError(
                        f"Expected a dict/list for 'data' but received a {type(data).__name__}."
                    )

        if filter_opt:
            if not filter:
                raise MissingAttributeError("filter required")
            else:
                if not isinstance(filter, dict):
                    raise TypeError(
                        f"Expected a dict for 'filter' but received a {type(filter).__name__}."
                    )

        if bulk:
            if not isinstance(bulk, bool):
                raise TypeError(
                    f"Expected a bool for 'bulk' but received a {type(bulk).__name__}."
                )

    def upload(self, db_name=None, table_name=None, data=None):
        """_summary_

        Args:
            db_name (str): database name.
            table_name (str): table name.
            data (dict, list): data to be dumped over database.
                dict -> to be used for single insertion.
                list -> to be used for bulk insertion.

        Returns:
            response: response code, data
        """
        self.validate(db_name, table_name, data_opt=True, data=data)

        database = self.mongod[db_name]
        dataset = database[table_name]

        if isinstance(data, dict):
            user_id = dataset.find().sort(
                "user_uuid", pymongo.DESCENDING).limit(1)[0]["user_uuid"]
            data.update({"user_uuid": user_id+1})
            response = dataset.insert_one(data)
        else:
            response = dataset.insert_many(data)

        return response

    def query(self, db_name=None, table_name=None, filter=None, bulk=False):
        """_summary_

        Args:
            db_name (str): database name.
            table_name (str): table name.
            filter (dict): filter to be applied over search query
            bulk (bool): multiple results will be returned, if True

        Returns:
            response: response code, data
        """

        self.validate(
            db_name,
            table_name,
            filter_opt=True if filter else False,
            filter=filter,
            bulk=bulk,
        )

        database = self.mongod[db_name]
        dataset = database[table_name]

        if bulk:
            if filter:
                response = dataset.find(filter)
            else:
                response = dataset.find()
        elif filter:
            response = dataset.find_one(filter)
        else:
            response = dataset.find_one()

        return response

    def update(self, db_name=None, table_name=None, data=None, bulk=False):
        """_summary_

        Args:
            db_name (str): database name.
            table_name (str): table name.
            data (dict): data to be updated
            bulk (bool): multiple results will be updated, if True


        Returns:
            response: response code, data
        """
        self.validate(db_name, table_name, data_opt=True, data=data, bulk=bulk)

        database = self.mongod[db_name]
        dataset = database[table_name]

        update = {"$set": data["user_data"]}

        if bulk:
            response = dataset.update_many(data["filter"], update)
        else:
            response = dataset.update_one(data["filter"], update)

        return response

    def delete(self, db_name=None, table_name=None, filter=None):
        """_summary_

        Args:
            db_name (str): database name.
            table_name (str): table name.
            filter (dict): filter to be applied over search query

        Returns:
            response: response code, data
        """
        self.validate(db_name, table_name, filter_opt=True, filter=filter)

        database = self.mongod[db_name]
        dataset = database[table_name]
        response = dataset.delete_one(filter)

        return response
