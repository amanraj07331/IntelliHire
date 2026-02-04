from datetime import datetime, timedelta
from db_pool import init_pool

async def is_cookie_expired(cookie_id: str) -> bool:
    async with init_pool() as pool:
        async with pool.acquire() as connection:
            result = await connection.fetchrow(
                """
                SELECT expiry FROM users WHERE session = $1
                """,
                cookie_id,
            )
            if result:
                expiry_time = result[0]
                now = datetime.now() + timedelta()
                now_unix = int(now.timestamp())
                return now_unix > expiry_time
            else:
                return True