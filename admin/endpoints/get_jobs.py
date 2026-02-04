from fastapi import APIRouter
from db_pool import init_pool
router = APIRouter()

@router.get("/get_jobs")
async def get_user_data():
    pool = await init_pool()
    
    async with pool.acquire() as connection:
        jobs = await connection.fetch(
            """
            SELECT * FROM jobs
            """
        )
        return jobs




# from fastapi import APIRouter
# from sqlalchemy.orm import Session
# from. import models, database

# router = APIRouter()

# @router.get("/get_jobs")
# async def get_jobs():
#     db = Session(database.engine)
#     jobs = db.query(models.Job).all()
#     db.close()
#     return [job.__dict__ for job in jobs]