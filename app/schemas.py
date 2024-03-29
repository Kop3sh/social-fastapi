from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint


        
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode=True
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
    
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
class PostBase(BaseModel):
    """Pydantic Schema (schema)
    """
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

class PostIntermediate(PostBase):
    id: int
    created_at: datetime
    user: UserResponse
    
    class Config:
        orm_mode=True

class PostResponse(BaseModel):
    Post: PostIntermediate
    votes: int
    
    class Config:
        orm_mode=True
        
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)