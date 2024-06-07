from sqlalchemy.ext.asyncio import AsyncSession, select
from backend.src.users.models import user
from backend.src.users.config import fastapi_users

current_user = fastapi_users.current_user()
current_active_user = fastapi_users.current_user(active=True)
current_verified_user = fastapi_users.current_user(verified=True)

async def is_admin(user_id: int, session: AsyncSession) -> bool:
    query = select(user).where(user == user_id)
    result = await session.execute(query)
    user_data = dict(result.mappings().one())
    return user_data['role_id'] == 0


async def is_staff(user_id: int, session: AsyncSession) -> bool:
    query = select(user).where(user == user_id)
    result = await session.execute(query)
    user_data = dict(result.mappings().one())
    return user_data['role_id'] == 1