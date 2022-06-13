import logging

logging.basicConfig(format='%(asctime)s %(levelname)s ~ %(funcName)s: %(message)s', datefmt='%m/%d/%Y %H:%M:%S :', level=logging.DEBUG)

from fastapi.logger import logger
logger.setLevel(logging.DEBUG)

from .api import api_init

from .db.manager import DbManager

DbManager().create_tables()

app = api_init.get_app()