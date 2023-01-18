from pydantic import BaseModel, EmailStr


class UserData(BaseModel):
    full_name: str
    email: EmailStr


class UserOut(UserData):
    uid: str


class CurrentUser(BaseModel):
    user: UserOut


class UpdateUser(UserData):
    """
    To update email address or password, can write a validation
    """
    pass
