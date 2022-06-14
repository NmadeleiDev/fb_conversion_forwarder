from pydantic import BaseModel, EmailStr

class AccountModel(BaseModel):
    email: EmailStr

class AccountWithPasswdModel(AccountModel):
    password: str

class AccountWithTokenModel(AccountModel):
    token: str = ''