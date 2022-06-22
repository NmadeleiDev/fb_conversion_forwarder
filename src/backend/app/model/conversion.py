from typing import Union
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

from facebook_business.adobjects.serverside.gender import Gender

class SendConversionRequest(BaseModel):
    event_time: int = Field(default_factory=lambda : int(datetime.now().timestamp()))

    emails: List[str] = []
    phones: List[str] = []
    last_names: List[str] = []
    first_names: List[str] = []
    cities: List[str] = []
    countries: List[str] = []
    dates_of_birth: List[str] = []
    
    hash_emails: List[str] = []
    hash_phones: List[str] = []
    hash_last_names: List[str] = []
    hash_first_names: List[str] = []
    hash_cities: List[str] = []
    hash_countries: List[str] = []
    hash_dates_of_birth: List[str] = []

    genders: List[Gender] = []
    fbc: Union[str, None] = None
    fbp: Union[str, None] = None

    lead_id: Union[int, None] = None

    auth_token: str = ''