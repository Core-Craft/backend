import re

from bson import ObjectId
from pydantic import BaseModel, EmailStr, constr, validator

from .utils import TimestampMixin


class BaseUser(BaseModel):
    """
    Represents the base user model with common attributes.

    Attributes:
        user_uuid (int): The unique identifier for the user.
        full_name (str): The full name of the user, constrained to 50 characters with leading/trailing whitespaces stripped.
        email (EmailStr, optional): The email address of the user, if provided.
        phone_no (str): The phone number of the user.
        aadhar_no (int, optional): The Aadhar number of the user if provided.
        user_role (str): The role or designation of the user, constrained to 50 characters with leading/trailing whitespaces stripped.

    Config:
        from_attributes (bool): Indicates whether attribute values should be populated from the corresponding class attributes when creating an instance. Defaults to True.
    """

    full_name: constr(strip_whitespace=True, max_length=50) | None = None
    email: EmailStr | None = None
    phone_no: str | None = None
    aadhar_no: int | None = None
    user_role: constr(strip_whitespace=True, max_length=50) | None = None

    class Config:
        """
        Configuration options for Pydantic models.

        Attributes:
            from_attributes (bool): Determines whether attribute values should be populated from class attributes when creating an instance of the model. If True, class attributes with the same name as fields in the model will be used to initialize those fields. Defaults to True, enabling attribute initialization from class attributes.
        """

        from_attributes = True


class UserIn(TimestampMixin, BaseUser):
    """
    Represents a user input model with additional fields and validation.

    Attributes:
        _id (ObjectId): The unique identifier for the user.
        password (str): The password associated with the user.
        is_active (bool): Indicates whether the user account is active. Defaults to True.
        is_superuser (bool): Indicates whether the user has superuser privileges. Defaults to False.

    Validators:
        check_aadhar_no (classmethod): A validator method that checks the Aadhar number (if provided) for its format. Raises a ValueError if the format is invalid.

    Config:
        from_attributes (bool): Indicates whether attribute values should be populated from the corresponding class attributes when creating an instance. Defaults to True.

    Inherits from:
        - TimestampMixin: A mixin class providing timestamp fields (e.g., created_at, updated_at).
        - BaseUser: The base user model with common attributes.

    Note:
        The `check_aadhar_no` validator is applied to the `aadhar_no` field if a value is provided and ensures it is exactly 12 digits long.

    """

    password: str
    is_active: bool = True
    is_superuser: bool = False

    @validator("aadhar_no", pre=True, always=True)
    def check_aadhar_no(cls, value):
        """
        Validate the Aadhar number.

        This validator method checks if the provided Aadhar number (if not None) is a valid 12-digit integer.

        Args:
            cls: The Pydantic model class.
            value: The value of the Aadhar number field to be validated.

        Returns:
            int or None: The validated Aadhar number if it is valid, or None if the input is None.

        Raises:
            ValueError: If the provided Aadhar number is not exactly 12 digits long or has a non-integer format.

        Note:
            This validator is intended for use with Pydantic models and is applied to the "aadhar_no" field.
        """
        if value is not None:
            if not re.match(r"^\d{12}$", str(value)):
                raise ValueError("Aadhar number must be exactly 12 digits long")
        return value

    class Config:
        """
        Configuration options for Pydantic models.

        Attributes:
            from_attributes (bool): Determines whether attribute values should be populated from class attributes when creating an instance of the model. If True, class attributes with the same name as fields in the model will be used to initialize those fields. Defaults to True, enabling attribute initialization from class attributes.
        """

        from_attributes = True


class UserOut(BaseUser):
    """
    Represents a user output model.

    This class inherits attributes and behavior from the `BaseUser` class and is intended to be used for representing user data in output or response objects.

    Inherits from:
        - BaseUser: The base user model with common attributes.

    Note:
        This class does not introduce additional attributes or behavior beyond what is defined in the `BaseUser` class. It serves as a specialized version of `BaseUser` specifically designed for representing user data in response objects.
    """
    user_uuid: int | None = None
    class Config:
        """
        Configuration options for Pydantic models.

        Attributes:
            from_attributes (bool): Determines whether attribute values should be populated from class attributes when creating an instance of the model. If True, class attributes with the same name as fields in the model will be used to initialize those fields. Defaults to True, enabling attribute initialization from class attributes.
        """

        from_attributes = True


class UserSearch(BaseUser):
    """
    Represents a user search model with optional filter criteria.

    This class inherits attributes and behavior from the `BaseUser` class but sets several fields to None, allowing them to be used as optional filter criteria when searching for users.

    Inherits from:
        - BaseUser: The base user model with common attributes.

    Note:
        - Fields that are set to None, such as `user_uuid`, `full_name`, `user_role`, and `phone_no`, can be used as optional filter criteria when performing user searches.
        - When creating instances of this class, you can specify values for specific fields to filter user search results based on the provided criteria.
    """

    class Config:
        """
        Configuration options for Pydantic models.

        Attributes:
            from_attributes (bool): Determines whether attribute values should be populated from class attributes when creating an instance of the model. If True, class attributes with the same name as fields in the model will be used to initialize those fields. Defaults to True, enabling attribute initialization from class attributes.
        """

        from_attributes = True


class UserUpdate(BaseModel):
    """
    Represents a user update model for modifying user data.

    This class includes two fields:
    - filter: An instance of the UserSearch class that specifies the filter criteria for identifying the user to be updated.
    - user_data: An instance of the BaseUser class containing updated user data.

    Attributes:
        filter (UserSearch): An instance of the UserSearch class to specify filter criteria.
        user_data (BaseUser): An instance of the BaseUser class containing updated user data.

    Note:
        - Use this class to define the criteria for selecting a user to update and provide the new user data to be applied.

    Configuration Options:
        - Config.from_attributes (bool): Determines whether attribute values should be populated from class attributes when creating an instance of the model. If True, class attributes with the same name as fields in the model will be used to initialize those fields. Defaults to True, enabling attribute initialization from class attributes.
    """

    filter: UserSearch
    user_data: BaseUser

    class Config:
        """
        Configuration options for Pydantic models.

        Attributes:
            from_attributes (bool): Determines whether attribute values should be populated from class attributes when creating an instance of the model. If True, class attributes with the same name as fields in the model will be used to initialize those fields. Defaults to True, enabling attribute initialization from class attributes.
        """

        from_attributes = True


class UserLogin(BaseModel):
    '''
    Represents a user model for login user.
    '''
    email: str
    password: str
