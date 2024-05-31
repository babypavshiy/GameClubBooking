from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.database import get_async_session
from backend.src.ps.models import ps_station
from backend.src.stations_schemas import StationCreate, StationUpdate


router = APIRouter(
    prefix="/ps_stations",
    tags=["ps_stations"],
)


@router.get("/")
async def get_all_ps_stations(
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    """
    Get all ps stations
    """
    try:
        query = select(ps_station)
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
async def get_ps_station(
        station_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> dict:
    """
    Get a specific ps station by id
    """
    try:
        query = select(ps_station).where(ps_station.c.id == station_id)
        result = await session.execute(query)
        data = [dict(row) for row in result.mappings().all()][0]
        return {
            "status": "ok",
            "data": data,
        }
    except Exception as e:
        return {
            "status": "error",
            "data": str(e),
        }


@router.post("/")
async def create_ps_station(
        station_create = Depends(StationCreate),
        session: AsyncSession = Depends(get_async_session),
) -> dict:
    """
    Create a new ps station
    """
    try:
        stmt = insert(ps_station).values(**station_create.dict())
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "ok",
            "data": station_create.dict(),
                }
    except Exception as e:
        return {
            "status": "error",
            "data": str(e),
        }


@router.patch("/{station_id}")
async def update_ps_station(
        station_id: int,
        station_update = Depends(StationUpdate),
        session: AsyncSession = Depends(get_async_session),
) -> dict:
    """
    Update a ps station by id
    """
    try:
        station_update = station_update.dict()
        query = select(ps_station).where(ps_station.c.id == station_id)
        result = await session.execute(query)
        data = [dict(row) for row in result.mappings().all()][0]
        for key, value in station_update.items():
            if station_update[key] is None:
                station_update[key] = data[key]
        stmt = (
            update(ps_station)
            .where(ps_station.c.id == station_id)
            .values(**station_update)
        )
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "ok",
            "data": station_update,
                }
    except Exception as e:
        return {
            "status": "error",
            "data": str(e),
        }


@router.delete("/{station_id}")
async def delete_ps_station(
        station_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    """
    Delete a specific ps station by id
    """
    try:
        stmt = delete(ps_station).where(ps_station.c.id == station_id)
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "ok",
            "data": None,
        }
    except Exception as e:
        return {
            "status": "error",
            "data": str(e),
        }
