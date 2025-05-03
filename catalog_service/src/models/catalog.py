from sqlalchemy import Column, ForeignKey, Integer, Float, String, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import uuid
from src.config.settings import settings

Base = declarative_base()

class Category(Base):
    __tablename__ = "category"
    __table_args__ = {"schema": "catalog"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    subcategories = relationship("Subcategory", back_populates="category", cascade="all, delete-orphan")

class Subcategory(Base):
    __tablename__ = "subcategory"
    __table_args__ = {"schema": "catalog"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("catalog.category.id"), nullable=False)
    category = relationship("Category", back_populates="subcategories")
    services = relationship("Service", back_populates="subcategory", cascade="all, delete-orphan")

class Service(Base):
    __tablename__ = "service"
    __table_args__ = {"schema": "catalog"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    subcategory_id = Column(UUID(as_uuid=True), ForeignKey("catalog.subcategory.id"), nullable=False)
    price = Column(Float, nullable=False)
    duration = Column(Integer, nullable=False)
    subcategory = relationship("Subcategory", back_populates="services")

engine = create_engine(settings.database_url)
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()