from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from modules.utils import is_cookie_expired
from modules.database import Database
from fastapi import Query

router = APIRouter()
database = Database()


class EditUserData(BaseModel):
    id: str
    name:str
    phone: str
    address: str

COOKIE_NAME = "session"

@router.on_event("startup")
async def on_startup():
    await database.initialize()

# @router.get("/get_user_data")
# async def get_user_data(request: Request):
#     cookie_id = request.cookies.get(COOKIE_NAME)
#     if cookie_id:
#         if await is_cookie_expired(cookie_id):
#             return {"detail": "Cookie expired"}
#         else:
#             result = await database.user_data_from_db()
#             if result:
#                 return result
#             else:
#                 raise HTTPException(status_code=404, detail="User not found.")
#     else:
#         raise HTTPException(status_code=401, detail="Unauthorized")
    



@router.get("/get_profile_data/email")
async def get_user_data(email: str = Query(..., description="Email of the user to fetch")):
    # Fetch all user data from the database
    all_users = await database.user_data_from_db()
    
    # Filter the results to include only the user with the matching email
    filtered_users = [user for user in all_users if user['email'] == email]
    
    if filtered_users:
        return filtered_users[0]  # Return the first matching user
    else:
        raise HTTPException(status_code=404, detail="User not found.")


@router.post("/get_user_data")
async def edit_user_data(request: Request, user: EditUserData):
    cookie_id = request.cookies.get(COOKIE_NAME)
    if cookie_id:
        if await is_cookie_expired(cookie_id):
            return {"detail": "Cookie expired"}
        else:
            result = await database.edit_user_data(user.id, user.name, user.phone, user.address)
            print(result)
            if result:
                return {"message": f"User data updated successfully for user : {user.email}"}
            else:
                raise HTTPException(status_code=404, detail="User not found.")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
