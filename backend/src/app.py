from fastapi import FastAPI
from backend.src.stations.router import router as station_router
from fastapi_users import FastAPIUsers
from backend.src.users.models import User
from sqlalchemy.dialects.postgresql import UUID
from backend.src.users.config import auth_backend, get_user_manager
from backend.src.users.schemas import UserCreate, UserRead, UserUpdate
from backend.src.reservations.router import router as reservation_router
from backend.src.reviews.router import router as review_router

"""
Main FastAPI app
and included routers
"""
app = FastAPI()
app.include_router(station_router)
app.include_router(reservation_router)
app.include_router(review_router)


fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend],
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/users",
    tags=["users"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/users",
    tags=["users"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/users",
    tags=["users"],
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/users",
    tags=["users"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)