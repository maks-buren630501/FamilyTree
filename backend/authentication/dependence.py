from backend.authentication.crud import UserCrud, RefreshTokenCrud


def user_crud():
    return UserCrud()


def refresh_token_crud():
    return RefreshTokenCrud()
