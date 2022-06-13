import os
import logging
from typing import List
import psycopg2
from ..model.bm import BusinessManagerModel, NewBusinessManagerModel, UpdateBusinessManagerModel
from .table_queries import *
from ..model.server_exception import ServerException
from .utils import generate_random_string

from fastapi import status


class DbManager():
    def __init__(self) -> None:
        self.db_name = os.getenv('POSTGRES_DB')
        self.host = os.getenv('POSTGRES_HOST')
        self.port = int(os.getenv('POSTGRES_PORT'))
        self.user = os.getenv('POSTGRES_USER')
        self.password = os.getenv('POSTGRES_PASSWORD')

        logging.debug("Establishing db connection... {}".format(
            (self.db_name, self.user, self.password, self.host, self.port)))
        self.conn = psycopg2.connect(
            database=self.db_name, user=self.user, password=self.password, host=self.host, port=self.port)

        self.conn.autocommit = True
        logging.debug("Connected to db")

        self.bm_table_ref = f'{schema_name}.{business_managers_table}'

    def create_tables(self, cursor=None):
        with self.conn.cursor() as cursor:
            cursor.execute(schema_create_query)
            cursor.execute(BMs_table_query)


    #CRUD BM
    def get_bms(self) -> List[BusinessManagerModel]:
        query = f"""SELECT id, name, forwarder_secret, access_token, pixel_id FROM {self.bm_table_ref}"""

        with self.conn.cursor() as curs:
            curs.execute(query)
            return [BusinessManagerModel(
                id=x[0], 
                name=x[1], 
                forwarder_secret=x[2],
                access_token=x[3],
                pixel_id=x[4]) for x in curs.fetchall()]

    def get_bm_forwarder_secret(self, bm_id: str) -> str:
        query = f"""SELECT forwarder_secret FROM {self.bm_table_ref} WHERE id = %s"""

        with self.conn.cursor() as curs:
            curs.execute(query, (bm_id,))
            return curs.fetchone()[0]

    def insert_bm(self, bm: NewBusinessManagerModel) -> BusinessManagerModel:
        forwarder_secret = generate_random_string(32)

        query = f"""INSERT INTO {self.bm_table_ref} (name, forwarder_secret, access_token, pixel_id) VALUES (%s,%s,%s,%s) RETURNING id"""

        with self.conn.cursor() as curs:
            curs.execute(query, (bm.name, forwarder_secret, bm.access_token, bm.pixel_id))
            new_id = curs.fetchall()[0][0]
            return BusinessManagerModel(id=new_id, forwarder_secret=forwarder_secret, **bm.dict())

    def update_bm(self, bm: UpdateBusinessManagerModel):
        query = f"""UPDATE {self.bm_table_ref} SET (name, access_token, pixel_id) = (%s,%s,%s) WHERE id = %s"""

        with self.conn.cursor() as curs:
            curs.execute(query, (bm.name, bm.access_token, bm.pixel_id, bm.id))

    def delete_bm(self, bm_id: str):
        query = f"""DELETE FROM {self.bm_table_ref} WHERE id = %s"""

        with self.conn.cursor() as curs:
            curs.execute(query, (bm_id, ))

    # For forwarding
    def get_bm_by_id_and_secret(self, bm_id: str, forwarder_secret: str) -> BusinessManagerModel:
        query = f"""SELECT forwarder_secret, access_token, pixel_id FROM {self.bm_table_ref} WHERE id=%s"""

        with self.conn.cursor() as curs:
            curs.execute(query, (bm_id,))
            res = curs.fetchall()
            if len(res) != 1:
                raise ServerException('id not found', http_code=status.HTTP_404_NOT_FOUND)
            true_secret, access_token, pixel_id = res[0]

            if forwarder_secret != true_secret:
                raise ServerException('forwarder_secret incorrect', http_code=status.HTTP_404_NOT_FOUND)

            return BusinessManagerModel(name = '', access_token=access_token, forwarder_secret=true_secret, pixel_id=pixel_id, id=bm_id)
    