from fastapi import APIRouter, HTTPException, Response
from modules.database import Database
from pydantic import BaseModel
import  uuid
import random
from datetime import datetime, timedelta

router = APIRouter()

database = Database()

@router.on_event("startup")
async def on_startup():
    await database.initialize()

class VerifyOtpData(BaseModel):
    email: str
    otp: str

COOKIE_NAME = "session"
           
def generate_id():
    id = random.randint(100000, 999999)
    return id

@router.post("/verify_otp")
async def verify_otp(data: VerifyOtpData, response: Response):
    otp_is_expired = await database.check_otp(data.email)
    if otp_is_expired:
        return {"message": "OTP expired"}
    else:
        otp = await database.get_otp(data.email)
        otps = otp.split("_")[0]

        if otps == data.otp:
            expiry_time = datetime.now() + timedelta(seconds=300)
            exp_unix = int(expiry_time.timestamp())
            id = generate_id()
            cookie_id = f"{id}_{str(uuid.uuid4())}"
            await database.insert_session(data.email, cookie_id, exp_unix, otp, id)
            response.set_cookie(
                key=COOKIE_NAME,
                value=cookie_id,
                max_age=300, # 5 minutes
                httponly=True,
                samesite="lax",
            )
            
            # await database.remove_otp_verify(data.email)   
            return {"message": "OTP verified successfully."}
        else:
            raise HTTPException(status_code=400, detail="Invalid OTP.")