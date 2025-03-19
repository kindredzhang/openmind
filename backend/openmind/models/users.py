from pydantic import BaseModel, ConfigDict
from typing import Optional
from openmind.internal.db import get_db

class UserSettings(BaseModel):
    ui: Optional[dict] = {}
    model_config = ConfigDict(extra="allow")
    pass

class UsersModel(BaseModel):
    id: str
    name: str
    email: str
    role: str = "pending"

    updated_at: int  # timestamp in epoch
    created_at: int  # timestamp in epoch

class UsersTable:
    def get_user_by_id(self, id: str) -> Optional[UserModel]:
        try:
            with get_db() as db:
                user = db.query(User).filter_by(id=id).first()
                return UsersModel.model_validate(user)
        except Exception:
            return None

    def update_user_last_active_by_id(self, id: str) -> Optional[UserModel]:
        try:
            with get_db() as db:
                db.query(User).filter_by(id=id).update(
                    {"last_active_at": int(time.time())}
                )
                db.commit()

                user = db.query(User).filter_by(id=id).first()
                return UsersModel.model_validate(user)
        except Exception:
            return None

Users = UsersTable()