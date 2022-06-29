from typing import Tuple, Union
import logging
import requests


api_key = '66000001b0e76f5e27e94c2bfd4d8116a08cedb7'

def get_fbclicd_and_pixel_id_by_click_id(click_id: str) -> Tuple[str, str, bool]:
    url = f'http://traffictop.online/arm.php?api_key={api_key}&action=clickinfo@get&clickid={click_id}'

    resp = requests.get(url)

    if resp.status_code != 200:
        logging.warn(f'Status code = {resp.status_code} for url: {url}')
        return '', '', False

    body = resp.json()
    if body['status'] != 'true':
        logging.warn(f'Status is not true for url: {url}: {body}')
        return '', '', False

    data = body['click']

    if 'token_6_value' not in data.keys() or 'token_9_value' not in data.keys():
        logging.warn(f'Invalid data for url: {url}: {body}')
        return '', '', False

    return data['token_9_value'], data['token_6_value'], True
