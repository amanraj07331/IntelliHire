import asyncpg
import logging
import traceback
import json
from datetime import datetime
from db_pool import init_pool

class Database:
    def __init__(self):
        self.pool = None

    def load_config(self):
        with open('config.json', 'r') as config_file:
            return json.load(config_file)

    
    async def initialize(self):
        self.config = self.load_config()
        try:
            self.pool = await init_pool()
            logging.info("Database pool initialized")
        except Exception as e:
            traceback.print_exc()
            logging.error(f"Failed to initialize database pool: {e}")



    async def delete_otp(self, email):
        if not self.pool:
            raise Exception("Database pool is not initialized")
        async with self.pool.acquire() as connection:
            await connection.execute(
                """
                DELETE FROM login WHERE email = $1
                """,
                email,
            )

    async def create_table(self):
        async with self.pool.acquire() as connection:
            await connection.execute(
                """
                CREATE TABLE IF NOT EXISTS users(
                    "name" text,
                    "phone" text,
                    "email" text,
                    "address" text,
                    "id" integer,
                    "session" text,
                    "expiry" integer,
                    "otp" text
                )
                """
            )
            await connection.execute(
                """
                CREATE TABLE IF NOT EXISTS login(
                    "email" text,
                    "otp" text
                )
                """
            )
            await connection.execute(
                """
                CREATE TABLE IF NOT EXISTS jobs(
                    "job_title" text,
                    "location" text,
                    "department" text,
                    "salary" text,
                    "employment_type" integer,
                    "responsibilities" text,
                    "requirements" text,
                    "experience" text,
                    pk text PRIMARY KEY
                )
                """
            )

    async def check_otp(self, email):
        timee = str(datetime.now().timestamp())
        if not self.pool:
            raise Exception("Database pool is not initialized")
        async with self.pool.acquire() as connection:
            otp_expiry = await connection.fetchval(
                """
                SELECT otp FROM login WHERE email = $1
                """,
                email,
            )
            exp = otp_expiry.split("_")[1]
            
            if exp > timee :
                return False
            else:
                return True
            
    async def user_data_from_db(self):
        if not self.pool:
            raise Exception("Database pool is not initialized")
        async with self.pool.acquire() as connection:
            result = await connection.fetch(
                """
                SELECT * FROM users
                """
                )
            return result
        
    async def edit_user_data(self, email, name=None, phone=None, address=None):
        if not self.pool:
            raise Exception("Database pool is not initialized")

        # Prepare the SQL statement dynamically based on the fields provided
        set_clauses = []
        params = []  # Initialize an empty list for parameters

        if name:
            set_clauses.append(f"name = ${len(params) + 1}")
            params.append(name)
        if phone:
            set_clauses.append(f"phone = ${len(params) + 1}")
            params.append(phone)
        if address:
            set_clauses.append(f"address = ${len(params) + 1}")
            params.append(address)

        if not set_clauses:
            raise ValueError("At least one field to update must be provided")

        params.append(email)

        set_clause_str = ", ".join(set_clauses)
        sql = f"""
        UPDATE users SET {set_clause_str} WHERE email = ${len(params)}
        """ 

        logging.info(f"Executing SQL: {sql}")
        logging.info(f"With params: {params}")

        async with self.pool.acquire() as connection:
            result = await connection.execute(sql, *params)
            if result == "UPDATE 0":
                raise asyncpg.exceptions.NoDataFoundError("User not found.")
        return result


                
    async def remove_otp_verify(self, email):
        if not self.pool:
            raise Exception("Database pool is not initialized")
        async with self.pool.acquire() as connection:
            await connection.execute(
                """
                UPDATE users SET otp = NULL WHERE email = $1
                """,
                email,
            )

    async def insert_otp(self, email, otp):
        if not self.pool:
            raise Exception("Database pool is not initialized")
        async with self.pool.acquire() as connection:
            emails = await connection.fetchval(
                """
                SELECT email FROM login WHERE email = $1
                """,
                email
            )

            if emails == email:
                await connection.execute(
                    """
                    UPDATE login SET otp = $1 WHERE email = $2
                    """,
                    otp, email
                )
            else:
                await connection.execute(
                    """
                    INSERT INTO login (email, otp)
                    VALUES ($1, $2)
                    """,
                    email, otp
                )

    async def save_user(self, name, phone, email, address):
        if not self.pool:
            raise Exception("Database pool is not initialized")
        async with self.pool.acquire() as connection:
                await connection.execute(
                    """
                    UPDATE users SET name = $1, phone = $2, address = $4 WHERE email = $3
                    """,
                    name, phone, email, address
                )   
                return {"Userdata Saved"}
        
    
    async def check_user(self, phone, email):
        if not self.pool:
            raise Exception("Database pool is not initialized")
        async with self.pool.acquire() as connection:
            existing_record = await connection.fetch(
                """
                SELECT * FROM users WHERE phone = $1 OR email = $2
                """,
                phone, email
            )
            
            return existing_record


    async def get_otp(self, email):
        if not self.pool:
            raise Exception("Database pool is not initialized")
        async with self.pool.acquire() as connection:
            result = await connection.fetchval(
                """
                SELECT otp FROM login WHERE email = $1
                """,
                email,
            )
            return result


    async def insert_session(self, email, session, expiry, otp, id):
        if not self.pool:
            raise Exception("Database pool is not initialized")
       
        async with self.pool.acquire() as connection:
 
            emails = await connection.fetchval(
                """
                SELECT email FROM users WHERE email = $1
                """,
                email
            )
            if email == emails:
                await connection.execute(
                    """
                    UPDATE users SET session = $1, expiry = $2, otp = $4, id = $5 WHERE email = $3
                    """,
                    session, expiry, email, otp, id
                )
            else:
                await connection.execute(
                    """
                    INSERT INTO users (session, expiry, email, otp, id)
                    VALUES ($1, $2, $3, $4, $5)
                    """,
                    session, expiry, email, otp, id
                )


    async def add_otp(self, otp):
        if not self.pool:
            raise Exception("Database pool is not initialized")
        async with self.pool.acquire() as connection:
            otp = await connection.fetchrow(
                """
                SELECT otp FROM login
                """
            )

            await connection.fetchrow(
                """
                UPDATE users SET otp = $1
                """,
                otp
            )


    async def get_id(self, email):
        if not self.pool:
            raise Exception("Database pool is not initialized")
        async with self.pool.acquire() as connection:
            id = await connection.fetchrow(
                """
                SELECT id FROM users WHERE email = $1
                """,
                email
            )
        return id