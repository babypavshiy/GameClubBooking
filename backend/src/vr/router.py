from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.database import get_async_session
from backend.src.vr.models import vr_station
from backend.src.stations_schemas import StationCreate, StationUpdate


router = APIRouter(
    prefix="/vr_stations",
    tags=["vr_stations"],
)


@router.get("/")
async def get_all_vr_stations(
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    """
    Get all VR stations
    """
    try:
        query = select(vr_station)
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
async def get_vr_station(
        station_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> dict:
    """
    Get VR station by ID
    """
    try:
        query = select(vr_station).where(vr_station.c.id == station_id)
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
async def create_vr_station(
        station_create = Depends(StationCreate),
        session: AsyncSession = Depends(get_async_session),
) -> dict:
    """
    Create new VR station
    """
    try:
        stmt = insert(vr_station).values(**station_create.dict())
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
async def update_vr_station(
        station_id: int,
        station_update = Depends(StationUpdate),
        session: AsyncSession = Depends(get_async_session),
) -> dict:
    """
    Update VR station by ID
    """
    try:
        station_update = station_update.dict()
        query = select(vr_station).where(vr_station.c.id == station_id)
        result = await session.execute(query)
        data = [dict(row) for row in result.mappings().all()][0]
        for key, value in station_update.items():
            if station_update[key] is None:
                station_update[key] = data[key]
        stmt = (
            update(vr_station)
            .where(vr_station.c.id == station_id)
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
async def delete_vr_station(
        station_id: int,
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    """
    Delete VR station by ID
    """
    try:
        stmt = delete(vr_station).where(vr_station.c.id == station_id)
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
