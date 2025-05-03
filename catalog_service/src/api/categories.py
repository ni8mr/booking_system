from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from pydantic import BaseModel
from src.models.catalog import get_db
from src.services.catalog_service import CatalogService
from src.utils.auth import verify_jwt_token, User

router = APIRouter()

class CategoryCreate(BaseModel):
    name: str

class CategoryResponse(BaseModel):
    id: UUID
    name: str

async def get_current_admin(token: str = Depends(verify_jwt_token)) -> User:
    user = verify_jwt_token(token)
    if not user or user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user

@router.get("/", response_model=List[CategoryResponse])
async def list_categories(db: Session = Depends(get_db)):
    catalog_service = CatalogService(db)
    return catalog_service.list_categories()

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(category: CategoryCreate, user: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    catalog_service = CatalogService(db)
    return catalog_service.create_category(category.name)