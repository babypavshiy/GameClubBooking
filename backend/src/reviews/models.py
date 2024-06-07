from datetime import datetime
from sqlalchemy import MetaData, Integer, Table, Column, Identity, String, ForeignKey, TIMESTAMP
from backend.src.users.models import user

metadata = MetaData()

review = Table(
    'review',
    metadata,
    Column('id', Integer, Identity(start=1, always=True), primary_key=True),
    Column('user_id', ForeignKey(user.c.id), nullable=False),
    Column('station_id', Integer, nullable=False),
    Column('rating', Integer, nullable=False),
    Column('comment', String, nullable=True),
    Column('created_at', TIMESTAMP, default=datetime.utcnow),
)
