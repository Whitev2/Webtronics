from fastapi import APIRouter, HTTPException, status
from fastapi import Depends


router = APIRouter(
    tags=["Users"],
    prefix='/user'
)


