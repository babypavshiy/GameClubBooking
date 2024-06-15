from sqlalchemy import insert
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from src.database import DATABASE_URL
from src.users.models import role

from src.stations.models import station

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
     "name": "user",
     "permissions": {
         "edit_all": False,
         "edit_reservations": False,
     }},
]

stations_data = [
    {
        "name": "Игровой ПК 1",
        "type": "PC",
        "is_working": True,
    },
{
        "name": "Игровой ПК 2",
        "type": "PC",
        "is_working": True,
    },
{
        "name": "Игровой ПК 3",
        "type": "PC",
        "is_working": True,
    },
{
        "name": "PlayStation 1",
        "type": "PS",
        "is_working": True,
    },
{
        "name": "PlayStation 2",
        "type": "PS",
        "is_working": True,
    },
{
        "name": "PlayStation 3",
        "type": "PS",
        "is_working": True,
    },
{
        "name": "VR-станция 1",
        "type": "VR",
        "is_working": True,
    },
{
        "name": "VR-станция 2",
        "type": "VR",
        "is_working": True,
    },
{
        "name": "VR-станция 3",
        "type": "VR",
        "is_working": True,
    }
]

async def seed_data():
    engine = create_async_engine(DATABASE_URL)
    async with AsyncSession(engine) as session:
        async with session.begin():
            for item in data:
                stmt = insert(role).values(**item)
                await session.execute(stmt)
            for item in stations_data:
                stmt = insert(station).values(**item)
                await session.execute(stmt)
            await session.commit()