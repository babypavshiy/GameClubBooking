from datetime import datetime, timedelta, time
from typing import List, Dict, Set

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, insert, update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database import get_async_session
from backend.src.stations.models import station
from backend.src.reservations.models import reservation
from backend.src.reservations.schemas import ReservationCreate, ReservationUpdate
from backend.src.users.models import user
from backend.src.users.utils import current_verified_user, is_admin, is_staff

router = APIRouter(
    prefix="/reservations",
    tags=["reservations"],
)

async def does_station_exist(station_id: int, session: AsyncSession) -> bool:
    """
    Checks if the given station exists
    """
    query = select(station).where(station.c.id == station_id)
    result = await session.execute(query)
    return bool(result.mappings().all())

async def is_time_slot_available(station_id: int, start_time: datetime, end_time: datetime,
                                 session: AsyncSession) -> bool:
    """
    Checks if the given time slot is available for the station
    """
    query = select(reservation).where(
        and_(
            reservation.c.station_id == station_id,
            reservation.c.start_time < end_time,
            reservation.c.end_time > start_time
        )
    )
    result = await session.execute(query)
    return not result.mappings().all()

@router.get("/")
async def get_all_reservations(session: AsyncSession = Depends(get_async_session),
                               current_user: user = Depends(current_verified_user)) -> dict:
    """
    Get all reservations
    """
    try:
        if is_admin(current_user.id, session) or is_staff(current_user.id, session):
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

def get_date_object(date_str: str) -> datetime:
    return datetime.strptime(date_str, '%Y-%m-%d')

def generate_all_slots(start_time: datetime, end_time: datetime) -> List[str]:
    all_slots = []
    current_time = start_time
    while current_time <= end_time:
        all_slots.append(current_time.time().strftime('%H:%M'))
        current_time += timedelta(hours=1)
    return all_slots

def get_occupied_slots(reservations: List[Dict[str, datetime]]) -> Set[str]:
    occupied_slots = set()
    for res in reservations:
        start = res['start_time'].strftime('%H:%M')
        end = res['end_time'].strftime('%H:%M')
        current_time = datetime.combine(res['date'], time(0, 0))
        end_time = datetime.combine(res['date'], time(23, 59, 59))
        while current_time <= end_time:
            if start <= current_time.time().strftime('%H:%M') < end:
                occupied_slots.add(current_time.time().strftime('%H:%M'))
            current_time += timedelta(hours=1)
    return occupied_slots

async def get_available_slots(date: str, session: AsyncSession) -> List[str]:
    date_obj = get_date_object(date)
    start_time = datetime.combine(date_obj, time(9, 0))
    end_time = datetime.combine(date_obj, time(21, 59, 59))

    query = (
        select(reservation)
        .where(reservation.c.date == date_obj)
        .order_by(reservation.c.start_time)
    )
    result = await session.execute(query)
    reservations = [dict(row) for row in result.mappings().all()]

    all_slots = generate_all_slots(start_time, end_time)
    occupied_slots = get_occupied_slots(reservations)
    available_slots = [slot for slot in all_slots if slot not in occupied_slots]

    return available_slots

@router.get("/availability/")
async def get_availability(
        date: str = Query(..., description="Дата в формате YYYY-MM-DD"),
        session: AsyncSession = Depends(get_async_session),
) -> dict:
    try:
        available_slots = await get_available_slots(date, session)
        return {
            "status": "ok",
            "data": available_slots
        }
    except Exception as e:
        return {
            "status": "error",
            "data": str(e)
        }


@router.post("/")
async def create_reservation(new_reservation: ReservationCreate,
                             session: AsyncSession = Depends(get_async_session)) -> dict:
    """
    Create a new reservation
    """
    try:
        new_reservation.created_at = datetime.utcnow()

        new_reservation_dict = new_reservation.dict()
        if not await does_station_exist(new_reservation_dict["station_id"], session):
            raise HTTPException(status_code=400, detail="Station with this ID does not exist")
        if not await is_time_slot_available(new_reservation_dict["station_id"], new_reservation_dict["start_time"],
                                            new_reservation_dict["end_time"], session):
            raise HTTPException(status_code=400, detail="Time slot is not available")
        stmt = insert(reservation).values(new_reservation_dict)
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "ok",
            "data": new_reservation_dict,
        }
    except Exception as e:
        return {
            "status": "error",
            "data": str(e),
        }

@router.get("/{reservation_id}")
async def get_reservation(reservation_id: int, session: AsyncSession = Depends(get_async_session)) -> dict:
    """
    Get a reservation by ID
    """
    try:
        query = select(reservation).where(reservation.c.id == reservation_id)
        result = await session.execute(query)
        data = result.mappings().all()
        if not data:
            raise HTTPException(status_code=404, detail="Reservation not found")
        return {
            "status": "ok",
            "data": dict(data[0]),
        }
    except Exception as e:
        return {
            "status": "error",
            "data": str(e),
        }


@router.patch("/{reservation_id}")
async def update_reservation(reservation_id: int, updated_reservation: ReservationUpdate,
                             session: AsyncSession = Depends(get_async_session)) -> dict:
    """
    Update a reservation by ID
    """
    try:
        existing_reservation = await get_reservation(reservation_id, session)
        update_data = updated_reservation.dict(exclude_unset=True)
        if "station_id" in update_data and not await does_station_exist(update_data["station_id"], session):
            raise HTTPException(status_code=400, detail="Station with this ID does not exist")
        if not await is_time_slot_available(update_data.get("station_id", existing_reservation["data"]["station_id"]),
                                            update_data.get("start_time", existing_reservation["data"]["start_time"]),
                                            update_data.get("end_time", existing_reservation["data"]["end_time"]),
                                            session):
            raise HTTPException(status_code=400, detail="Time slot is not available")

        updated_data = {**existing_reservation["data"], **update_data}
        stmt = update(reservation).where(reservation.c.id == reservation_id).values(**updated_data)
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "ok",
            "data": updated_data,
        }
    except HTTPException as e:
        return {
            "status": "error",
            "data": str(e.detail),
        }
    except Exception as e:
        return {
            "status": "error",
            "data": str(e),
        }

@router.delete("/{reservation_id}")
async def delete_reservation(reservation_id: int, session: AsyncSession = Depends(get_async_session)) -> dict:
    """
    Delete a reservation by ID
    """
    try:
        await get_reservation(reservation_id, session)
        stmt = delete(reservation).where(reservation.c.id == reservation_id)
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "ok",
            "data": None,
        }
    except HTTPException as e:
        return {
            "status": "error",
            "data": str(e.detail),
        }
    except Exception as e:
        return {
            "status": "error",
            "data": str(e),
        }

