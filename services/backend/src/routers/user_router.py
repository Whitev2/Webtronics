from fastapi import APIRouter, HTTPException, status
from fastapi import Depends

from src.crud.user_crud import UserCrud
from src.routers.dopends import get_user_crud

router = APIRouter(
    tags=["Users"],
    prefix='/user'
)

