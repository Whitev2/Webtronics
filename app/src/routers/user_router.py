from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.current_user import get_current_user
from src.crud.user_crud import UserCrud
from src.routers.dopends import get_db
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
                 db_session: AsyncSession = Depends(get_db),
                 current_user: CurrentUser = Depends(get_current_user)):
    user_crud = UserCrud(db_session)
    new_user = await user_crud.update(update_data, current_user)
    return new_user


@router.delete("/delete", status_code=200)
async def delete(db_session: AsyncSession = Depends(get_db),
                 current_user: CurrentUser = Depends(get_current_user)):
    user_crud = UserCrud(db_session)
    delete_info = await user_crud.delete(current_user)
    return delete_info
