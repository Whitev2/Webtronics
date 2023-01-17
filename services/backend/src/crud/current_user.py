
from uuid import uuid4

from sqlalchemy import exc, select, insert, update
from fastapi import HTTPException, status, Depends

from src.core.jwt_handler import JwtHandler
from src.core.security import Password, JWTBearer
from src.crud.user_crud import UserCrud
from src.database.config import async_session
from src.database.models.user_models.user_model import User
from src.routers.dopends import get_user_crud
from src.schemas.user_schemas.auth_schema import SignUp, Token
from src.schemas.user_schemas.user_schema import UserOut, CurrentUser


async def get_current_user(users: UserCrud = Depends(get_user_crud),
                           token: str = Depends(JWTBearer())) -> CurrentUser:
    cred_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid")
    try:
        payload = JwtHandler().decode_access_token(token)
    except AttributeError:
        raise cred_exception
    if payload is None:
        raise cred_exception
    user_jwt: dict = payload.get("user")
    email = user_jwt.get('email', None)

    if email is None:
        raise cred_exception

    user = await users.get_by_email(email)
    if user is None:
        raise cred_exception
    return CurrentUser(user=UserOut(**user.__dict__))