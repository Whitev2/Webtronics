from typing import List
from uuid import uuid4

from sqlalchemy import exc, select, insert, update, delete
from fastapi import HTTPException, status

from src.core.jwt_handler import JwtHandler
from src.core.security import Password
from src.database.config import async_session
from src.database.models.post_models.like_model import user_like
from src.database.models.post_models.post_model import Post
from src.database.models.user_models.user_model import User
from src.schemas.post_schemas.post_schema import CurrentPost, PostOut, PostIn, PostReactionOut, UserReactions
from src.schemas.user_schemas.user_schema import UserOut, CurrentUser


class PostCrud:

    @classmethod
    async def create(cls, post_in: PostIn, current_user: CurrentUser) -> CurrentPost:
        post = Post(**post_in.dict(exclude_unset=True), owner=current_user.user.uid)
        try:
            async with async_session() as session:
                async with session.begin():
                    user: User = await session.get(User, current_user.user.uid)
                    user.posts.append(post)
                    session.add(user)
                    await session.commit()

            return CurrentPost(post=PostOut(**post.__dict__))

        except exc.IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"Sorry, this post already exists.")

    @classmethod
    async def get_by_id(cls, post_id: int) -> Post:

        async with async_session() as session:
            async with session.begin():
                return await session.get(Post, post_id)

    @classmethod
    async def update(cls, post_id: int, post_in: PostIn, current_user: CurrentUser) -> CurrentPost:
        current_post: Post = await cls.get_by_id(post_id)

        if current_post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Current post not found")

        if current_post.owner != current_user.user.uid:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can't edit someone else's post")

        values = {**post_in.dict(exclude_unset=True)}
        stmt = (
            update(Post).
            where(Post.id == post_id).
            values(values)
        )

        async with async_session() as session:
            async with session.begin():
                await session.execute(stmt)

            try:
                await session.commit()
                new_post: Post = await session.get(Post, post_id)
                return CurrentPost(post=PostOut(**new_post.__dict__))
            except exc.IntegrityError:
                await session.rollback()

    @classmethod
    async def delete(cls, post_id: int, current_user: CurrentUser):
        current_post: Post = await cls.get_by_id(post_id)

        if current_post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Current post not found")

        if current_post.owner != current_user.user.uid:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can't edit someone else's post")

        stmt = (
            delete(Post).
            where(Post.id == post_id)
        )

        async with async_session() as session:
            async with session.begin():
                await session.execute(stmt)

            try:
                await session.commit()
                return HTTPException(status_code=status.HTTP_200_OK, detail=f"Post with id <{post_id}> has ben deleted")
            except exc.IntegrityError:
                await session.rollback()

    @classmethod
    async def add_like(cls, post_id: int, current_user: CurrentUser) -> PostReactionOut:
        async with async_session() as session:
            async with session.begin():
                user: User = await session.get(User, current_user.user.uid)
                post: Post = await session.get(Post, post_id)

        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

        if post.owner == current_user.user.uid:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot edit your post")

        if user in post.user_likes:  # If the user is on the likes list
            post.user_likes.remove(user)
            post.like_count -= 1

        else:
            post.user_likes.append(user)
            post.like_count += 1

            if user in post.user_dislike:  # if the user clicked like - dislike removed
                post.user_dislike.remove(user)
                post.dislike_count -= 1

        try:
            session.add(post)
            await session.commit()
            return PostReactionOut(**post.__dict__)
        except exc.IntegrityError:
            await session.rollback()

    @classmethod
    async def add_dislike(cls, post_id: int, current_user: CurrentUser) -> PostReactionOut:
        async with async_session() as session:
            async with session.begin():
                user: User = await session.get(User, current_user.user.uid)
                post: Post = await session.get(Post, post_id)

        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

        if post.owner == current_user.user.uid:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot edit your post")

        if user in post.user_dislike:  # If the user is on the dislikes list
            post.user_dislike.remove(user)
            post.dislike_count -= 1

        else:
            post.user_dislike.append(user)
            post.dislike_count += 1

            if user in post.user_likes:  # if the user clicked dislike - like removed
                post.user_likes.remove(user)
                post.like_count -= 1

        try:
            session.add(post)
            await session.commit()
            return PostReactionOut(**post.__dict__)
        except exc.IntegrityError:
            await session.rollback()

    @classmethod
    async def get_owner_posts(cls, current_user: CurrentUser) -> List[CurrentPost]:
        async with async_session() as session:
            async with session.begin():
                user: User = await session.get(User, current_user.user.uid)

        post_list = list()
        for post in user.posts:
            post_list.append(CurrentPost(post=PostOut(**post.__dict__)))

        return post_list

    @classmethod
    async def get_user_posts(cls, user_id: str) -> List[CurrentPost]:
        async with async_session() as session:
            async with session.begin():
                user: User = await session.get(User, user_id)

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        post_list = list()
        for post in user.posts:
            post_list.append(CurrentPost(post=PostOut(**post.__dict__)))

        return post_list

    @classmethod
    async def get_all_posts(cls, page: int = 0, page_size: int = 10) -> List[CurrentPost]:
        async with async_session() as session:
            async with session.begin():
                query = select(Post).order_by(Post.id.desc())
                if page_size:
                    query = query.limit(page_size)
                if page:
                    query = query.offset(page * page_size)
                try:
                    result = await session.execute(query)

                    posts = result.unique()

                    order_list = list()
                    for post in posts:
                        order_list.append(CurrentPost(post=PostOut(**post[0].__dict__)))

                    return order_list
                except exc.IntegrityError:
                    pass



