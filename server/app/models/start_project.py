from pydantic import BaseModel,EmailStr

class StartProject(BaseModel):
    fullname: str
    company: str | None = None
    email: EmailStr
    phone: str
    projectdetails: str
    budget: str
    type: str