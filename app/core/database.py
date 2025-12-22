from sqlalchemy import crreate_engine , URL
from sqlalchemy.orm import sessionmaker , declarative_base

from .config import settings


DATABASE_URL = URL.create(
    drivername='postgresql+ psycopg2',
    host=settings.db_host , 
    port=settings.db_port,
    user=settings.db_user,
    password=settings.db_pass,
    database=settings.db_name
)
engine = crreate_engine(url=DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)