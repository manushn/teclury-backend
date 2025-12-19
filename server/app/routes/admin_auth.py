from fastapi import APIRouter, HTTPException,BackgroundTasks
from jose import jwt
from pydantic import BaseModel, EmailStr
import time, os,random
from app.emailserve.email_service import send_email


router = APIRouter(prefix="/admin", tags=["Admin Auth"])

JWT_SECRET = os.getenv("JWT_SECRET")
ADMIN_EMAILS = os.getenv("ADMIN_EMAILS")


otp_store = {}
OTP_EXPIRY = 300  

class EmailRequest(BaseModel):
    email: EmailStr

class EmailVerifys(BaseModel):
    email:EmailStr
    otp:str

def generate_otp():
    return f"{random.randint(100000, 999999)}"

@router.post("/send-otp")
def send_otp(data: EmailRequest,background_tasks: BackgroundTasks):
    email=data.email
    if email not in ADMIN_EMAILS:
        raise HTTPException(status_code=200, detail="Invalid admin email")

    otp = generate_otp()
    expires_at = time.time() + OTP_EXPIRY

    otp_store[email] = {
        "otp": otp,
        "expires_at": expires_at
    }

    background_tasks.add_task(   
        send_email,
        email,
        "Admin Login OTP",
        f"Your admin OTP is {otp}. Valid for 5 minutes."
    )

    return {"message": "OTP sent successfully"}


@router.post("/verify-otp")
def verify_otp(data:EmailVerifys):
    email=data.email
    otp=data.otp
    data = otp_store.get(email)

    if not data:
        raise HTTPException(status_code=400, detail="OTP not found")

    if time.time() > data["expires_at"]:
        del otp_store[email]
        raise HTTPException(status_code=200, detail="OTP expired")
    if data["otp"] != otp:
        raise HTTPException(status_code=200, detail="Invalid OTP")

    del otp_store[email] 

    token = jwt.encode(
        {
            "email": email,
            "role": "admin",
            "exp": int(time.time()) + 3600
        },
        JWT_SECRET,
        algorithm="HS256"
    )

    return {
        "success": True,
        "token": token
    }
