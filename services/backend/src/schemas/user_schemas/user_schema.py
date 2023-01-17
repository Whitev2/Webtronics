from pydantic import constr
from pydantic import BaseModel, EmailStr, validator


class UserOut(BaseModel):
    __tablename__ = "users"

    uid: str
    full_name: str
    email: str

