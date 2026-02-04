from fastapi import APIRouter
from pydantic import BaseModel
import asyncpg
import random
import json
from db_pool import init_pool

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


with open('config.json') as config_file:
    config = json.load(config_file)

def get_job_code(dept):
    return f"{dept}_{random.randint(1000, 9999)}"

@router.post("/add_jobs")
async def add_jobs(job_data: JobData):
    
    pool = await init_pool()
    
    async with pool.acquire() as connection:
        
        result = await connection.fetchrow(
            """
            SELECT job_title FROM jobs WHERE job_title = $1
            """,
            job_data.job_title
        )
        if result:
            
            await connection.execute(
                """
                UPDATE jobs
                SET location = $1, department = $2, salary = $3, employment_type = $4, responsibilities = $5, requirements = $6, experience = $7
                WHERE job_title = $8
                """,
                job_data.job_title, job_data.location, job_data.department, job_data.salary, job_data.employment_type, job_data.responsibilities, job_data.requirements, job_data.experience
            )
            return {f"Job UPDATED successfully : {job_data.job_title}"}
        else:
            pk = get_job_code(job_data.department)
            print(pk)
            # Job title does not exist, insert the new job
            await connection.execute(
                """
                INSERT INTO jobs (job_title, location, department, salary, employment_type, responsibilities, requirements, experience, pk)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                """,
                job_data.job_title, job_data.location, job_data.department, job_data.salary, job_data.employment_type, job_data.responsibilities, job_data.requirements, job_data.experience, pk
            )
            return {"message": f"Job ADDED successfully : {job_data.job_title}"}
