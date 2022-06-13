from pydantic import BaseModel


class NewBusinessManagerModel(BaseModel):
    name: str
    access_token: str
    pixel_id: str

class UpdateBusinessManagerModel(NewBusinessManagerModel):
    id: str

class BusinessManagerModel(UpdateBusinessManagerModel):
    forwarder_secret: str
