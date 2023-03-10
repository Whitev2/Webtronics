from datetime import datetime
from pydantic import BaseModel


class PostIn(BaseModel):
    name: str
    description: str


class PostOut(BaseModel):
    id: int
    owner: str

    name: str
    description: str

    like_count: int
    dislike_count: int

    created_at = datetime
    modified_at = datetime


class CurrentPost(BaseModel):
    post: PostOut


class UserReactions(BaseModel):
    uid: str
    full_name: str


class PostReactionOut(PostOut):
    pass
