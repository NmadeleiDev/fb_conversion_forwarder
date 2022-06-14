from pydantic import BaseModel


class NewBusinessManagerModel(BaseModel):
    ad_container_id: int
    name: str
    access_token: str
    pixel_id: str

class UpdateBusinessManagerModel(NewBusinessManagerModel):
    id: str