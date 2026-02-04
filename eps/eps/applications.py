from fastapi import APIRouter, HTTPException
from modules.database import Database
from pydantic import BaseModel
import random

router = APIRouter()


class UserData(BaseModel):
    name: str
    phone: str
    email: str
    address: str

database = Database()

@router.on_event("startup")
async def on_startup():
    await database.initialize()

def generate_id():
    id = random.randint(100000, 999999)
    return id
    
@router.post("/applications")
async def application_data(user_data: UserData):
    id = generate_id()
    try:
        users = await database.check_user(user_data.phone, user_data.email)
        if users:
            return{"message": "Record with the provided phone or email already exists."}
        else:
            await database.save_user(user_data.name, user_data.phone, user_data.email, user_data.address, id)
            return{"Message" : "Userdata Saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))