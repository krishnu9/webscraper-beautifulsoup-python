from sqlalchemy import create_engine, MetaData

DATABASE_URL = "postgresql://postgres:mysecretpassword@localhost:5432/dentalapidb"

engine = create_engine(DATABASE_URL)
metadata = MetaData()


