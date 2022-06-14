from pydantic import BaseModel


class NewAdvertiserContainerModel(BaseModel):
    name: str

class UpdateAdvertiserContainerModel(NewAdvertiserContainerModel):
    id: str

class AdvertiserContainerModel(UpdateAdvertiserContainerModel):
    forwarder_secret: str
