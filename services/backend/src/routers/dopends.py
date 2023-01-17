from src.crud.post_crud import PostCrud
from src.crud.user_crud import UserCrud


def get_user_crud() -> UserCrud:
    return UserCrud()


def get_post_crud() -> PostCrud:
    return PostCrud()
