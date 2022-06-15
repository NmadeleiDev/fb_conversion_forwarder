
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
    user_data = {
        "em": [lower_and_hash(x) for x in conversion.emails] + conversion.hash_emails,
        "ph": [lower_and_hash(filter_str_for_subset(x, string.digits).lstrip('0')) for x in conversion.phones] + conversion.hash_phones,
        "fbc": conversion.fbc,
        "fbp": conversion.fbp,
        "ge": [x.value for x in conversion.genders],
        "db": [lower_and_hash(x) for x in conversion.dates_of_birth] + conversion.hash_dates_of_birth,
        "ln": [lower_and_hash(x) for x in conversion.last_names] + conversion.hash_last_names,
        "ct": [lower_and_hash(x) for x in conversion.cities] + conversion.hash_cities,
        "fn": [lower_and_hash(x) for x in conversion.first_names] + conversion.hash_first_names,
        "country": [lower_and_hash(x) for x in conversion.countries] + conversion.hash_countries,
    }
    if ip:
        user_data["client_ip_address"] = ip
    if user_agent:
        user_data["client_user_agent"] = user_agent
    if conversion.lead_id:
        user_data["lead_id"] = conversion.lead_id

    req_data = {
                "event_name": conversion.event_name,
                "event_time": conversion.event_time,
                "action_source": "website",
                "user_data": user_data,
            }
    if event_source:
        req_data["event_source_url"] = event_source

    return req_data

def send_convesrion(conversion: SendConversionRequest, ip: str, user_agent: str, event_source: str, 
                    pixel_id: str, access_token: str):
    PIXEL_ID = pixel_id
    TOKEN = access_token

    logging.debug(f'Sending conversion to fb with pixel_id={pixel_id}, access_token={access_token}: {conversion.dict()}')

    req_data = create_fb_conversion_event_data(conversion, ip, user_agent, event_source)

    logging.debug(f'Request data: {req_data}')

    resp = requests.post(
        f'https://graph.facebook.com/{API_VERSION}/{PIXEL_ID}/events?access_token={TOKEN}',
        json={
            'data': [
                req_data
            ]
        })
    logging.debug(f"Got resp form FB: {resp.json()}")


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
