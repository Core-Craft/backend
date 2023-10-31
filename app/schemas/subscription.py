from datetime import datetime
from typing import List

import pytz
from pydantic import BaseModel

from .utils import TimestampMixin


class BaseSubscription(BaseModel):
    """
    A base subscription model for representing subscription information using Pydantic.

    This class is designed to serve as a base for subscription models. It includes attributes to represent
    the start date, end date, and amount of the subscription.

    Attributes:
        start_date (datetime): The timestamp indicating the creation time of the object.
        end_date (datetime): The timestamp indicating the last update time of the object.
        amount (int, optional): The subscription amount of the user if provided.
    Config:
        from_attributes (bool): Indicates whether attribute values should be populated from the corresponding class attributes when creating an instance. Defaults to True.
    """

    start_date: str = datetime.now(pytz.timezone("Asia/Kolkata")).strftime(
        "%Y-%m-%d || %H:%M:%S:%f"
    )
    end_date: str = datetime.now(pytz.timezone("Asia/Kolkata")).strftime(
        "%Y-%m-%d || %H:%M:%S:%f"
    )
    amount: int | None = None

    class Config:
        """
        Configuration options for Pydantic models.

        Attributes:
            from_attributes (bool): Determines whether attribute values should be populated from class attributes when creating an instance of the model. If True, class attributes with the same name as fields in the model will be used to initialize those fields. Defaults to True, enabling attribute initialization from class attributes.
        """

        from_attributes = True


class SubscriptionIn(TimestampMixin):
    """
    Represents an input model for creating a subscription.

    This class inherits from `TimestampMixin` to include timestamp fields for created and updated dates.

    Attributes:
        user_uuid (int): The unique identifier of the user for whom the subscription is created.
        subscription (List[BaseSubscription]): A list of subscription objects, where each subscription is based on the `BaseSubscription` model.

    Config:
        from_attributes (bool): Indicates whether attribute values should be populated from the corresponding class attributes when creating an instance. Defaults to True.
    """

    user_uuid: int
    subscription: List[BaseSubscription]

    class Config:
        """
        Configuration options for Pydantic models.

        Attributes:
            from_attributes (bool): Determines whether attribute values should be populated from class attributes when creating an instance of the model. If True, class attributes with the same name as fields in the model will be used to initialize those fields. Defaults to True, enabling attribute initialization from class attributes.
        """

        from_attributes = True


class SubscriptionOut(BaseSubscription):
    """
    Represents a user output model for subscription information.

    This class inherits attributes and behavior from the `BaseSubscription` class and is intended to be used for representing subscription data in output or response objects.

    Attributes:
        user_uuid (int): The unique identifier for the user associated with the subscription.

    Inherits from:
        BaseSubscription: The base subscription model with common subscription attributes.

    Note:
        This class does not introduce additional attributes or behavior beyond what is defined in the `BaseSubscription` class. It serves as a specialized version of `BaseSubscription` specifically designed for representing subscription data in response objects.
    """

    user_uuid: int

    class Config:
        """
        Configuration options for Pydantic models.

        Attributes:
            from_attributes (bool): Determines whether attribute values should be populated from class attributes when creating an instance of the model. If True, class attributes with the same name as fields in the model will be used to initialize those fields. Defaults to True, enabling attribute initialization from class attributes.
        """

        from_attributes = True


class SubscriptionSearch(BaseSubscription):
    """
    Represents a user search model with optional filter criteria for subscription information.

    This class inherits attributes and behavior from the `BaseSubscription` class but sets several fields to None, allowing them to be used as optional filter criteria when searching for subscriptions.

    Attributes:
        user_uuid (int | None): The unique identifier for the user, which can be used as an optional filter criterion when searching for subscriptions.

    Inherits from:
        BaseSubscription: The base subscription model with common subscription attributes.

    Note:
        - Fields that are set to None, such as `user_uuid`, `start_date`, `end_date`, and `amount`, can be used as optional filter criteria when performing subscription searches.
        - When creating instances of this class, you can specify values for specific fields to filter subscription search results based on the provided criteria.
    """

    user_uuid: int | None = None

    class Config:
        """
        Configuration options for Pydantic models.

        Attributes:
            from_attributes (bool): Determines whether attribute values should be populated from class attributes when creating an instance of the model. If True, class attributes with the same name as fields in the model will be used to initialize those fields. Defaults to True, enabling attribute initialization from class attributes.
        """

        from_attributes = True


class SubscriptionUpdate(BaseModel):
    """
    Represents a subscription update model for modifying subscription data.

    This class includes two fields:
    - user_uuid (int): The unique identifier for the user whose subscription is being updated.
    - user_data (BaseSubscription): An instance of the `BaseSubscription` class containing the updated subscription data.

    Attributes:
        user_uuid (int): The unique identifier for the user whose subscription is being updated.
        user_data (BaseSubscription): An instance of the `BaseSubscription` class containing the updated subscription data.

    Config:
        from_attributes (bool): Indicates whether attribute values should be populated from the corresponding class attributes when creating an instance. Defaults to True.
    """

    user_uuid: int
    user_data: BaseSubscription

    class Config:
        """
        Configuration options for Pydantic models.

        Attributes:
            from_attributes (bool): Determines whether attribute values should be populated from class attributes when creating an instance of the model. If True, class attributes with the same name as fields in the model will be used to initialize those fields. Defaults to True, enabling attribute initialization from class attributes.
        """

        from_attributes = True
