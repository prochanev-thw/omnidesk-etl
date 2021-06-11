from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    MetaData,
    Table,
    BigInteger
)

metadata = MetaData()

lables = Table(
    'lables',
    metadata,
    Column('label_id', BigInteger().with_variant(Integer, "sqlite"), nullable=False),
    Column('label_title', String(256), nullable=False),
)

cases = Table(
    'cases',
    metadata,
    Column('case_id', Integer, primary_key=True),
    Column('case_number', Integer),
    Column('user_id', Integer),
    Column('staff_id', Integer),
    Column('status', String(256)),
    Column('priority', String(256)),
    Column('channel', String(256)),
    Column('deleted', Boolean),
    Column('spam', Boolean),
    Column('created_at', Date),
    Column('updated_at', Date, nullable=True),
    Column('parent_case_id', Integer, nullable=True),
    Column('closing_speed', Integer, nullable=True)
)

case_label = Table(
    'case_label',
    metadata,
    Column("id", BigInteger().with_variant(Integer, "sqlite"), primary_key=True),
    Column('case_id', Integer),
    Column('label_id', Integer)
)
