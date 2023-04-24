from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from config import settings


url = URL.create(
    drivername=settings.db_drivername,
    username=settings.postgres_user,
    password=settings.postgres_password,
    host=settings.db_host,
    database=settings.db_name,
)

engine = create_engine(url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
