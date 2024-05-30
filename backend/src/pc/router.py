from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.database import get_async_session
from backend.src.pc.models import pc_station
from backend.src.stations_schemas import StationCreate


router = APIRouter(
    prefix="/pc_stations",
    tags=["pc_stations"],
)


@router.get("/")
async def get_all_pc_stations(
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    try:
        query = select(pc_station)
        result = await session.execute(query)
        data = [dict(row) for row in result.mappings().all()]
        return {
            "status": "ok",
            "data": data,
        }
    except Exception as e:
        return {
            "status": "error",
            "data": str(e),
        }


@router.get("/{station_id}")
async def get_pc_station(
        station_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> dict:
    try:
        query = select(pc_station).where(pc_station.c.id == station_id)
        result = await session.execute(query)
        data = [dict(row) for row in result.mappings().all()][0]
        return {
            "status": "ok",
            "data": data,
        }
    except Exception as e:
        return {
            "status": "error",
            "data": None,
        }


@router.post("/")
async def create_pc_station(
        station_create = Depends(StationCreate),
        session: AsyncSession = Depends(get_async_session),
) -> dict:
    try:
        stmt = insert(pc_station).values(**station_create.dict())
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "ok",
            "data": station_create.dict(),
                }
    except Exception as e:
        return {
            "status": "error",
            "data": None,
        }


@router.patch("/{station_id}")
async def update_pc_station(
        station_id: int,
        station_update = Depends(StationCreate),
        session: AsyncSession = Depends(get_async_session),
) -> dict:
    try:
        stmt = (
            update(pc_station)
            .where(pc_station.c.id == station_id)
            .values(**station_update.dict())
        )
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "ok",
            "data": station_update.dict(),
                }
    except Exception as e:
        return {
            "status": "error",
            "data": None,
        }


@router.delete("/{station_id}")
async def delete_pc_station(
        station_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    try:
        stmt = delete(pc_station).where(pc_station.c.id == station_id)
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "ok",
            "data": None,
        }
    except Exception as e:
        return {
            "status": "error",
            "data": None,
        }
