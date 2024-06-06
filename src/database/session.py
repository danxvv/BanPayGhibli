from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src.config import settings
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True) # type: ignore
TestEngine = create_engine(TEST_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TestEngine)

Base = declarative_base()