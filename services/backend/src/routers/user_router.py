from fastapi import APIRouter, HTTPException, status
from fastapi import Depends

from src.crud.current_user import get_current_user
from src.crud.user_crud import UserCrud
from src.routers.dopends import get_user_crud
from src.schemas.user_schemas.user_schema import CurrentUser

router = APIRouter(
    tags=["Users"],
    prefix='/user'
)


@router.get("/", response_model=CurrentUser)
async def get_user(current_user: CurrentUser = Depends(get_current_user)):
    return current_user
