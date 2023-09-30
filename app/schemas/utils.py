from datetime import datetime
from pydantic import BaseModel
import pytz

class TimestampMixin(BaseModel):
    created_at: datetime = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d || %H:%M:%S:%f")
    updated_at: datetime = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d || %H:%M:%S:%f")
