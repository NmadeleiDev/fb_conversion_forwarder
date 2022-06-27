schema_name = "conversion_forwarder"
business_managers_table = "business_manager"
auth_table = "account"
advertiser_container_table = "advertiser_container_table"
domain_table = "event_source_domain"

schema_create_query = f"""create schema if not exists {schema_name}"""

advertiser_container_table_query = f"""
create table if not exists {schema_name}.{advertiser_container_table}
(
	id serial PRIMARY KEY,
	forwarder_secret varchar not null,
	name varchar default null
);
"""

BMs_table_query = f"""
create table if not exists {schema_name}.{business_managers_table}
(
	id serial PRIMARY KEY,
	ad_container_id integer,
	name varchar default null,
	access_token varchar not null,
	pixel_id varchar not null,
	fields_sent	varchar[] default '{{}}' not null,
	fields_generated varchar[] default '{{}}' not null,
	event_source_domain varchar default '',

	CONSTRAINT fk_ad_container_id
      FOREIGN KEY(ad_container_id) 
	  	REFERENCES {schema_name}.{advertiser_container_table}(id)
		ON DELETE CASCADE
);
"""

domain_table_query = f"""
create table if not exists {schema_name}.{domain_table}
(
	id serial PRIMARY KEY,
	domain varchar not null,
	fb_meta_tag varchar not null,
	created_at timestamp default now() not null
);
"""

auth_table_query = f"""
create table if not exists {schema_name}.{auth_table}
(
	id serial PRIMARY KEY,
	email varchar not null,
	password varchar not null,
	token varchar default null
);
"""

