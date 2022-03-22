from fastapi import FastAPI, Response, status, Depends
from jose import JWTError
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from backend.authentication.config import registration_url_config, activate_url_config, \
    login_url_config, logout_url_config, refresh_url_config
from backend.authentication.crud import RefreshTokenCrud
from backend.user.crud import UserCrud
from backend.user.dependence import user_crud
from backend.authentication.dependence import refresh_token_crud
from backend.authentication.schemas import LoginUserSchema, UpdatePasswordSchema, RecoveryPasswordSchema
from backend.authentication.functions import hash_password, create_registration_token, create_login_token, \
    new_refresh_token, get_refresh_cookies_age, update_refresh_token, create_password_recovery_token
from backend.core.additional import decode_token
from backend.core.email.driver import mail
from backend.core.exception.base_exeption import UniqueIndexException
from backend.core.exception.http_exeption import NotUniqueIndex, TokenError
from backend.core.middleware import error_handler_middleware
from backend.user.schemas import UserSchemaCreate

app_authentication = FastAPI(middleware=[Middleware(BaseHTTPMiddleware, dispatch=error_handler_middleware)])


@app_authentication.post('/registration', **registration_url_config.dict())
async def registration_user(user: UserSchemaCreate, crud: UserCrud = Depends(user_crud)) -> str:
    try:
        user.password = hash_password(user.password)
        new_user = await crud.create({**user.dict(), **{'active': False}})
        try:
            registration_token = create_registration_token(new_user).replace('.', '|')
            mail.send_message(user.email,
                              f"Subject: Activate account FamilyTree\nGo to link '127.0.0.1/{registration_token}'")
            return new_user
        except Exception as e:
            await crud.delete(new_user)
            raise e
    except UniqueIndexException as e:
        raise NotUniqueIndex(e)


@app_authentication.put('/activate/{registration_token}', **activate_url_config.dict())
async def activate_user(registration_token: str, crud: UserCrud = Depends(user_crud)) -> Response:
    try:
        user_data = decode_token(registration_token.replace('|', '.'))
    except JWTError as e:
        raise TokenError(e)
    update_count = await crud.update(user_data['user_id'], {'active': True})
    if update_count:
        return Response(status_code=status.HTTP_201_CREATED)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@app_authentication.post('/login', **login_url_config.dict())
async def login(user: LoginUserSchema, response: Response, crud: UserCrud = Depends(user_crud)) -> Response | dict:
    user.password = hash_password(user.password)
    data_base_user = await crud.find({'username': user.username})
    if data_base_user and data_base_user['password'] == user.password and data_base_user['active']:
        access_token = create_login_token(data_base_user['id'])
        refresh_token = await new_refresh_token(data_base_user['id'])
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, path='api/',
                            max_age=get_refresh_cookies_age(90))
        response.status_code = status.HTTP_200_OK
        return {'access_token': access_token, 'time_out': decode_token(access_token)['exp']}
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)


@app_authentication.get('/refresh', **refresh_url_config.dict())
async def refresh(request: Request, response: Response) -> Response | dict:
    refresh_token = request.cookies.get('refresh_token')
    if refresh_token:
        new_access_token = await update_refresh_token(refresh_token)
        if new_access_token:
            return {'access_token': new_access_token, 'time_out': decode_token(new_access_token)['exp']}
        else:
            response.delete_cookie(key='refresh_token', httponly=True, path='api/')
            response.status_code = status.HTTP_403_FORBIDDEN
            return {}
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)


@app_authentication.get('/logout', **logout_url_config.dict())
async def logout(request: Request, response: Response, refresh_crud: RefreshTokenCrud = Depends(refresh_token_crud)) -> Response | None:
    if not request.scope['user']:
        return Response(status_code=status.HTTP_403_FORBIDDEN)
    else:
        if request.cookies.get('refresh_token'):
            await refresh_crud.delete(request.cookies['refresh_token'])
            response.delete_cookie(key='refresh_token', httponly=True, path='api/')
        response.status_code = status.HTTP_200_OK
        return


@app_authentication.post('/start_recovery_password')
async def start_recovery_password(data: RecoveryPasswordSchema, crud: UserCrud = Depends(user_crud)) -> Response:
    data_base_user = await crud.find({'email': data.email})
    if data_base_user:
        password_recovery_token = create_password_recovery_token(data_base_user['id']).replace('.', '|')
        mail.send_message(data.email,
                          f"Subject: Recovery password FamilyTree\nGo to link '127.0.0.1/forgot/{password_recovery_token}'")
        return Response(status_code=status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@app_authentication.get('/check_recovery_password/{password_recovery_token}')
async def check_recovery_password(password_recovery_token: str) -> Response:
    try:
        user_data = decode_token(password_recovery_token.replace('|', '.'))
    except JWTError as e:
        raise TokenError(e)
    if user_data.get('recovery'):
        return Response(status_code=status.HTTP_200_OK)
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)


@app_authentication.put('/recovery_password/{password_recovery_token}')
async def recovery_password(password_recovery_token: str, data: UpdatePasswordSchema, crud: UserCrud = Depends(user_crud)) -> Response:
    try:
        user_data = decode_token(password_recovery_token.replace('|', '.'))
    except JWTError as e:
        raise TokenError(e)
    if user_data.get('recovery'):
        password = hash_password(data.password)
        update_count = await crud.update(user_data['user_id'], {'password': password})
        if update_count:
            return Response(status_code=status.HTTP_200_OK)
        else:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)

