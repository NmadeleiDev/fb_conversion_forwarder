from typing import List, Union
from fastapi import APIRouter, Header, status, Request, Response
from fastapi.responses import PlainTextResponse

from ...model.conversion import SendConversionRequest

from ...fb.conversions_api import send_convesrion, send_test_conversion

from ...model.advertiser_container import AdvertiserContainerModel, NewAdvertiserContainerModel, UpdateAdvertiserContainerModel

from ...model.account import AccountModel, AccountWithPasswdModel
from .helpers.auth import CookieAuthMiddlewareRoute, remove_auth_cookie_from_response

from ...db.manager import DbManager

from ...model.bm import NewBusinessManagerModel, UpdateBusinessManagerModel

router = APIRouter(
    prefix="/admin",
    tags=["Service administration"],
    route_class=CookieAuthMiddlewareRoute
)

@router.get('/ac', status_code=status.HTTP_200_OK, response_model=List[AdvertiserContainerModel])
async def get_acs():
    return DbManager().get_advertiser_conatiners()

@router.post('/ac', status_code=status.HTTP_200_OK, response_model=AdvertiserContainerModel)
async def create_ac(body: NewAdvertiserContainerModel):
    return DbManager().insert_advertiser_conatiner(body)

@router.put('/ac', status_code=status.HTTP_200_OK)
async def update_ac(body: UpdateAdvertiserContainerModel):
    DbManager().update_advertiser_conatiner(body)

@router.delete('/ac', status_code=status.HTTP_200_OK)
async def delete_ac(ac_id: str):
    DbManager().delete_advertiser_conatiner(ac_id)


@router.get('/bm', status_code=status.HTTP_200_OK, response_model=List[UpdateBusinessManagerModel])
async def get_bms(ac_id: int):
    return DbManager().get_bms_for_ad_container(ac_id)

@router.post('/bm', status_code=status.HTTP_200_OK, response_model=UpdateBusinessManagerModel)
async def create_bm(body: NewBusinessManagerModel, request: Request, test_code: Union[str, None] = None, user_agent: str = Header(default=None)):
    created = DbManager().insert_bm(body)
    client_ip = str(request.client.host)

    if test_code is not None and len(test_code) > 0:

        send_test_conversion(test_code, client_ip, user_agent, event_source=str(request.base_url), 
            access_token=body.access_token, pixel_id=body.pixel_id)
        
    send_convesrion(SendConversionRequest(emails=['example@mail.com'], first_names=['Mary']), ip=client_ip, user_agent=user_agent, event_source=str(request.base_url), access_token=body.access_token, pixel_id=body.pixel_id)

    return created

@router.put('/bm', status_code=status.HTTP_200_OK)
async def update_bm(body: UpdateBusinessManagerModel):
    DbManager().update_bm(body)

@router.delete('/bm', status_code=status.HTTP_200_OK)
async def delete_bm(bm_id: str):
    DbManager().delete_bm(bm_id)

@router.get('/account', status_code=status.HTTP_200_OK)
async def is_logged_to_account():
    pass

@router.post('/account', status_code=status.HTTP_200_OK)
async def create_account(body: AccountWithPasswdModel):
    DbManager().create_account(body)

@router.delete('/account', status_code=status.HTTP_200_OK)
async def delete_this_account(request: Request, response: Response):
    DbManager().delete_account(request.state.email)
    remove_auth_cookie_from_response(response)

@router.get('/pixel', status_code=status.HTTP_200_OK, response_class=PlainTextResponse)
async def get_forwarder_pixel_script(ac_id: str):
    secret = DbManager().get_advertiser_conatiner_forwarder_secret(ac_id)

    with open('pixel_script.js', 'r') as f:
        cont = f.read()
        cont = cont.replace('ACCOUNT_TOKEN_PLACEHOLDER', f'{ac_id}.{secret}')

        return cont
