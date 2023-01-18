from fastapi import APIRouter, HTTPException, status
from fastapi import Depends

from src.crud.current_user import get_current_user
from src.crud.user_crud import UserCrud
from src.routers.dopends import get_user_crud
from src.schemas.user_schemas.user_schema import CurrentUser, UpdateUser

router = APIRouter(
    tags=["Users"],
    prefix='/user'
)


@router.get("/", response_model=CurrentUser)
async def get_user(current_user: CurrentUser = Depends(get_current_user)):
    return current_user


@router.put("/update", response_model=CurrentUser)
async def update(update_data: UpdateUser,
                 user: UserCrud = Depends(get_user_crud),
                 current_user: CurrentUser = Depends(get_current_user)):
    new_user = await user.update(update_data, current_user)
    return new_user


@router.delete("/delete", status_code=200)
async def delete(user: UserCrud = Depends(get_user_crud),
                 current_user: CurrentUser = Depends(get_current_user)):
    delete_info = await user.delete(current_user)
    return delete_info
