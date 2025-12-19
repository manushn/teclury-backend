from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.routes.contact import router as contact_router
from app.routes.startproject import router as start_project_router
from app.routes.early_access import router as early_access_router
from app.routes.admin_auth import router as admin_auth_router
from app.routes.getdetails import router as getdetails_router

load_dotenv()

ORIGINS = os.getenv("ORIGINS")

if not ORIGINS:
    raise RuntimeError(
        "CORS misconfiguration: ORIGINS environment variable is required"
    )

allowed_origins = [origin.strip() for origin in ORIGINS.split(",") if origin.strip()]

app = FastAPI(title="Startup Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(contact_router)
app.include_router(start_project_router)
app.include_router(early_access_router)
app.include_router(admin_auth_router)
app.include_router(getdetails_router)

@app.get("/")
def health():
    return {"status": "Backend running 🚀"}
