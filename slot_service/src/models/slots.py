from sqlalchemy import Column, ForeignKey, Boolean, DateTime, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
from src.config.settings import settings

Base = declarative_base()

class PartnerSlot(Base):
    __tablename__ = "partner_slot"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    partner_id = Column(UUID(as_uuid=True), nullable=False)
    service_id = Column(UUID(as_uuid=True), nullable=False)
    slot_time = Column(DateTime, nullable=False)
    is_available = Column(Boolean, nullable=False)

engine = create_engine(settings.database_url)
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()