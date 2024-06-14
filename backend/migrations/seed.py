from sqlalchemy import insert
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from src.database import DATABASE_URL
from src.users.models import role

data = [
    {"id": 0,
     "name": "admin",
     "permissions": {
         "edit_all": True,
         "edit_reservations": True,
     }},
    {"id": 1,
     "name": "staff",
     "permissions": {
         "edit_all": False,
         "edit_reservations": True,
     }},
    {"id": 2,
     "name": "admin",
     "permissions": {
         "edit_all": False,
         "edit_reservations": False,
     }},
]

async def seed_data():
    engine = create_async_engine(DATABASE_URL)
    async with AsyncSession(engine) as session:
        async with session.begin():
            for item in data:
                stmt = insert(role).values(**item)
                await session.execute(stmt)
            await session.commit()