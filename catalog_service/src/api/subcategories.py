from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from pydantic import BaseModel
from src.models.catalog import get_db
from src.services.catalog_services import CatalogService
from src.utils.auth import verify_jwt_token, User

router = APIRouter()

class SubcategoryCreate(BaseModel):
    name: str
    category_id: UUID

class SubcategoryResponse(BaseModel):
    id: UUID
    name: str
    category_id: UUID

async def get_current_admin(token: str = Depends(verify_jwt_token)) -> User:
    user = verify_jwt_token(token)
    if not user or user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user

@router.get("/{category_id}/subcategories", response_model=List[SubcategoryResponse])
async def list_subcategories(category_id: UUID, db: Session = Depends(get_db)):
    catalog_service = CatalogService(db)
    return catalog_service.list_subcategories(category_id)

@router.post("/", response_model=SubcategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_subcategory(subcategory: SubcategoryCreate, user: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    catalog_service = CatalogService(db)
    return catalog_service.create_subcategory(subcategory.name, subcategory.category_id)