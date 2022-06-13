from typing import Union
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

from facebook_business.adobjects.serverside.gender import Gender

class SendConversionRequest(BaseModel):
    event_name: str
    event_time: int = Field(default_factory=lambda : int(datetime.now().timestamp()))
    emails: List[str] = []
    phones: List[str] = []
    genders: List[Gender] = []
    fbc: Union[str, None] = None
    fbp: Union[str, None] = None
    last_names: List[str] = []
    first_names: List[str] = []
    dates_of_birth: List[str] = []
    cities: List[str] = []
    countries: List[str] = []

    auth_token: str