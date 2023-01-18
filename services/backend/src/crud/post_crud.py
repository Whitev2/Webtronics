from typing import List
from fastapi import HTTPException, status

from sqlalchemy import exc, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.post_models.post_model import Post
from src.database.models.user_models.user_model import User
from src.schemas.post_schemas.post_schema import CurrentPost, PostOut, PostIn, PostReactionOut
from src.schemas.user_schemas.user_schema import CurrentUser


class PostCrud:

    def __init__(self, db_session: AsyncSession) -> None:
        self._db_session: AsyncSession = db_session

    async def create(self, post_in: PostIn, current_user: CurrentUser) -> CurrentPost:

        post = Post(**post_in.dict(exclude_unset=True), owner=current_user.user.uid)
        user: User = await self._db_session.get(User, current_user.user.uid)
        user.posts.append(post)

        try:
            self._db_session.add(user)
            await self._db_session.commit()
        except Exception as e:
            await self._db_session.rollback()

        return CurrentPost(post=PostOut(**post.__dict__))

    async def get_by_id(self, post_id: int) -> Post:
        return await self._db_session.get(Post, post_id)

    async def update(self, post_id: int, post_in: PostIn, current_user: CurrentUser) -> CurrentPost:

        current_post: Post = await self.get_by_id(post_id)

        if current_post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Current post not found")

        if current_post.owner != current_user.user.uid:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can't edit someone else's post")

        stmt = (
            update(Post).
            where(Post.id == post_id).
            values({**post_in.dict(exclude_unset=True)})
        )

        try:
            await self._db_session.execute(stmt)
            await self._db_session.commit()
        except exc.IntegrityError:
            await self._db_session.rollback()

        new_post: Post = await self._db_session.get(Post, post_id)
        return CurrentPost(post=PostOut(**new_post.__dict__))

    async def delete(self, post_id: int, current_user: CurrentUser):

        current_post: Post = await self.get_by_id(post_id)

        if current_post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Current post not found")

        if current_post.owner != current_user.user.uid:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can't edit someone else's post")

        stmt = (
            delete(Post).
            where(Post.id == post_id)
        )

        try:
            await self._db_session.execute(stmt)
            await self._db_session.commit()
        except exc.IntegrityError:
            await self._db_session.rollback()

        return HTTPException(status_code=status.HTTP_200_OK, detail=f"Post with id <{post_id}> has ben deleted")

    async def add_like(self, post_id: int, current_user: CurrentUser) -> PostReactionOut:

        user: User = await self._db_session.get(User, current_user.user.uid)
        post: Post = await self._db_session.get(Post, post_id)

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
            self._db_session.add(post)
            await self._db_session.commit()
        except exc.IntegrityError:
            await self._db_session.rollback()

        return PostReactionOut(**post.__dict__)

    async def add_dislike(self, post_id: int, current_user: CurrentUser) -> PostReactionOut:

        user: User = await self._db_session.get(User, current_user.user.uid)
        post: Post = await self._db_session.get(Post, post_id)

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
            self._db_session.add(post)
            await self._db_session.commit()
        except exc.IntegrityError:
            await self._db_session.rollback()

        return PostReactionOut(**post.__dict__)

    async def get_owner_posts(self, current_user: CurrentUser) -> List[CurrentPost]:

        user: User = await self._db_session.get(User, current_user.user.uid)

        post_list = list()
        for post in user.posts:
            post_list.append(CurrentPost(post=PostOut(**post.__dict__)))

        return post_list

    async def get_user_posts(self, user_id: str) -> List[CurrentPost]:

        user: User = await self._db_session.get(User, user_id)

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        post_list = list()
        for post in user.posts:
            post_list.append(CurrentPost(post=PostOut(**post.__dict__)))

        return post_list

    async def get_all_posts(self, page: int, page_size: int) -> List[CurrentPost]:

        result = await self._db_session.execute(self.page_sizer(page, page_size))

        posts = result.unique()

        order_list = list()
        for post in posts:
            order_list.append(CurrentPost(post=PostOut(**post[0].__dict__)))

        return order_list

    @classmethod
    def page_sizer(cls, page: int = 0, page_size: int = 10):

        query = select(Post).order_by(Post.id.desc())

        if page_size:
            query = query.limit(page_size)
        if page:
            query = query.offset(page * page_size)

        return query
