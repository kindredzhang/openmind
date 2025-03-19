from pydantic import BaseModel
from typing import Optional
from openmind.models.users import UserModel
from openmind.internal.db import get_db

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str
    profile_image_url: str

class Token(BaseModel):
    token: str
    token_type: str

class SigninResponse(Token, UserResponse):
    pass

class SignInForm(BaseModel):
    email: str
    password: str

# class AuthsTable:
#     def authenticate_user(self, email: str, password: str) -> Optional[UserModel]:
#         log.info(f"authenticate_user: {email}")
#         try:
#             with get_db() as db:
#                 auth = db.query(Auth).filter_by(email=email, active=True).first()
#                 if auth:
#                     if verify_password(password, auth.password):
#                         user = Users.get_user_by_id(auth.id)
#                         return user
#                     else:
#                         return None
#                 else:
#                     return None
#         except Exception:
#             return None