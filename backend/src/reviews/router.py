from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.reviews.models import review
from src.reviews.schemas import ReviewCreate, ReviewUpdate
from src.users.models import User
from src.users.utils import current_verified_user

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
)


@router.get("/{review_id}")
async def get_review(review_id: int, session: AsyncSession = Depends(get_async_session)) -> dict:
    """
    Get a review by ID
    """
    try:
        query = select(review).where(review.c.id == review_id)
        result = await session.execute(query)
        data = result.mappings().one()
        if not data:
            raise HTTPException(status_code=404, detail="Review not found")
        return {
            "status": "ok",
            "data": dict(data),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by_station/{station_id}")
async def get_reviews_by_station(station_id: int, session: AsyncSession = Depends(get_async_session)) -> dict:
    try:
        query = select(review).where(review.c.station_id == station_id)
        result = await session.execute(query)
        data = result.mappings().all()
        if not data:
            raise HTTPException(status_code=404, detail="Reviews not found")
        return {
            "status": "ok",
            "data": [dict(d) for d in data],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=ReviewCreate)
async def create_review(review_create: ReviewCreate,
                        current_user: User = Depends(current_verified_user),
                        session: AsyncSession = Depends(get_async_session)) -> dict:
    """
    Create a new review
    """
    try:
        review_data = review_create.dict()
        review_data["rating"] = int(review_data["rating"])
        review_data["user_id"] = current_user.id
        review_data["created_at"] = datetime.utcnow()
        stmt = insert(review).values(**review_data)
        await session.execute(stmt)
        await session.commit()
        return review_create.dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{review_id}")
async def update_review(review_id: int, updated_review: ReviewUpdate,
                        session: AsyncSession = Depends(get_async_session)) -> dict:
    """
    Update a review by ID
    """
    try:
        existing_review = await get_review(review_id, session)
        stmt = update(review).where(review.c.id == review_id).values(**updated_review.dict(exclude_unset=True))
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "ok",
            "data": {**existing_review["data"], **updated_review.dict()},
        }
    except HTTPException as e:
        return {
            "status": "error",
            "data": str(e),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{review_id}")
async def delete_review(review_id: int, session: AsyncSession = Depends(get_async_session)) -> dict:
    """
    Delete a review by ID
    """
    try:
        existing_review = await get_review(review_id, session)
        stmt = delete(review).where(review.c.id == review_id)
        await session.execute(stmt)
        await session.commit()
        return {
            "status": "ok",
            "data": existing_review["data"],
        }
    except HTTPException as e:
        return {
            "status": "error",
            "data": str(e),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
