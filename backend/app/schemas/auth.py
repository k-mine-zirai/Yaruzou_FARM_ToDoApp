from typing import Optional
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class User(BaseModel):
    id: str
    email: str
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

class UserData(BaseModel):
    email: str
    password: str