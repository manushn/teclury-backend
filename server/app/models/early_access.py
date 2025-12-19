from pydantic import BaseModel, EmailStr

class EarlyAccess(BaseModel):
    name: str
    email: EmailStr
