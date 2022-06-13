from io import StringIO
import logging
from typing import List
from fastapi import APIRouter, status
from fastapi.responses import PlainTextResponse
from .helpers.auth import CookieAuthMiddlewareRoute

from ...db.manager import DbManager

from ...model.bm import BusinessManagerModel, NewBusinessManagerModel, UpdateBusinessManagerModel

router = APIRouter(
    prefix="/admin",
    tags=["Service administration"],
    route_class=CookieAuthMiddlewareRoute
)

@router.get('/bm', status_code=status.HTTP_200_OK, response_model=List[BusinessManagerModel])
async def get_bms():
    return DbManager().get_bms()

@router.post('/bm', status_code=status.HTTP_200_OK, response_model=BusinessManagerModel)
async def create_bm(body: NewBusinessManagerModel):
    return DbManager().insert_bm(body)

@router.put('/bm', status_code=status.HTTP_200_OK)
async def update_bm(body: UpdateBusinessManagerModel):
    DbManager().update_bm(body)

@router.delete('/bm', status_code=status.HTTP_200_OK)
async def delete_bm(bm_id: str):
    DbManager().delete_bm(bm_id)

@router.get('/pixel', status_code=status.HTTP_200_OK, response_class=PlainTextResponse)
async def get_forwarder_pixel_script(bm_id: str):
    secret = DbManager().get_bm_forwarder_secret(bm_id)

    with open('pixel_script.js', 'r') as f:
        cont = f.read()
        cont = cont.replace('ACCOUNT_TOKEN_PLACEHOLDER', f'{bm_id}.{secret}')

        return cont
