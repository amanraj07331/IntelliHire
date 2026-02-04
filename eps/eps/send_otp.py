from fastapi import APIRouter, HTTPException
from modules.database import Database
from pydantic import BaseModel
from modules.email import EmailService
import random
from datetime import datetime, timedelta

router = APIRouter()

database = Database()

@router.on_event("startup")
async def on_startup():
    await database.initialize()

class EmailData(BaseModel):
    email: str

email_service = EmailService()


def generate_otp():
    rnd = random.randint(1000, 9999)
    exp = datetime.now() + timedelta(minutes=5)
    exp_unix = int(exp.timestamp())
    otp = f"{rnd}_{exp_unix}"
    return otp


@router.post("/send_otp")
async def send_otp(email_data: EmailData):
    otp = str(generate_otp())
    try:
        send_otp = otp.split("_")[0]
        email_service.send_otp(email_data.email, send_otp)
        await database.delete_otp(email_data.email)
        await database.insert_otp(email_data.email, otp)
        # background_tasks.add_task(database.remove_otp, email_data.email)
        return {"message": "OTP sent to your email."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))