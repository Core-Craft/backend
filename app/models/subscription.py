from .base import Base


class Subscription(Base):
    """
    Represents a class for managing subscription data.

    This class inherits from the `Base` class, which provides generic methods for interacting with a database table. The `Subscription` class is specialized for managing subscription-related data and is configured to interact with a specific database table specified by the "SUBSCRIPTION_TABLE_NAME" environment variable.

    Attributes:
        None

    Methods:
        - __init__(): Initializes a `Subscription` instance, inheriting the database connection and methods from the `Base` class.

    Note:
        - This class is designed for managing subscription data specifically and relies on the generic database operations provided by the `Base` class.
        - The database table name is configured through the "SUBSCRIPTION_TABLE_NAME" environment variable.
    """

    def __init__(self):
        """
        Initialize a Subscription instance for managing subscription-related data.

        The database table name is determined by the "SUBSCRIPTION_TABLE_NAME" environment variable.

        Args:
            None
        """
        super().__init__(table_name="SUBSCRIPTION_TABLE_NAME")
