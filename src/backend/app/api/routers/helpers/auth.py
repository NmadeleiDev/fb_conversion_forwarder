from datetime import timedelta, datetime
import logging
import os
from typing import Callable, Tuple
from fastapi import Request, Response
from fastapi.routing import APIRoute
import jwt
from fastapi.responses import JSONResponse
from fastapi import status
from ....db.manager import DbManager
from ....model.account import AccountWithTokenModel
from ....model.err_msg import ErrorMsgModel

AUTH_TOKEN_COOKIE_NAME = 'fwdrauth'
SERVER_JWT_SECRET = 'apvTDyxAx9GYNLIAv69Qe'

def get_account_from_request(request: Request) -> Tuple[AccountWithTokenModel | None, bool]:
    if AUTH_TOKEN_COOKIE_NAME in request.cookies.keys():
        token = request.cookies.get(AUTH_TOKEN_COOKIE_NAME)
        try:
            jwtoken = jwt.decode(token, SERVER_JWT_SECRET, algorithms=["HS256"])
        except jwt.ExpiredSignatureError as e:
            logging.debug(f'jwt decode exc: {e}')
            return None, False
        if 'email' not in jwtoken or 'token' not in jwtoken:
            logging.debug(f'jwt token not full: {jwtoken}')
            return None, False
        return AccountWithTokenModel(email=jwtoken['email'], token=jwtoken['token']), True
    else:
        logging.debug('no auth cookie')
        return None, False


def add_auth_cookie_to_response(request: Request, response: Response, acc: AccountWithTokenModel):
    days_to_live = 3
    expr_timestamp = datetime.now() + timedelta(days=days_to_live)
    jwtoken = jwt.encode({
            'email': acc.email, 
            'token': acc.token, 
            'exp': expr_timestamp
        }, 
        SERVER_JWT_SECRET)
    dev_mode = os.environ['DEV_MODE'] == 'on'

    response.set_cookie(AUTH_TOKEN_COOKIE_NAME, jwtoken, 
                        httponly=True, 
                        secure=True,
                        samesite='None' if dev_mode else 'Lax',
                        max_age=timedelta(days=days_to_live).total_seconds())


def remove_auth_cookie_from_response(response: Response):
    dev_mode = os.environ['DEV_MODE'] == 'on'

    response.set_cookie(AUTH_TOKEN_COOKIE_NAME, '', 
                        httponly=True, 
                        secure=True,
                        samesite='None' if dev_mode else 'Lax',
                        max_age=0, expires=0)

class CookieAuthMiddlewareRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            acc, ok = get_account_from_request(request)
            if not ok or acc is None:
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=ErrorMsgModel(msg='get auth error').dict())

            if not DbManager().auth_account_token(acc):
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=ErrorMsgModel(msg='auth error').dict())

            request.state.email = acc.email

            response = await original_route_handler(request)

            return response

        return custom_route_handler
