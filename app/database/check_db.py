import aiosqlite
import asyncio

async def check():
    async with aiosqlite.connect("database.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            for r in rows:
                print(r)

asyncio.run(check())
