from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter
from fastapi import Depends

from src.crud.current_user import get_current_user
from src.crud.post_crud import PostCrud
from src.routers.dopends import get_db
from src.schemas.post_schemas.post_schema import CurrentPost, PostIn, PostReactionOut
from src.schemas.user_schemas.user_schema import CurrentUser

router = APIRouter(
    tags=["Posts"],
    prefix='/post'
)


@router.post("/create", status_code=201, response_model=CurrentPost)
async def create(create_post: PostIn,
                 current_user: CurrentUser = Depends(get_current_user),
                 db_session: AsyncSession = Depends(get_db)):
    post_crud = PostCrud(db_session)
    post = await post_crud.create(create_post, current_user)
    return post


@router.put("/update", status_code=200, response_model=CurrentPost)
async def update(post_id: int, update_data: PostIn,
                 current_user: CurrentUser = Depends(get_current_user),
                 db_session: AsyncSession = Depends(get_db)):
    post_crud = PostCrud(db_session)
    post = await post_crud.update(post_id, update_data, current_user)
    return post


@router.delete("/delete", status_code=200)
async def delete(post_id: int,
                 current_user: CurrentUser = Depends(get_current_user),
                 db_session: AsyncSession = Depends(get_db)):
    post_crud = PostCrud(db_session)
    post = await post_crud.delete(post_id, current_user)
    return post


@router.post("/add-like", status_code=200, response_model=PostReactionOut)
async def add_like(post_id: int,
                   current_user: CurrentUser = Depends(get_current_user),
                   db_session: AsyncSession = Depends(get_db)):
    post_crud = PostCrud(db_session)
    post = await post_crud.add_like(post_id, current_user)
    return post


@router.post("/add-dislike", status_code=200, response_model=PostReactionOut)
async def add_dislike(post_id: int,
                      current_user: CurrentUser = Depends(get_current_user),
                      db_session: AsyncSession = Depends(get_db)):
    post_crud = PostCrud(db_session)
    post = await post_crud.add_dislike(post_id, current_user)
    return post


@router.get("/", response_model=List[CurrentPost])
async def owner_posts(
                      current_user: CurrentUser = Depends(get_current_user),
                      db_session: AsyncSession = Depends(get_db)):
    post_crud = PostCrud(db_session)
    posts = await post_crud.get_owner_posts(current_user)
    return posts


@router.get("/{user_id}", response_model=List[CurrentPost])
async def user_posts(user_id: str,
                     db_session: AsyncSession = Depends(get_db)):
    post_crud = PostCrud(db_session)
    post = await post_crud.get_user_posts(user_id)
    return post


@router.get("/{page}/{page_size}", response_model=List[CurrentPost])
async def all_posts(page: int, page_size: int,
                    db_session: AsyncSession = Depends(get_db)):
    post_crud = PostCrud(db_session)
    post = await post_crud.get_all_posts(page, page_size)
    return post
