from fastapi import APIRouter, HTTPException, status
from fastapi import Depends

from src.core.jwt_handler import JwtHandler
from src.core.security import Password, JWTBearer
from src.crud.current_user import get_current_user
from src.crud.user_crud import UserCrud
from src.routers.dopends import get_user_crud
from src.schemas.user_schemas.auth_schema import Token, SignUp, SignIn
from src.schemas.user_schemas.user_schema import CurrentUser

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/signup", status_code=201, response_model=Token)
async def sign_up(signup: SignUp, user: UserCrud = Depends(get_user_crud)):
    token = await user.create(signup)
    return token


@router.post("/signin", response_model=Token)
async def sign_in(signin: SignIn, user: UserCrud = Depends(get_user_crud)):
    user = await user.get_by_email(signin.email)

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
                 user: UserCrud = Depends(get_user_crud)):
    return await user.block_token(token)
