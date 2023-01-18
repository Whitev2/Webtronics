import asyncio
from uuid import uuid4

from fastapi import HTTPException, status

from sqlalchemy import exc, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.jwt_handler import JwtHandler
from src.core.security import Password
from src.core.services import Service
from src.database.models.user_models.user_model import User
from src.database.redis import DataRedis
from src.schemas.user_schemas.auth_schema import SignUp, Token
from src.schemas.user_schemas.user_schema import UserOut, CurrentUser, UpdateUser


class UserCrud:
    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session: AsyncSession = db_session

    async def create(self, signup: SignUp) -> Token:

        asyncio.create_task(Service.hand_search_email(signup.email))

        user = User(
            **signup.dict(exclude_unset=True, exclude={"password", "password_2"}),
            uid=str(uuid4()),
            password=Password().hash_password(signup.password)
        )

        try:

            self._db_session.add(user)
            await self._db_session.commit()

        except exc.IntegrityError:
            await self._db_session.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Sorry, this email already exists.")

        return Token(
            access_token=JwtHandler().create_access_token(
                user.uid, {'fullname': user.full_name, 'email': user.email}
            )
        )

    async def get_by_email(self, email: str) -> User:

        query = await self._db_session.execute(select(User).where(User.email == email))
        return query.scalars().first()

    async def get_by_uid(self, uid: str) -> User:

        query = await self._db_session.execute(select(User).where(User.uid == uid))
        return query.scalars().first()

    async def update(self, update_data: UpdateUser, current_user: CurrentUser):

        stmt = (
            update(User).
            where(User.uid == current_user.user.uid).
            values({**update_data.dict(exclude_unset=True)})
        )

        try:
            await self._db_session.execute(stmt)
            await self._db_session.commit()
        except exc.IntegrityError:
            await self._db_session.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This email already exist")

        new_user: User = await self._db_session.get(User, current_user.user.uid)
        return CurrentUser(user=UserOut(**new_user.__dict__))

    async def delete(self, current_user: CurrentUser):

        await self._db_session.execute(delete(User).where(User.uid == current_user.user.uid))
        await self._db_session.commit()

        return HTTPException(status_code=200, detail=f"User <{current_user.user.uid}> has been deleted")

    @classmethod
    async def block_token(cls, token):
        await DataRedis().block_jwt(token)
        return HTTPException(status_code=200, detail="token has been blocked")
