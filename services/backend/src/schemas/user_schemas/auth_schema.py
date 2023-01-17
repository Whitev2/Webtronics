from pydantic import constr
from pydantic import BaseModel, EmailStr, validator


class SignIn(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=128)


class SignUp(SignIn):
    full_name: str

    password_2: constr(min_length=8, max_length=128)

    @validator('password_2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v

    @validator('full_name')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'must be alphanumeric'
        return v


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
