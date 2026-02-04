from fastapi import APIRouter, UploadFile, Request, File
from modules.database import Database
import os

router = APIRouter()
COOKIE_NAME = "session"

database = Database()

@router.on_event("startup")
async def on_startup():
    await database.initialize()


@router.post("/upload_file")
async def send_file(request: Request,file: UploadFile = File(...)):
    print(request.cookies)

    id = request.cookies.get(COOKIE_NAME).split("_")[0]
    SAVE_DIR = "./pdfs"
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    # file_path = os.path.join(SAVE_DIR, "cv.pdf")
    file_path = os.path.join(SAVE_DIR, f"{id}_cv.pdf")
    
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    print(file)
    return {"filename": file.filename}