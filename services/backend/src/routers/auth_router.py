from fastapi import APIRouter, HTTPException, status
from fastapi import Depends

from src.crud.user_crud import UserCrud
from src.routers.dopends import get_user_crud
from src.schemas.user_schemas.auth_schema import Token, SignUp

router = APIRouter(
    tags=["Authentication"]
)


@router.post("/sign-up", status_code=201, response_model=Token)
async def sign_up(signup: SignUp, user: UserCrud = Depends(get_user_crud)):
    token = await user.create(signup)
    return token