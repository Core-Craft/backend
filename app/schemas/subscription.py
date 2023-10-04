from pydantic import BaseModel, EmailStr, constr, validator
from datetime import datetime
from typing import List
from bson import ObjectId
from .utils import TimestampMixin


class BaseSubscription(TimestampMixin):
    start_date: datetime
    end_date: datetime
    amount: int

    class Config:
        """
        Configuration options for Pydantic models.

        Attributes:
            from_attributes (bool): Determines whether attribute values should be populated from class attributes when creating an instance of the model. If True, class attributes with the same name as fields in the model will be used to initialize those fields. Defaults to True, enabling attribute initialization from class attributes.
        """

        from_attributes = True


class SubscriptionIn(BaseModel):
    _id: ObjectId
    user_uuid: int
    subscription: List[BaseSubscription]
