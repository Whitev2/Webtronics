from datetime import datetime
from typing import Union

from sqlalchemy import Column, String, DateTime, BOOLEAN, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.database.config import Base
from src.database.models.post_models.like_model import user_like, user_dislike


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    owner = Column(String, ForeignKey("users.uid"))
    is_owner = Column(BOOLEAN)

    name = Column(String)
    description = Column(String)

    like_count = Column(Integer, default=0)  # А не пора ли уходить от лайков к эмодзи?)
    dislike_count = Column(Integer, default=0)

    user_likes: list = relationship("User", secondary=user_like, backref="user-likes",  lazy='joined')
    user_dislike: list = relationship("User", secondary=user_dislike, backref="user-dislikes", lazy='joined')

    created_at = Column(DateTime, default=datetime.utcnow())
    modified_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
