from pydantic import BaseModel,EmailStr

class contactModel(BaseModel):
    name:str
    email:EmailStr
    phone:str
    message:str