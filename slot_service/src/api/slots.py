from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from pydantic import BaseModel
from src.models.slot import get_db
from src.services.slot_service import SlotService
from src.utils.auth import verify_jwt_token, User

router = APIRouter()

class SlotCreate(BaseModel):
    partner_id: UUID
    service_id: UUID
    slot_time: str  # ISO 8601, e.g., "2025-05-03T10:00:00Z"
    is_available: bool

class SlotResponse(BaseModel):
    id: UUID
    partner_id: UUID
    service_id: UUID
    slot_time: str
    is_available: bool

async def get_current_admin(token: str = Depends(verify_jwt_token)) -> User:
    user = verify_jwt_token(token)
    if not user or user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user

@router.get("/{partner_id}/{service_id}", response_model=List[SlotResponse])
async def get_slots(partner_id: UUID, service_id: UUID, db: Session = Depends(get_db)):
    slot_service = SlotService(db)
    return slot_service.get_slots(partner_id, service_id)

@router.post("/", response_model=SlotResponse, status_code=status.HTTP_201_CREATED)
async def create_slot(slot: SlotCreate, user: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    slot_service = SlotService(db)
    return slot_service.create_slot(
        slot.partner_id,
        slot.service_id,
        slot.slot_time,
        slot.is_available
    )