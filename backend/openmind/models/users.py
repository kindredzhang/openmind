from pydantic import BaseModel, ConfigDict
from typing import Optional

class UserSettings(BaseModel):
    ui: Optional[dict] = {}
    model_config = ConfigDict(extra="allow")
    pass

class UserModel(BaseModel):
    id: str
    name: str
    email: str
    role: str = "pending"

    updated_at: int  # timestamp in epoch
    created_at: int  # timestamp in epoch