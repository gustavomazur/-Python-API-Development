
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title:str
    content:str
    published:bool = True


class PostCreat(PostBase):
    pass



class Post(PostBase):
    title:str 
    content: str
    published: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True) 

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    acess_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None    