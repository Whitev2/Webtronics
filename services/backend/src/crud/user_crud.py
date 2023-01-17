from uuid import uuid4

from sqlalchemy import exc, select, insert, update
from fastapi import HTTPException, status

from src.core.jwt_handler import JwtHandler
from src.core.security import Password
from src.database.config import async_session
from src.database.models.user_models.user_model import User
from src.schemas.user_schemas.auth_schema import SignUp, Token


class UserCrud:

    @classmethod
    async def create(cls, signup: SignUp) -> Token:

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

            return Token(
                access_token=JwtHandler().create_access_token(
                    user.uid, {'fullname': user.full_name, 'email': user.email}
                )
            )

        except exc.IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={0: f"Sorry, this email already exists."})


