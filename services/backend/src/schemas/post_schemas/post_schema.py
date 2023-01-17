from datetime import datetime

from pydantic import constr
from pydantic import BaseModel, EmailStr, validator


class PostIn(BaseModel):
    name: str
    description: str


class PostOut(BaseModel):
    id: int
    owner: str

    name: str
    description: str

    created_at = datetime
    modified_at = datetime


class CurrentPost(BaseModel):
    post: PostOut
