from typing import Union
from fastapi import APIRouter, FastAPI, Header, Response, Request, status, UploadFile, File

from ...model.err_msg import ErrorMsgModel
from .helpers.auth import CookieAuthMiddlewareRoute
import logging
from fastapi.responses import JSONResponse

from ...model.conversion import SendConversionRequest
from ...fb import conversions_api

from ...db.manager import DbManager

router = APIRouter(
    prefix="/fw",
    tags=["Conversion forwarding"],
)

db = DbManager()

@router.post('/c', status_code=status.HTTP_200_OK)
async def send_conversion_to_fb(
        request: Request, 
        body: SendConversionRequest, 
        user_agent: str = Header(default=None)):

    client_ip = str(request.client.host)

    logging.debug(f'Got request to forward: auth_token={body.auth_token}')
    parts = body.auth_token.split('.')
    ac_id = parts[0]
    fw_secret = parts[1]

    if db.get_advertiser_conatiner_forwarder_secret(ac_id) != fw_secret:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=ErrorMsgModel(msg='secret incorrect').dict())

    bms = db.get_bms_for_ad_container(ac_id)

    logging.debug(f'ac auth success for ac_id={ac_id}')

    for bm in bms:
        conversions_api.send_convesrion(
            conversion=body, 
            ip=client_ip, 
            user_agent=user_agent, 
            event_source=str(request.base_url),
            pixel_id=bm.pixel_id, 
            access_token=bm.access_token
        )

@router.post('/t', status_code=status.HTTP_200_OK)
async def send_test_conversion_to_fb(
        request: Request, 
        test_event_code: str,
        auth_token: str,
        user_agent: str = Header(default=None)):

    client_ip = str(request.client.host)

    parts = auth_token.split('.')
    ac_id = parts[0]
    fw_secret = parts[1]

    if db.get_advertiser_conatiner_forwarder_secret(ac_id) != fw_secret:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=ErrorMsgModel(msg='secret incorrect').dict())

    bms = db.get_bms_for_ad_container(ac_id)

    logging.debug(f'ac auth success for ac_id={ac_id}')

    for bm in bms:
        conversions_api.send_test_conversion(
            test_code=test_event_code,
            ip=client_ip, 
            user_agent=user_agent, 
            event_source=str(request.base_url),
            pixel_id=bm.pixel_id, 
            access_token=bm.access_token
        )