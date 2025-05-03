from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from pydantic import BaseModel
from src.models.catalog import get_db
from src.services.catalog_service import CatalogService
from src.utils.auth import verify_jwt_token, User

router = APIRouter()

class ServiceCreate(BaseModel):
    name: str
    subcategory_id: UUID
    price: float
    duration: int

class ServiceResponse(BaseModel):
    id: UUID
    name: str
    subcategory_id: UUID
    price: float
    duration: int

async def get_current_admin(token: str = Depends(verify_jwt_token)) -> User:
    user = verify_jwt_token(token)
    if not user or user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user

@router.get("/{subcategory_id}/services", response_model=List[ServiceResponse])
async def list_services(subcategory_id: UUID, db: Session = Depends(get_db)):
    catalog_service = CatalogService(db)
    return catalog_service.list_services(subcategory_id)

@router.get("/{service_id}", response_model=ServiceResponse)
async def get_service(service_id: UUID, db: Session = Depends(get_db)):
    catalog_service = CatalogService(db)
    service = catalog_service.get_service(service_id)
    if not service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    return service

@router.post("/", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
async def create_service(service: ServiceCreate, user: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    catalog_service = CatalogService(db)
    return catalog_service.create_service(service.name, service.subcategory_id, service.price, service.duration)