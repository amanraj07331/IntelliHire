from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from modules.database import Database
from admin.admin import router as admin_router
from eps.send_otp import router as otp_router
from eps.send_file import router as file_router
from eps.verify_otp import router as verify_router
from eps.user_data import router as user_router
from eps.profile import router as profile_router
# from eps.applications import router as application_router

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    database = Database()
    await database.initialize()
    await database.create_table()
    print("database created")

allowed_origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key="1234",
    max_age=300, # 5 minutes
)

app.include_router(otp_router, tags=["otp"])
app.include_router(verify_router, tags=["verify"])
app.include_router(profile_router, tags=["profile"])
app.include_router(file_router, tags=["file"])
# app.include_router(application_router, tags=["application"])
app.include_router(user_router, tags=["user_data"])
app.include_router(admin_router, prefix="/admin", tags=["users"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)