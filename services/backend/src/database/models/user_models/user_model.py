from datetime import datetime
from sqlalchemy import Column, String, DateTime, BOOLEAN
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from src.database.config import Base
from src.database.models.post_models.post_model import Post


class User(Base):
    __tablename__ = "users"

    uid = Column(String, primary_key=True, unique=True)

    full_name = Column(String(100), default=None)
    email = Column(String, unique=True)

    password = Column(String(128), default=None)

    posts: list = relationship(
        "Post",
         lazy='joined', backref='user_posts'
    )
