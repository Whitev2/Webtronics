from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.database.config import Base


class User(Base):
    __tablename__ = "users"

    uid = Column(String, primary_key=True, unique=True)

    full_name = Column(String(100), default=None)
    email = Column(String, unique=True)

    password = Column(String(128), default=None)

    posts: list = relationship(
        "Post",
        lazy='joined', backref='user_posts', cascade="all"
    )
