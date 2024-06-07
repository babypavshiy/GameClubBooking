from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend
from fastapi_users import FastAPIUsers
from backend.src.database import get_async_session
from fastapi import Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.users.models import User
from backend.src.users.manager import UserManager
from backend.src.config import JWT_SECRET

cookie_transport = CookieTransport(
    cookie_name="auth_token",
    cookie_max_age=3600,
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=JWT_SECRET,
        lifetime_seconds=3600,
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy
)


async def get_user_db(session: AsyncSession = Depends(get_async_session)) -> SQLAlchemyUserDatabase:
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

