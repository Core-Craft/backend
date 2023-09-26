from pydantic import BaseModel, Optional

from .utils import TimestampMixin

class User(TimestampMixin):
    id: int
    full_name: str
    email: str
    phone_no: str
    aadhar_no: Optional[int]
    user_type: str
    is_active: bool``
    is_superuser: bool