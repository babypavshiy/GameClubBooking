import json
import uuid
from datetime import datetime

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from yookassa import Payment, Configuration

from src.config import PAYMENTS_SECRET_KEY, PAYMENTS_ACCOUNT
from src.reservations.models import payment

Configuration.account_id = PAYMENTS_ACCOUNT
Configuration.secret_key = PAYMENTS_SECRET_KEY


def get_timestamp(dt: str):
    return datetime.fromisoformat(dt[:-1])

async def add_payment(
        payment_dict: dict,
        user_id: int,
        reservation_id: int,
        session: AsyncSession
):
    new_payment = {
        "id": payment_dict["id"],
        "status": payment_dict["status"],
        "currency": payment_dict['amount']["currency"],
        "amount": float(payment_dict['amount']["value"]),
        "by_user": user_id,
        "reservation": reservation_id,
        "created_at": get_timestamp(payment_dict["created_at"]),
    }
    stmt = insert(payment).values(new_payment)
    await session.execute(stmt)
    await session.commit()


async def get_payment_data(payment_id: str):
    return json.loads(Payment.find_one(payment_id).json())


async def create_payment(
        amount: float,
        user_id: int,
        reservation_id: int,
        session: AsyncSession
):
    idempotency_key = uuid.uuid4()
    new_payment = Payment.create({
        "amount": {
            "value": str(amount),
            "currency": "RUB",
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "example.com",
        },
        "capture": True,
    },
        idempotency_key=idempotency_key,
    )
    new_payment_data = await get_payment_data(new_payment.id)
    await add_payment(new_payment_data, user_id, reservation_id, session)
    return new_payment.confirmation.confirmation_url
