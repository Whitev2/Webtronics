from fastapi import APIRouter, HTTPException, status
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.jwt_handler import JwtHandler
from src.core.security import Password, JWTBearer
from src.crud.user_crud import UserCrud

from src.routers.dopends import get_db
from src.schemas.user_schemas.auth_schema import Token, SignUp, SignIn

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/signup", status_code=201, response_model=Token)
async def sign_up(signup: SignUp,
                  db_session: AsyncSession = Depends(get_db)):
    user_crud = UserCrud(db_session)
    token = await user_crud.create(signup)
    return token


@router.post("/signin", response_model=Token)
async def sign_in(signin: SignIn, db_session: AsyncSession = Depends(get_db)):
    user_crud = UserCrud(db_session)

    user = await user_crud.get_by_email(signin.email)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Incorrect email, user not found')

    if user is None or not Password().verify_password(signin.password, user.password):
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    return Token(
        access_token=JwtHandler().create_access_token(
            user.uid,
            {'fullname': user.full_name, 'email': user.email}
        )
    )


@router.post("/logout", status_code=200)
async def logout(token: str = Depends(JWTBearer()),
                 db_session: AsyncSession = Depends(get_db)):
    user_crud = UserCrud(db_session)
    return await user_crud.block_token(token)
