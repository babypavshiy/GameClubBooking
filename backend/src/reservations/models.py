from datetime import datetime
from sqlalchemy import MetaData, Integer, TIMESTAMP, ForeignKey, Table, Column, Identity, String, REAL
from src.users.models import user


metadata = MetaData()

reservation = Table(
    'reservation',
    metadata,
    Column('id', Integer, Identity(start=1, always=True), primary_key=True),
    Column('station_id', Integer, nullable=False),
    Column('status', Integer, nullable=False),
    Column('user_id', ForeignKey(user.c.id)),
    Column('staff_id', Integer, ForeignKey(user.c.id)),
    Column('amount', REAL, default=datetime.utcnow),
    Column('date', TIMESTAMP, nullable=False),
    Column('start_time', TIMESTAMP, nullable=False),
    Column('end_time', TIMESTAMP, nullable=False),
    Column('created_at', TIMESTAMP, default=datetime.utcnow),
)


payment = Table(
    'payment',
    metadata,
    Column("id", String(50), primary_key=True),
    Column("status", String(20), nullable=False),
    Column("currency", String(4), nullable=False),
    Column("amount", REAL, nullable=False),
    Column("by_user", Integer, ForeignKey(user.c.id), nullable=False),
    Column("reservation", Integer, ForeignKey(reservation.c.id), nullable=False),
    Column("created_at", TIMESTAMP, nullable=False),
)
