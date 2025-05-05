from pydantic import BaseModel, EmailStr
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    #created_at: datetime
    
class PostCreate(PostBase):
    pass 

class PostResponse(PostBase): #aca manejo las respuestas al usuario
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    #tengo que validar el email. Si la biblioteca no estuviera instalada la instalo:pip install email -validator
    email: EmailStr
    password:str
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        from_attributes = True
    