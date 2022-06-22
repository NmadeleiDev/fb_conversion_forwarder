from enum import Enum
from typing import List
from pydantic import BaseModel

class UserDataFieldsEnum(str, Enum):
    fbc = 'fbc'
    fbp = 'fbp'

    emails = 'Email'
    phones = 'Phone'
    last_names = 'Last name'
    first_names = 'First name'
    cities = 'City'
    countries = 'Country'
    dates_of_birth = 'Date of birth'

    genders = 'Genders'

    lead_id = 'Lead id'
    client_ip_address = 'Client IP address'

class NewBusinessManagerModel(BaseModel):
    ad_container_id: int
    name: str
    access_token: str
    pixel_id: str
    fields_sent: List[UserDataFieldsEnum]

class UpdateBusinessManagerModel(NewBusinessManagerModel):
    id: str