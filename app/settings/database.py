from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base

def get_sqlite_url():
    return "sqlite:////code/my_database.db"

def get_engine():
    return create_engine(get_sqlite_url(), echo=DEBUG)


engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
