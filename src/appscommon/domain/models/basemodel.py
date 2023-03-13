from datetime import datetime


class BaseModel:
    def __init__(self,
        created_by: int,
        created_at: datetime,
        last_updated_by: int,
        last_updated_at: datetime
    ) -> None:
        self.created_by = created_by
        self.created_at = created_at
        self.last_updated_by = last_updated_by
        self.last_updated_at = last_updated_at
