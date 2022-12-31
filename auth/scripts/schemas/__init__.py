from pydantic import BaseModel
from typing import Optional


class RegisterSchema(BaseModel):
    user_id: Optional[str]
    first_name: str
    last_name: str
    email: str
    password: str


class LoginSchema(BaseModel):
    email: str
    password: str
    
class GoogleLoginSchema(BaseModel):
    id_token: str


class DefaultResponseSchema(BaseModel):
    message: str = "success"
    status: str = "success"
    data: Optional[dict] = None
