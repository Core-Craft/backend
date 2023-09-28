from pydantic import EmailStr, constr, validator
import re
from typing import Optional

from .utils import TimestampMixin

class User(TimestampMixin):
    id: int
    full_name: str
    email: EmailStr
    password: str
    phone_no: str
    aadhar_no: Optional[int]
    user_type: str
    is_active: bool
    is_superuser: bool
    
    
    # @validator("phone_no")
    # def check_phoneNumber_format(cls, v):
    #     # write regex for phone no as per indian standards
    #     regExs = (r"\(\w{3}\) \w{3}\-\w{4}", r"^\w{3}\-\w{4}$")
    #     if not re.search(regExs[0], v):
    #         return ValueError("not match")
    #     return v