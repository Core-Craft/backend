from datetime import datetime
from typing import List

from bson import ObjectId
from pydantic import BaseModel

from .utils import TimestampMixin


class BaseSubscription(TimestampMixin):
    start_date: datetime
    end_date: datetime
    amount: int


class SubscriptionIn(BaseModel):
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
