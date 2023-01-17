from datetime import datetime
from sqlalchemy import Column, String, DateTime, BOOLEAN, Integer, ForeignKey

from src.database.config import Base


class Like(Base):
    __tablename__ = "likes"

    post_id = Column(Integer, ForeignKey("posts.id"))
    like_owner_id = Column(String, ForeignKey("users.uid"))