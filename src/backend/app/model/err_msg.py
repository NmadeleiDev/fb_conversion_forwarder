from pydantic import BaseModel


class ErrorMsgModel(BaseModel):
    msg: str = 'Unknown error'