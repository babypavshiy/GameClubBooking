from fastapi import FastAPI
from src.stations.router import router as station_router
from fastapi_users import FastAPIUsers
from src.users.models import User
from sqlalchemy.dialects.postgresql import UUID
from src.users.config import auth_backend, get_user_manager
from src.users.schemas import UserCreate, UserRead, UserUpdate
from src.reservations.router import router as reservation_router
from src.reviews.router import router as review_router
from fastapi.middleware.cors import CORSMiddleware

"""
Main FastAPI app
and included routers
"""
app = FastAPI()
app.include_router(station_router)
app.include_router(reservation_router)
app.include_router(review_router)


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://0.0.0.0"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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