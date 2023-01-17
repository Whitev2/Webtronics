from src.crud.user_crud import UserCrud


def get_user_crud() -> UserCrud:
    return UserCrud()
