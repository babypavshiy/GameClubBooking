from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.database import get_async_session
from backend.src.reservations.models import reservation
from backend.src.pc.models import pc_station
from backend.src.ps.models import ps_station
from backend.src.vr.models import vr_station
from backend.src.reservations.schemas import ReservationCreate, ReservationUpdate

router = APIRouter(
    prefix="/reservations",
    tags=["reservations"],
)


async def does_station_exist(
    station_id: int,
    session: AsyncSession  = Depends(get_async_session),
) -> bool:
    """
    Checks if the given station exists in any of the database tables:
    pc_station, ps_station, vr_station
    """
    for station in [pc_station, ps_station, vr_station]:
        query = select(station).where(station.c.id == station_id)
        result = await session.execute(query)
        data = [dict(row) for row in result.mappings().all()]
        if len(data) != 0:
            return True
    return False


@router.get("/")
async def get_all_reservations(
        session: AsyncSession = Depends(get_async_session),
) -> dict:
    """
    Get all reservations
    """
    try:
        query = select(reservation)
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


@router.post("/")
async def create_reservation(
        new_reservation: ReservationCreate = Depends(ReservationCreate),
        session: AsyncSession = Depends(get_async_session),
) -> dict:
    """
    Create a new reservation
    """
    try:
        new_reservation = new_reservation.dict()
        if await does_station_exist(new_reservation["station_id"], session):
            stmt = insert(reservation).values(new_reservation)
            await session.execute(stmt)
            await session.commit()
            return {
                "status": "ok",
                "data": new_reservation,
            }
        return {
            "status": "error",
            "data": "station with this id does not exist",
        }
    except Exception as e:
        return {
            "status": "error",
            "data": str(e),
        }


@router.get("/{reservation_id}")
async def get_reservation(
        reservation_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> dict:
    """
    Get a reservation by id
    """
    try:
        query = select(reservation).where(reservation.c.id == reservation_id)
        result = await session.execute(query)
        data  =  [dict(row) for row in result.mappings().all()][0]
        return  {
            "status": "ok",
            "data": data,
        }
    except Exception as e:
        return {
            "status": "error",
            "data": str(e),
        }


@router.patch("/{reservation_id}")
async def update_reservation(
        reservation_id: int,
        updated_reservation: ReservationUpdate = Depends(ReservationUpdate),
        session: AsyncSession = Depends(get_async_session),
) -> dict:
    """
    Update a reservation by id
    """
    try:
        updated_reservation = updated_reservation.dict()
        if await does_station_exist(updated_reservation["station_id"], session):
            query = select(reservation).where(reservation.c.id == reservation_id)
            result = await session.execute(query)
            data = [dict(row) for row in result.mappings().all()][0]
            for key, value in updated_reservation.items():
                if updated_reservation[key] is None:
                    updated_reservation[key] = data[key]
            stmt = (update(reservation)
                    .where(reservation.c.id == reservation_id)
                    .values(updated_reservation))
            await session.execute(stmt)
            await session.commit()
            return {
                "status": "ok",
                "data": updated_reservation,
            }
        return  {
            "status": "error",
            "data": "station with this id does not exist",
        }
    except Exception as e:
        return {
            "status": "error",
            "data": str(e),
        }


@router.delete("/{reservation_id}")
async def delete_reservation(
        reservation_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> dict:
    """
    Delete a reservation by id
    """
    try:
        stmt  = delete(reservation).where(reservation.c.id  == reservation_id)
        await session.execute(stmt)
        await session.commit()
        return  {
            "status": "ok",
            "data": None,
        }
    except Exception as e:
        return {
            "status": "error",
            "data": str(e),
        }
