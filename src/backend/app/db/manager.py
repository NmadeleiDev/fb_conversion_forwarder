from hashlib import sha256
import os
import logging
from typing import List, Union
import psycopg2

from ..model.domain import EventSourceDomainModel, NewEventSourceDomainModel

from ..model.account import AccountModel, AccountWithPasswdModel, AccountWithTokenModel
from ..model.bm import NewBusinessManagerModel, BusinessManagerModel
from ..model.advertiser_container import AdvertiserContainerModel, NewAdvertiserContainerModel, UpdateAdvertiserContainerModel
from .table_queries import *
from ..model.server_exception import ServerException
from ..utils.utils import generate_random_string


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
        self.domain_table_ref = f'{schema_name}.{domain_table}'
        self.account_table_ref = f'{schema_name}.{auth_table}'

    def create_tables(self, cursor=None):
        with self.conn.cursor() as cursor:
            cursor.execute(schema_create_query)
            cursor.execute(advertiser_container_table_query)
            cursor.execute(domain_table_query)
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
    def get_bms(self, ac_id=None, pixel_id=None) -> List[BusinessManagerModel]:
        query = f"""SELECT ad_container_id, id, name, access_token, pixel_id, fields_sent, fields_generated, event_source_domain FROM {self.bm_table_ref}"""
        
        args = []
        filters = []
        if ac_id is not None:
            filters.append('ad_container_id = %s')
            args.append(ac_id)
        if pixel_id is not None:
            filters.append('pixel_id = %s')
            args.append(pixel_id)

        if len(filters) > 0:
            query += (' WHERE ' + ' AND '.join(filters))

        with self.conn.cursor() as curs:
            curs.execute(query, tuple(args))
            return [BusinessManagerModel(
                ad_container_id=int(x[0]),
                id=x[1],
                name=x[2], 
                access_token=x[3],
                pixel_id=x[4], 
                fields_sent=x[5], 
                fields_generated=x[6],
                event_source_domain=x[7]) for x in curs.fetchall()]

    def insert_bm(self, bm: NewBusinessManagerModel) -> BusinessManagerModel:
        query = f"""INSERT INTO {self.bm_table_ref} (name, ad_container_id, access_token, pixel_id, fields_sent, fields_generated, event_source_domain) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id"""

        with self.conn.cursor() as curs:
            curs.execute(query, (bm.name, bm.ad_container_id, bm.access_token, bm.pixel_id, bm.fields_sent, bm.fields_generated, bm.event_source_domain))
            new_id = curs.fetchone()[0]
            return BusinessManagerModel(id=new_id, **bm.dict())

    def update_bm(self, bm: BusinessManagerModel):
        query = f"""UPDATE {self.bm_table_ref} SET (name, access_token, pixel_id, fields_sent, fields_generated, event_source_domain) = (%s,%s,%s,%s,%s,%s) WHERE id = %s"""

        with self.conn.cursor() as curs:
            curs.execute(query, (bm.name, bm.access_token, bm.pixel_id, bm.fields_sent, bm.fields_generated, bm.event_source_domain, bm.id))

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

        
    # CRUD Domains
    def get_domains(self) -> List[EventSourceDomainModel]:
        query = f"""SELECT id, domain, fb_meta_tag FROM {self.domain_table_ref}"""

        with self.conn.cursor() as curs:
            curs.execute(query)
            return [EventSourceDomainModel(
                id=x[0], domain=x[1], fb_meta_tag=x[2]) for x in curs.fetchall()]

    def get_domain(self, domain: str) -> EventSourceDomainModel:
        query = f"""SELECT id, fb_meta_tag FROM {self.domain_table_ref} WHERE domain=%s"""

        with self.conn.cursor() as curs:
            curs.execute(query, (domain,))
            data = curs.fetchone()
            return EventSourceDomainModel(id=data[0], fb_meta_tag=data[1], domain=domain)

    def insert_domain(self, data: NewEventSourceDomainModel) -> EventSourceDomainModel:
        query = f"""INSERT INTO {self.domain_table_ref} (domain, fb_meta_tag) VALUES (%s,%s) RETURNING id"""

        with self.conn.cursor() as curs:
            curs.execute(query, (data.domain, data.fb_meta_tag))
            new_id = curs.fetchone()[0]
            return EventSourceDomainModel(id=new_id, **data.dict())

    def update_domain(self, data: EventSourceDomainModel):
        query = f"""UPDATE {self.domain_table_ref} SET fb_meta_tag = %s WHERE id = %s"""

        with self.conn.cursor() as curs:
            curs.execute(query, (data.fb_meta_tag, data.id))

    def delete_domain(self, id: str):
        query = f"""DELETE FROM {self.domain_table_ref} WHERE id = %s"""

        with self.conn.cursor() as curs:
            curs.execute(query, (id, ))

    