from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.jwt_handler import JwtHandler
from src.core.security import JWTBearer
from src.crud.user_crud import UserCrud
from src.database.redis import DataRedis
from src.routers.dopends import get_db
from src.schemas.user_schemas.user_schema import UserOut, CurrentUser


async def get_current_user(token: str = Depends(JWTBearer()),
                           db_session: AsyncSession = Depends(get_db)) -> CurrentUser:
    user_crud = UserCrud(db_session)

    cred_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credentials are not valid")

    token_status = await DataRedis().get_data(token)

    if token_status == 'blocked':
        raise cred_exception

    payload = JwtHandler().decode_access_token(token)

    if payload is None:
        raise cred_exception

    user_jwt: dict = payload.get("user")
    email = user_jwt.get('email', None)

    if email is None:
        raise cred_exception

    user = await user_crud.get_by_email(email)

    if user is None:
        raise cred_exception

    return CurrentUser(user=UserOut(**user.__dict__))