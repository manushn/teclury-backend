from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.routes.contact import router as contact_router
from app.routes.startproject import router as start_project_router
from app.routes.early_access import router as early_access_router
from app.routes.admin_auth import router as admin_auth_router
from app.routes.getdetails import router as getdetails_router


load_dotenv()


app = FastAPI(title="Startup Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contact_router)
app.include_router(start_project_router)
app.include_router(early_access_router)
app.include_router(admin_auth_router)
app.include_router(getdetails_router)

@app.get("/")
def health():
    return {"status": "Backend running 🚀"}
