from sqlalchemy import MetaData
from sqlalchemy import create_engine

engine = create_engine('sqlite:///Database.db')

metadata = MetaData()
metadata.reflect(bind=engine)
tables = metadata.tables.keys()

with engine.begin() as connection:
    for table in reversed(metadata.sorted_tables):
        connection.execute(table.delete())