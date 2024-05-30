from sqlalchemy import MetaData, Integer, Table, Column, Identity, String, Boolean

metadata = MetaData()

pc_station = Table(
    'pc_station',
           metadata,
    Column('id', Integer, Identity(start=1000, always=True), primary_key=True),
    Column('name', String(255), nullable=False),
    Column("is_working", Boolean, default=True),
           )


