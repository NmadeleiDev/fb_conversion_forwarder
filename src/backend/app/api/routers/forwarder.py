from datetime import datetime
from typing import Union
from fastapi import APIRouter, FastAPI, Header, Response, Request, status, UploadFile, File

from ...tracker.api import get_fbclicd_and_pixel_id_by_click_id

from ...model.err_msg import ErrorMsgModel
from .helpers.auth import CookieAuthMiddlewareRoute
import logging
from fastapi.responses import JSONResponse

from ...model.conversion import SendConversionRequest
from ...fb import conversions_api

from ...db.manager import DbManager

EVENT_SOURCE_URL = ' https://funnel-end.site/'
DEFAULT_USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36'

router = APIRouter(
    prefix="/fw",
    tags=["Conversion forwarding"],
)

db = DbManager()

@router.get('/cb/{ac_id}/{fw_secret}/hashed', status_code=status.HTTP_200_OK)
@router.get('/cb/{ac_id}/{fw_secret}/raw', status_code=status.HTTP_200_OK)
async def send_conversion_to_fb_s2s(request: Request,
    ac_id: int, fw_secret: str, 
    click_id: str = '',
    event_time: Union[int, None] = None, fbp: Union[str, None] = None, email: Union[str, None] = None, phone: Union[str, None] = None, first_name: Union[str, None] = None, last_name: Union[str, None] = None, city: Union[str, None] = None, country: Union[str, None] = None, date_of_birth: Union[str, None] = None, gender: Union[str, None] = None, lead_id: Union[int, None] = None,
    client_ip: Union[str, None] = None, client_user_agent: Union[str, None] = None):

    logging.debug(f'Got s2s request to forward: ac_id={ac_id}, fw_secret={fw_secret}, click_id={click_id}')

    if db.get_advertiser_container_forwarder_secret(ac_id) != fw_secret:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=ErrorMsgModel(msg='secret incorrect').dict())

    to_hash_fields_prefix = ''
    if request.url.path.split('/')[-1] == 'hashed':
        to_hash_fields_prefix = 'hash_'

    fbclid, pixel_id, ok = get_fbclicd_and_pixel_id_by_click_id(click_id)

    kwargs = {}
    if event_time is not None:
        kwargs['event_time'] = event_time
    if fbclid is not None and fbclid != '':
        kwargs['fbc'] = f'fb.1.{int(datetime.now().timestamp() * 1000)}.{fbclid}'
    if fbp is not None:
        kwargs['fbp'] = fbp
    if email is not None:
        kwargs[f'{to_hash_fields_prefix}emails'] = [email]
    if phone is not None:
        kwargs[f'{to_hash_fields_prefix}phones'] = [phone]
    if first_name is not None:
        kwargs[f'{to_hash_fields_prefix}first_names'] = [first_name]
    if last_name is not None:
        kwargs[f'{to_hash_fields_prefix}last_names'] = [last_name]
    if city is not None:
        kwargs[f'{to_hash_fields_prefix}cities'] = [city]
    if country is not None:
        kwargs[f'{to_hash_fields_prefix}countries'] = [country]
    if date_of_birth is not None:
        kwargs[f'{to_hash_fields_prefix}dates_of_birth'] = [date_of_birth]
    if gender is not None:
        kwargs['genders'] = [gender]
    if lead_id is not None:
        kwargs['lead_id'] = lead_id

    conversion = SendConversionRequest(**kwargs, auth_token='')

    bms = db.get_bms(pixel_id=pixel_id)

    logging.debug(f'Got BMs for ac_id={ac_id}, pixel_id={pixel_id}\nSending conversion to fb for bms ({", ".join([f"(id={x.id} name={x.name} pixel_id={x.pixel_id})" for x in bms])}): {conversion.dict()}')

    if client_user_agent is None or len(client_user_agent) == 0:
        client_user_agent = DEFAULT_USER_AGENT

    for bm in bms:
        conversions_api.send_convesrion(
            conversion=conversion, 
            ip=client_ip, 
            user_agent=client_user_agent, 
            event_source=EVENT_SOURCE_URL,
            pixel_id=bm.pixel_id, 
            access_token=bm.access_token, 
            bm=bm
        )

@router.post('/c/{click_id}', status_code=status.HTTP_200_OK)
async def send_conversion_to_fb_post(
        request: Request, 
        body: SendConversionRequest, 
        click_id: str = '',
        user_agent: str = Header(default=None)):

    client_ip = str(request.client.host)

    logging.debug(f'Got request to forward: auth_token={body.auth_token}, click_id={click_id}')
    parts = body.auth_token.split('.')
    if len(parts) != 2:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=ErrorMsgModel(msg='secret incorrect').dict())
    ac_id = parts[0]
    fw_secret = parts[1]

    if db.get_advertiser_container_forwarder_secret(ac_id) != fw_secret:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=ErrorMsgModel(msg='secret incorrect').dict())

    fbclid, pixel_id, ok = get_fbclicd_and_pixel_id_by_click_id(click_id)
    if not ok:
        logging.warn(f'Failed to get fbclid from click_id={click_id}, body: {body}')
        return

    if ok and (not body.fbc or body.fbc == ''):
        body.fbc = f'fb.1.{int(datetime.now().timestamp() * 1000)}.{fbclid}'

    bms = db.get_bms(pixel_id=pixel_id)

    logging.debug(f'ac auth success for ac_id={ac_id}\nSending conversion to fb for bms ({", ".join([f"(id={x.id} name={x.name} pixel_id={x.pixel_id})" for x in bms])}): {body.dict()}')

    for bm in bms:
        conversions_api.send_convesrion(
            conversion=body, 
            ip=client_ip, 
            user_agent=user_agent, 
            event_source=EVENT_SOURCE_URL,
            pixel_id=bm.pixel_id, 
            access_token=bm.access_token,
            bm=bm
        )

@router.post('/t/{click_id}', status_code=status.HTTP_200_OK)
async def send_test_conversion_to_fb(
        request: Request, 
        test_event_code: str,
        auth_token: str,
        click_id: str = '',
        user_agent: str = Header(default=None)):

    client_ip = str(request.client.host)

    parts = auth_token.split('.')
    if len(parts) != 2:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=ErrorMsgModel(msg='secret incorrect').dict())
    ac_id = parts[0]
    fw_secret = parts[1]

    if db.get_advertiser_container_forwarder_secret(ac_id) != fw_secret:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=ErrorMsgModel(msg='secret incorrect').dict())

    fbclid, pixel_id, ok = get_fbclicd_and_pixel_id_by_click_id(click_id)

    bms = db.get_bms(pixel_id=pixel_id)

    logging.debug(f'ac auth success for ac_id={ac_id}')

    for bm in bms:
        conversions_api.send_test_conversion(
            test_code=test_event_code,
            ip=client_ip, 
            user_agent=user_agent, 
            event_source=EVENT_SOURCE_URL,
            pixel_id=bm.pixel_id, 
            access_token=bm.access_token,
        )