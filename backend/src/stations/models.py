from sqlalchemy import Column, String, Table, MetaData, Integer, Identity, Boolean

metadata = MetaData()

station = Table(
    'station',
    metadata,
    Column('id', Integer, Identity(start=1000, always=True), primary_key=True),
    Column('name', String(255), nullable=False),
    Column('type', String(50), nullable=False),
    Column("is_working", Boolean, default=True),
)