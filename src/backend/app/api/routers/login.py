import random
import string
from fastapi import APIRouter, FastAPI, Header, Response, Request, status, UploadFile, File
from .helpers.auth import CookieAuthMiddlewareRoute, add_auth_cookie_to_response
from fastapi.responses import JSONResponse

from ...model.err_msg import ErrorMsgModel
from ...model.account import AccountWithPasswdModel, AccountWithTokenModel

from ...db.manager import DbManager

router = APIRouter(
    prefix="/login",
    tags=["System login"],
)

db = DbManager()

def dummy_random_string(n) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

@router.post('/', status_code=status.HTTP_200_OK)
async def login_to_account(request: Request, response: Response, body: AccountWithPasswdModel):
    db = DbManager()
    if db.auth_account_password(body):
        with_token = AccountWithTokenModel(email=body.email, token=dummy_random_string(32))
        db.update_account_token(with_token)
        add_auth_cookie_to_response(request, response, with_token)
    else:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=ErrorMsgModel(msg='auth error').dict())

