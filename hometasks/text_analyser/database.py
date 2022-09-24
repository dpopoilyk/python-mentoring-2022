from sqlalchemy import create_engine, MetaData, Table, Column, DateTime, String


def create_sqlite_engine(db_file):
    url = f'sqlite:///{db_file}'
    engine = create_engine(url)

    return engine


logs_table = Table(
    "logs", MetaData(),
    Column('uid', String, primary_key=True),
    Column('timestamp', DateTime),
    Column('type_of_resource', String),
    Column('name_of_resource', String),
    Column('message', String)
)

