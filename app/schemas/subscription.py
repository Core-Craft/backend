from datetime import datetime
from typing import List

import pytz
from bson import ObjectId
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


class SubSearch(BaseModel):
    """
    Represents a subscription search model with optional filter criteria.

    Attributes:
        - user_uuid (int): The unique identifier for the user.

    """

    user_uuid: int | None = None

    class Config:
        """
        Configuration options for Pydantic models.

        Attributes:
            from_attributes (bool): Determines whether attribute values should be populated from class attributes when creating an instance of the model. If True, class attributes with the same name as fields in the model will be used to initialize those fields. Defaults to True, enabling attribute initialization from class attributes.
        """

        from_attributes = True


class SubUpdate(BaseModel):
    """
        Represents a subscription update model for modifying subscription data.

        This class includes two fields:
        - filter: An instance of the SubSearch class that specifies the filter criteria for identifying the subscription to be updated.
        - sub_data: An instance of the SubscriptionIn class containing updated subscription data.
    """

    filter: SubSearch
    user_data: SubscriptionIn

    class Config:
        """
        Configuration options for Pydantic models.

        Attributes:
            from_attributes (bool): Determines whether attribute values should be populated from class attributes when creating an instance of the model. If True, class attributes with the same name as fields in the model will be used to initialize those fields. Defaults to True, enabling attribute initialization from class attributes.
        """

        from_attributes = True
