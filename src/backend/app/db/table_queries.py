schema_name = "conversion_forwarder"
business_managers_table = "business_manager"
auth_table = "account"

schema_create_query = f"""create schema if not exists {schema_name}"""

BMs_table_query = f"""
create table if not exists {schema_name}.{business_managers_table}
(
	id serial PRIMARY KEY,
	forwarder_secret varchar not null,
	name varchar default null,
	access_token varchar not null,
	pixel_id varchar not null
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

