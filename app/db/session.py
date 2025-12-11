from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

db = os.getenv("db", "postgresql://mohit:mohit123@localhost:5432/gatekeeper")
engine = create_engine(db)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
