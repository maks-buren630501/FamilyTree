from fastapi import FastAPI, Response, status, Depends
from jose import JWTError
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from authentication.config import registration_url_config, activate_url_config, \
    login_url_config, logout_url_config, refresh_url_config
from authentication.crud import RefreshTokenCrud
from user.crud import UserCrud
from user.dependence import user_crud
from authentication.dependence import refresh_token_crud
from authentication.schemas import LoginUserSchema, UpdatePasswordSchema, RecoveryPasswordSchema
from authentication.functions import hash_password, create_registration_token, create_login_token, \
    new_refresh_token, get_refresh_cookies_age, update_refresh_token, create_password_recovery_token
from core.additional import decode_token
from core.email.driver import mail
from core.exception.base_exeption import UniqueIndexException
from core.exception.http_exeption import NotUniqueIndex, TokenError
from core.middleware import error_handler_middleware
from user.schemas import UserSchemaCreate

app_authentication = FastAPI(middleware=[Middleware(BaseHTTPMiddleware, dispatch=error_handler_middleware)])


@app_authentication.post('/registration', **registration_url_config.dict())
async def registration_user(user: UserSchemaCreate, crud: UserCrud = Depends(user_crud)) -> str | Response:
    try:
        if len(user.password) < 8 or len(user.username) < 4:
            return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)
        user.password = hash_password(user.password)
        new_user = await crud.create({**user.dict(), **{'active': False}})
        try:
            registration_token = create_registration_token(new_user).replace('.', '|')
            recovery_link = 'http://127.0.0.1:3000/'
            mail.send_message(
                user.email,
                'Activate account FamilyTree',
                f"Для активации аккаунта <a href=\"{recovery_link}{registration_token}\">перейдите по ссылке</a>"
            )
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
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, path='/',
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
            response.delete_cookie(key='refresh_token', httponly=True, path='/')
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
            response.delete_cookie(key='refresh_token', httponly=True, path='/')
        response.status_code = status.HTTP_200_OK
        return


@app_authentication.post('/start_recovery_password')
async def start_recovery_password(data: RecoveryPasswordSchema, crud: UserCrud = Depends(user_crud)) -> Response:
    data_base_user = await crud.find({'email': data.email})
    if data_base_user:
        password_recovery_token = create_password_recovery_token(data_base_user['id']).replace('.', '|')
        recovery_link = 'http://127.0.0.1:3000/forgot/'
        mail.send_message(
            data.email,
            'Recovery password',
            f"Для изменения пароля <a href=\"{recovery_link}{password_recovery_token}\">перейдите по ссылке</a>"
        )
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
            return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response(status_code=status.HTTP_403_FORBIDDEN)
