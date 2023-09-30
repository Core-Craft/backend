from pydantic import EmailStr, constr, validator
import re
from typing import Optional
from .utils import TimestampMixin
from pydantic import BaseModel


class BaseUser(BaseModel):
    id: Optional[int]
    full_name: Optional[constr(
        strip_whitespace=True,
        max_length=50
    )]
    email: Optional[EmailStr]
    phone_no: Optional[str]
    aadhar_no: Optional[int]
    user_type: Optional[constr(
        strip_whitespace=True,
        max_length=50
    )]
    
    @validator("aadhar_no", pre=True, always=True)
    def check_aadhar_no(cls, value):
        if value is not None and not re.match(r"^\d{12}$", str(value)):
            raise ValueError("Aadhar number must be exactly 12 digits long")
        return value
    
    class Config:
        from_attributes = True

   
class UserIn(TimestampMixin, BaseUser):
    password: str
    is_active: bool = True
    is_superuser: bool = False
    
    class Config:
        from_attributes = True


class UserOut(BaseUser):
    pass

class UserSearch(BaseUser):
    pass