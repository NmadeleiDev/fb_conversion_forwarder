import logging
from ..model.server_exception import ServerException
from ..utils.utils import generate_random_string
import requests
from os import path
from fastapi import status

BASE_URL = 'https://api.godaddy.com/'

def is_domain_availible(val: str) -> bool:
    res = requests.get(path.join(BASE_URL, 'v1/domains/available'), {'domain': val})

    if res.status_code != status.HTTP_200_OK:
        logging.warn(f"GoDaddy api resp is not 200: {res.status_code}, {res.text}")
        return False

    body = res.json()
    logging.debug(f"Got response from godaddy: {body}")

    return body['available']

def send_purchase_request(domain: str):
    pass    


def purchase_random_domain(domain_prefix='meta-funnel', domain_zone='site') -> str:
    attempt = 0

    while attempt < 10:
        attempt += 1
        domain = f'{domain_prefix}-{generate_random_string(6)}.{domain_zone}'

        if not is_domain_availible(domain):
            continue



