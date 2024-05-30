from sqlalchemy import MetaData, Integer, Table, Column, Identity, String, Boolean

metadata = MetaData()

vr_station = Table(
    'vr_station',
           metadata,
           Column('id', Integer, Identity(start=3000, always=True), primary_key=True),
Column('name', String(255), nullable=False),
    Column("is_working", Boolean, default=True),
           )

