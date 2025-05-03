from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_session_factory(database_url: str) -> sessionmaker:
    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal

def get_db(SessionLocal: sessionmaker):
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()