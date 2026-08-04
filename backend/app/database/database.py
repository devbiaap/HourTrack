import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

DATA_BASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATA_BASE_URL)

SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)

class Base(DeclarativeBase):
    pass

