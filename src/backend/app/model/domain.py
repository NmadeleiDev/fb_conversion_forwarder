from pydantic import BaseModel, EmailStr

class NewEventSourceDomainModel(BaseModel):
    domain: str
    fb_meta_tag: str

class EventSourceDomainModel(NewEventSourceDomainModel):
    id: int
    