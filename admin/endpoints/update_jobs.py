from fastapi import APIRouter, Request
import asyncpg
import traceback
from db_pool import init_pool

router = APIRouter()
@router.post("/update_jobs")
async def update_jobs(request: Request): 
    data = await request.json()
    try:
        pool = await init_pool()
        
        async with pool.acquire() as connection:

            # Check if the job exists
            job_exists = await connection.fetchval(
                """
                SELECT EXISTS(
                    SELECT 1 FROM jobs WHERE pk = $1
                )
                """,
                data['pk']
            )
            
            if not job_exists:
                return {"error": "Job not found."}
            
            set_clauses = []
            values = []
            for key, value in data.items():
                if key!= 'pk':
                    set_clauses.append(f"{key} = ${len(values) + 1}")
                    values.append(value)
            
            values.append(data['pk']) 
            
            sql_query = f"""
            UPDATE jobs 
            SET {', '.join(set_clauses)} 
            WHERE pk = ${len(values)}
            """
            
            await connection.execute(sql_query, *values)
            
        return {"message": "Job updated successfully."}
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}







# from fastapi import APIRouter, Request
# from sqlalchemy.orm import Session
# from. import models, database

# router = APIRouter()

# @router.post("/update_jobs")
# async def update_jobs(request: Request):
#     data = await request.json()
#     db = Session(database.engine)
#     try:
#         job = db.query(models.Job).filter_by(pk=data['pk']).first()
#         if not job:
#             return {"error": "Job not found."}
        
#         for attr, value in data.items():
#             setattr(job, attr, value)
        
#         db.commit()
#         return {"message": "Job updated successfully."}
#     finally:
#         db.close()