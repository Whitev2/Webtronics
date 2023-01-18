from sqlalchemy import Column, String, Integer, ForeignKey, Table

from src.database.config import Base

user_like = Table('user_like', Base.metadata,
                  Column("user_id", String, ForeignKey("users.uid", ondelete="CASCADE"), primary_key=True),
                  Column("post_id", Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
                  )

user_dislike = Table('user_dislike', Base.metadata,
                     Column("user_id", String, ForeignKey("users.uid", ondelete="CASCADE"), primary_key=True),
                     Column("post_id", Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
                     )
