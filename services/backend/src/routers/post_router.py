from typing import List

from fastapi import APIRouter, HTTPException, status
from fastapi import Depends

from src.core.jwt_handler import JwtHandler
from src.core.security import Password
from src.crud.current_user import get_current_user
from src.crud.post_crud import PostCrud
from src.crud.user_crud import UserCrud
from src.routers.dopends import get_user_crud, get_post_crud
from src.schemas.post_schemas.post_schema import CurrentPost, PostIn, PostReactionOut
from src.schemas.user_schemas.auth_schema import Token, SignUp, SignIn
from src.schemas.user_schemas.user_schema import CurrentUser

router = APIRouter(
    tags=["Posts"],
    prefix='/post'
)


@router.post("/", status_code=201, response_model=CurrentPost)
async def create(create_post: PostIn,
                 current_user: CurrentUser = Depends(get_current_user),
                 post: PostCrud = Depends(get_post_crud)):
    post = await post.create(create_post, current_user)
    return post


@router.put("/", status_code=200, response_model=CurrentPost)
async def update(post_id: int, update_data: PostIn,
                 current_user: CurrentUser = Depends(get_current_user),
                 post: PostCrud = Depends(get_post_crud)):
    post = await post.update(post_id, update_data, current_user)
    return post


@router.delete("/", status_code=200)
async def update(post_id: int,
                 current_user: CurrentUser = Depends(get_current_user),
                 post: PostCrud = Depends(get_post_crud)):
    post = await post.delete(post_id, current_user)
    return post


@router.post("/add-like", status_code=200, response_model=PostReactionOut)
async def add_like(post_id: int,
                   current_user: CurrentUser = Depends(get_current_user),
                   post: PostCrud = Depends(get_post_crud)):
    post = await post.add_like(post_id, current_user)
    return post


@router.post("/add-dislike", status_code=200, response_model=PostReactionOut)
async def add_dislike(post_id: int,
                      current_user: CurrentUser = Depends(get_current_user),
                      post: PostCrud = Depends(get_post_crud)):
    post = await post.add_dislike(post_id, current_user)
    return post


@router.get("/", response_model=List[CurrentPost])
async def owner_posts(current_user: CurrentUser = Depends(get_current_user),
                      post: PostCrud = Depends(get_post_crud)):
    posts = await post.get_owner_posts(current_user)
    return posts


@router.get("/{user_id}", response_model=List[CurrentPost])
async def user_posts(user_id: str,
                     post: PostCrud = Depends(get_post_crud)):
    post = await post.get_user_posts(user_id)
    return post


@router.get("/{page}/{page_size}", response_model=List[CurrentPost])
async def all_posts(page: int, page_size: int,
                    post: PostCrud = Depends(get_post_crud)):
    post = await post.get_all_posts(page, page_size)
    return post
