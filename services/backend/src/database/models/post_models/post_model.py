from datetime import datetime
from sqlalchemy import Column, String, DateTime, BOOLEAN, Integer, ForeignKey

from src.database.config import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    owner = Column(String, ForeignKey("users.uid"))
    is_owner = Column(BOOLEAN)

    name = Column(String)
    description = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow())
    modified_at = Column(DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
