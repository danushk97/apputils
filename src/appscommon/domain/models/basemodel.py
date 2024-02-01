from dataclasses import dataclass
from datetime import datetime


@dataclass
class BaseModel:
    created_by: datetime
    created_at: datetime
    last_updated_by: str
    last_updated_at: str
    is_active: bool
