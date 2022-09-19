
from typing import List
import requests
from hashlib import sha256
import string
import logging
import random

from facebook_business.api import FacebookAdsApi

from ..model.bm import BusinessManagerModel, FakeableDataFieldsEnum, UserDataFieldsEnum

from ..model.conversion import SendConversionRequest
from facebook_business.adobjects.serverside.gender import Gender

from .sample_data import german_cities, german_names, german_surnames, genders, random_date_of_birth, random_email, random_phone_number

API_VERSION = FacebookAdsApi.API_VERSION
FORWARDER_EVENT_NAME = 'Lead'


def filter_str_for_subset(val: str, subset: set) -> str:
    return ''.join(filter(lambda x: x in subset, val))

def lower_and_hash(val: str) -> str:
    return sha256(val.lower().encode('utf-8')).hexdigest()

def add_fake_data_to_conversion(conversion: SendConversionRequest, fields_to_fake: List[FakeableDataFieldsEnum]):
    if FakeableDataFieldsEnum.cities in fields_to_fake and len(conversion.cities) == 0 and len(conversion.hash_cities) == 0:
        conversion.cities = [random.choice(german_cities)]

    if FakeableDataFieldsEnum.countries in fields_to_fake and len(conversion.countries) == 0 and len(conversion.hash_countries) == 0:
        conversion.countries = 'de'

    if FakeableDataFieldsEnum.dates_of_birth in fields_to_fake and len(conversion.dates_of_birth) == 0 and len(conversion.hash_dates_of_birth) == 0:
        conversion.dates_of_birth = [random_date_of_birth()]

    if FakeableDataFieldsEnum.emails in fields_to_fake and len(conversion.emails) == 0 and len(conversion.hash_emails) == 0:
        conversion.emails = [random_email()]

    if FakeableDataFieldsEnum.first_names in fields_to_fake and len(conversion.first_names) == 0 and len(conversion.hash_first_names) == 0:
        conversion.first_names = [random.choice(german_names)]

    if FakeableDataFieldsEnum.last_names in fields_to_fake and len(conversion.last_names) == 0 and len(conversion.hash_last_names) == 0:
        conversion.last_names = [random.choice(german_surnames)]

    if FakeableDataFieldsEnum.genders in fields_to_fake and len(conversion.genders) == 0:
        conversion.genders = [random.choice([x for x in Gender])]
    
    if FakeableDataFieldsEnum.phones in fields_to_fake and len(conversion.phones) == 0 and len(conversion.hash_phones) == 0:
        conversion.phones = [random_phone_number()]


def create_fb_conversion_event_data(conversion: SendConversionRequest, ip: str, user_agent: str, event_source: str, bm_fields_sent: List[UserDataFieldsEnum], fields_to_fake: List[FakeableDataFieldsEnum] = [], fb_event_name=FORWARDER_EVENT_NAME) -> dict:
    user_data = {}
    if UserDataFieldsEnum.fbc in (bm_fields_sent + fields_to_fake):
        user_data['fbc'] = conversion.fbc
    if UserDataFieldsEnum.fbp in (bm_fields_sent + fields_to_fake):
        user_data['fbp'] = conversion.fbp
    if UserDataFieldsEnum.emails in (bm_fields_sent + fields_to_fake):
        user_data['em'] = [lower_and_hash(x) for x in conversion.emails] + conversion.hash_emails
    if UserDataFieldsEnum.phones in (bm_fields_sent + fields_to_fake):
        user_data['ph'] = [lower_and_hash(filter_str_for_subset(x, string.digits).lstrip('0')) for x in conversion.phones] + conversion.hash_phones
    if UserDataFieldsEnum.last_names in (bm_fields_sent + fields_to_fake):
        user_data['ln'] = [lower_and_hash(x) for x in conversion.last_names] + conversion.hash_last_names
    if UserDataFieldsEnum.first_names in (bm_fields_sent + fields_to_fake):
        user_data['fn'] = [lower_and_hash(x) for x in conversion.first_names] + conversion.hash_first_names
    if UserDataFieldsEnum.cities in (bm_fields_sent + fields_to_fake):
        user_data['ct'] = [lower_and_hash(x) for x in conversion.cities] + conversion.hash_cities
    if UserDataFieldsEnum.countries in (bm_fields_sent + fields_to_fake):
        user_data['country'] = [lower_and_hash(x) for x in conversion.countries] + conversion.hash_countries
    if UserDataFieldsEnum.dates_of_birth in (bm_fields_sent + fields_to_fake):
        user_data['db'] = [lower_and_hash(x) for x in conversion.dates_of_birth] + conversion.hash_dates_of_birth
    if UserDataFieldsEnum.genders in (bm_fields_sent + fields_to_fake):
        user_data['ge'] = [lower_and_hash(x.value) for x in conversion.genders]
    if UserDataFieldsEnum.lead_id in (bm_fields_sent + fields_to_fake):
        user_data['lead_id'] = conversion.lead_id
    if UserDataFieldsEnum.client_ip_address in (bm_fields_sent + fields_to_fake):
        user_data['client_ip_address'] = ip

    # if conversion.clickid is not None:
    #     user_data['external_id'] = conversion.clickid

    if user_agent:
        user_data['client_user_agent'] = user_agent

    req_data = {
                "event_name": fb_event_name,
                "event_time": conversion.event_time,
                "action_source": "website",
                "user_data": user_data,
                "event_source_url": event_source,
            }

    return req_data

def send_convesrion(conversion: SendConversionRequest, ip: str, user_agent: str, event_source: str, 
                    pixel_id: str, access_token: str, bm: BusinessManagerModel):
    PIXEL_ID = pixel_id
    TOKEN = access_token

    add_fake_data_to_conversion(conversion, fields_to_fake=bm.fields_generated)
    req_data = create_fb_conversion_event_data(conversion, ip, user_agent, event_source, bm_fields_sent=bm.fields_sent, fields_to_fake=bm.fields_generated, fb_event_name=bm.fb_event_name)

    logging.debug(f'Request data for pixel {PIXEL_ID}: {req_data}')

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
        auth_token='',
        name=FORWARDER_EVENT_NAME, 
        fbp = 'fb.1.1596403881668.1116446470', 
        fbc = 'fb.1.1554763741205.AbCdEfGhIjKlMnOpQrStUvWxYz1234567890')

    resp = requests.post(
        f'https://graph.facebook.com/{API_VERSION}/{PIXEL_ID}/events?access_token={TOKEN}',
        json={
            'data': [
                create_fb_conversion_event_data(conversion, ip, user_agent, event_source, [x.value for x in UserDataFieldsEnum])
            ],
            'test_event_code': test_code
        })
    logging.debug(f"Got resp form FB test req: {resp.text}")
