
from typing import List
import requests
from hashlib import sha256
import string
import logging

from facebook_business.api import FacebookAdsApi

from ..model.conversion import SendConversionRequest

API_VERSION = FacebookAdsApi.API_VERSION

def filter_str_for_subset(val: str, subset: set) -> str:
    return ''.join(filter(lambda x: x in subset, val))

def lower_and_hash(val: str) -> str:
    return sha256(val.lower().encode('utf-8')).hexdigest()

def create_fb_conversion_event_data(conversion: SendConversionRequest, ip: str, user_agent: str, event_source: str) -> dict:
    return {
                "event_name": conversion.event_name,
                "event_time": conversion.event_time,
                "event_source_url": event_source,         
                "action_source": "website",
                "user_data": {
                    "client_ip_address": ip,
                    "client_user_agent": user_agent,
                    "em": [lower_and_hash(x) for x in conversion.emails],
                    "ph": [lower_and_hash(filter_str_for_subset(x, string.digits).lstrip('0')) for x in conversion.phones],
                    "fbc": conversion.fbc,
                    "fbp": conversion.fbp,
                    "ge": [x.value for x in conversion.genders],
                    "db": [lower_and_hash(x) for x in conversion.dates_of_birth],
                    "ln": [lower_and_hash(x) for x in conversion.last_names],
                    "fn": [lower_and_hash(x) for x in conversion.first_names],
                    "ct": [lower_and_hash(x) for x in conversion.cities],
                    "country": [lower_and_hash(x) for x in conversion.countries],
                },
            }

def send_convesrion(conversion: SendConversionRequest, ip: str, user_agent: str, event_source: str, 
                    pixel_id: str, access_token: str):
    PIXEL_ID = pixel_id
    TOKEN = access_token

    logging.debug(f'Sending conversion to fb: {conversion.dict()}')
    logging.debug(f'ip={ip}, user_agent={user_agent}, event_source={event_source}')

    resp = requests.post(
        f'https://graph.facebook.com/{API_VERSION}/{PIXEL_ID}/events?access_token={TOKEN}',
        json={
            'data': [
                create_fb_conversion_event_data(conversion, ip, user_agent, event_source)
            ]
        })
    logging.debug(f"Got resp form FB: {resp.text}")


def send_test_conversion(test_code: str, ip: str, user_agent: str, event_source: str, pixel_id: str, access_token: str):
    PIXEL_ID = pixel_id
    TOKEN = access_token

    conversion = SendConversionRequest(
        name='test_event', 
        fbp = 'fb.1.1596403881668.1116446470', 
        fbc = 'fb.1.1554763741205.AbCdEfGhIjKlMnOpQrStUvWxYz1234567890')

    resp = requests.post(
        f'https://graph.facebook.com/{API_VERSION}/{PIXEL_ID}/events?access_token={TOKEN}',
        json={
            'data': [
                create_fb_conversion_event_data(conversion, ip, user_agent, event_source)
            ],
            'test_event_code': test_code
        })
    logging.debug(f"Got resp form FB: {resp.text}")
