from fastapi import FastAPI, APIRouter
from pydantic import BaseModel

import random
from admin.endpoints.add_jobs import router as add_router
from admin.endpoints.delete_jobs import router as delete_router
from admin.endpoints.get_jobs import router as get_router
from admin.endpoints.update_jobs import router as update_router


router = APIRouter()

class JobData(BaseModel):
    job_title: str
    location: str
    department: str
    salary: str
    employment_type: str
    responsibilities: str
    requirements: str
    experience: str

def get_job_code(dept):
    return f"{dept}_{random.randint(1000, 9999)}"

router.include_router(add_router,prefix='/jobs', tags=["users"])
router.include_router(delete_router,prefix='/jobs', tags=["users"])
router.include_router(get_router,prefix='/jobs', tags=["users"])
router.include_router(update_router,prefix='/jobs', tags=["users"])
