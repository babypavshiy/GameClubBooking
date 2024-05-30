from datetime import datetime
from sqlalchemy import MetaData, Integer, TIMESTAMP, ForeignKey, Table, Column, Identity
from backend.src.auth.models import user


metadata = MetaData()

reservation = Table(
    'reservation',
    metadata,
    Column('id', Integer, Identity(start=1, always=True), primary_key=True),
    Column('station_id', Integer, nullable=False),
    Column('status', Integer, nullable=False),
    Column('user_id', ForeignKey(user.c.id)),
    Column('staff_id', Integer, ForeignKey(user.c.id)),
    Column('date', TIMESTAMP, nullable=False),
    Column('start_time', TIMESTAMP, nullable=False),
    Column('end_time', TIMESTAMP, nullable=False),
    Column('created_at', TIMESTAMP, default=datetime.utcnow),
)
