import asyncio
from uuid import uuid4

from sqlalchemy import exc, select, insert, update, delete
from fastapi import HTTPException, status

from src.core.jwt_handler import JwtHandler
from src.core.security import Password
from src.core.services import Service
from src.database.config import async_session
from src.database.models.user_models.user_model import User
from src.database.redis import DataRedis
from src.schemas.user_schemas.auth_schema import SignUp, Token
from src.schemas.user_schemas.user_schema import UserOut, CurrentUser, UpdateUser


class UserCrud:

    @classmethod
    async def create(cls, signup: SignUp) -> Token:

        asyncio.create_task(Service.hand_search_email(signup.email))

        user = User(
            **signup.dict(exclude_unset=True, exclude={"password", "password_2"}),
            uid=str(uuid4()),
            password=Password().hash_password(signup.password)
        )

        try:
            async with async_session() as session:
                async with session.begin():
                    session.add(user)
                    await session.commit()

        except exc.IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Sorry, this email already exists.")

        return Token(
            access_token=JwtHandler().create_access_token(
                user.uid, {'fullname': user.full_name, 'email': user.email}
            )
        )

    @classmethod
    async def get_by_email(cls, email: str) -> User:

        async with async_session() as session:
            async with session.begin():
                query = await session.execute(select(User).where(User.email == email))

        return query.scalars().first()

    @classmethod
    async def get_by_uid(cls, uid: str) -> User:

        async with async_session() as session:
            async with session.begin():
                query = await session.execute(select(User).where(User.uid == uid))

        return query.scalars().first()

    @classmethod
    async def update(cls, update_data: UpdateUser, current_user: CurrentUser):

        if current_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        values = {**update_data.dict(exclude_unset=True)}

        stmt = (
            update(User).
            where(User.uid == current_user.user.uid).
            values(values)
        )

        async with async_session() as session:
            async with session.begin():
                await session.execute(stmt)

            try:
                await session.commit()
                new_user: User = await session.get(User, current_user.user.uid)
                return CurrentUser(user=UserOut(**new_user.__dict__))
            except exc.IntegrityError:
                await session.rollback()

    @classmethod
    async def delete(cls, current_user: CurrentUser):
        async with async_session() as session:
            async with session.begin():
                await session.execute(delete(User).where(User.uid == current_user.user.uid))
                await session.commit()

        return {"msg": f"User <{current_user.user.uid}> has been deleted"}

    @classmethod
    async def block_token(cls, token):
        await DataRedis().block_jwt(token)
        return HTTPException(status_code=200, detail="token has been blocked")











