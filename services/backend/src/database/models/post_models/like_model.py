from datetime import datetime
from sqlalchemy import Column, String, DateTime, BOOLEAN, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

from src.database.config import Base

user_like = Table('user_like', Base.metadata,
                  Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True),
                  Column("user_id", String, ForeignKey("users.uid"), primary_key=True)
                  )

user_dislike = Table('user_dislike', Base.metadata,
                     Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True),
                     Column("user_id", String, ForeignKey("users.uid"), primary_key=True)
                     )

