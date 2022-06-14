from hashlib import sha256
import os
import logging
from typing import List, Union
import psycopg2

from ..model.account import AccountModel, AccountWithPasswdModel, AccountWithTokenModel
from ..model.bm import NewBusinessManagerModel, UpdateBusinessManagerModel
from ..model.advertiser_container import AdvertiserContainerModel, NewAdvertiserContainerModel, UpdateAdvertiserContainerModel
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

        self.conn = psycopg2.connect(
            database=self.db_name, user=self.user, password=self.password, host=self.host, port=self.port)

        self.conn.autocommit = True

        self.advertiser_container_table_ref = f'{schema_name}.{advertiser_container_table}'
        self.bm_table_ref = f'{schema_name}.{business_managers_table}'
        self.account_table_ref = f'{schema_name}.{auth_table}'

    def create_tables(self, cursor=None):
        with self.conn.cursor() as cursor:
            cursor.execute(schema_create_query)
            cursor.execute(advertiser_container_table_query)
            cursor.execute(BMs_table_query)
            cursor.execute(auth_table_query)

    #CRUD advertiser_conatiners
    def get_advertiser_conatiners(self) -> List[AdvertiserContainerModel]:
        query = f"""SELECT id, name, forwarder_secret FROM {self.advertiser_container_table_ref}"""

        with self.conn.cursor() as curs:
            curs.execute(query)
            return [AdvertiserContainerModel(
                id=x[0],
                name=x[1], 
                forwarder_secret=x[2]) for x in curs.fetchall()]

    def insert_advertiser_conatiner(self, ac: NewAdvertiserContainerModel) -> AdvertiserContainerModel:
        forwarder_secret = generate_random_string(32)

        query = f"""INSERT INTO {self.advertiser_container_table_ref} (name, forwarder_secret) VALUES (%s,%s) RETURNING id"""

        with self.conn.cursor() as curs:
            curs.execute(query, (ac.name, forwarder_secret))
            new_id = curs.fetchone()[0]
            return AdvertiserContainerModel(id=new_id, forwarder_secret=forwarder_secret, **ac.dict())
 
    def update_advertiser_conatiner(self, ac: UpdateAdvertiserContainerModel):
        query = f"""UPDATE {self.advertiser_container_table_ref} SET name = %s WHERE id = %s"""

        with self.conn.cursor() as curs:
            curs.execute(query, (ac.name, ac.id))

    def delete_advertiser_conatiner(self, ac_id: str):
        query = f"""DELETE FROM {self.advertiser_container_table_ref} WHERE id = %s"""

        with self.conn.cursor() as curs:
            curs.execute(query, (ac_id, ))

    def get_advertiser_conatiner_forwarder_secret(self, ac_id: str) -> str:
        query = f"""SELECT forwarder_secret FROM {self.advertiser_container_table_ref} WHERE id = %s"""

        with self.conn.cursor() as curs:
            curs.execute(query, (ac_id,))
            return curs.fetchone()[0]

    #CRUD BM
    def get_bms_for_ad_container(self, ac_id: int) -> List[UpdateBusinessManagerModel]:
        query = f"""SELECT id, name, access_token, pixel_id FROM {self.bm_table_ref} WHERE ad_container_id = %s"""

        with self.conn.cursor() as curs:
            curs.execute(query, (ac_id,))
            return [UpdateBusinessManagerModel(
                ad_container_id=ac_id,
                id=x[0],
                name=x[1], 
                access_token=x[2],
                pixel_id=x[3]) for x in curs.fetchall()]

    def insert_bm(self, bm: NewBusinessManagerModel) -> UpdateBusinessManagerModel:
        query = f"""INSERT INTO {self.bm_table_ref} (name, ad_container_id, access_token, pixel_id) VALUES (%s,%s,%s,%s) RETURNING id"""

        with self.conn.cursor() as curs:
            curs.execute(query, (bm.name, bm.ad_container_id, bm.access_token, bm.pixel_id))
            new_id = curs.fetchone()[0]
            return UpdateBusinessManagerModel(id=new_id, **bm.dict())

    def update_bm(self, bm: UpdateBusinessManagerModel):
        query = f"""UPDATE {self.bm_table_ref} SET (name, access_token, pixel_id) = (%s,%s,%s) WHERE id = %s"""

        with self.conn.cursor() as curs:
            curs.execute(query, (bm.name, bm.access_token, bm.pixel_id, bm.id))

    def delete_bm(self, bm_id: str):
        query = f"""DELETE FROM {self.bm_table_ref} WHERE id = %s"""

        with self.conn.cursor() as curs:
            curs.execute(query, (bm_id, ))


    # Auth accounts
    def hash_password(self, val: str) -> str:
        return sha256(val.encode('utf-8')).hexdigest()

    def create_account(self, data: AccountWithPasswdModel):
        hashed_ent = AccountWithPasswdModel(email=data.email, password=self.hash_password(data.password))

        query = f"""INSERT INTO {self.account_table_ref} (email, password) VALUES (%s, %s)"""

        with self.conn.cursor() as curs:
            curs.execute(query, (hashed_ent.email, hashed_ent.password))

    def update_account_token(self, data: AccountWithTokenModel):
        query = f"""UPDATE {self.account_table_ref} SET token = %s WHERE email = %s"""

        with self.conn.cursor() as curs:
            curs.execute(query, (data.token, data.email))

    def auth_account_password(self, data: AccountWithPasswdModel) -> bool:
        hashed_ent = AccountWithPasswdModel(email=data.email, password=self.hash_password(data.password))

        query = f"""SELECT password FROM {self.account_table_ref} WHERE email = %s"""

        with self.conn.cursor() as curs:
            curs.execute(query, (hashed_ent.email,))
            passwd = curs.fetchone()[0]
            if passwd == hashed_ent.password:
                return True
            else:
                logging.debug(f"Password incorrect.\nOriginal: {passwd}\nPasswd: {hashed_ent.password}")
                return False

    def auth_account_token(self, data: AccountWithTokenModel) -> bool:
        query = f"""SELECT token FROM {self.account_table_ref} WHERE email = %s"""

        with self.conn.cursor() as curs:
            curs.execute(query, (data.email,))
            token = curs.fetchone()[0]
            return token == data.token

    def delete_account(self, email: str):
        query = f"""DELETE FROM {self.account_table_ref} WHERE email = %s"""

        with self.conn.cursor() as curs:
            curs.execute(query, (email,))


    