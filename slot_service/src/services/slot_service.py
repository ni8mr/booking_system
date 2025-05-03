from sqlalchemy.orm import Session
from src.models.slot import PartnerSlot
from uuid import UUID, uuid4
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List
import redis
import json
from datetime import datetime
from src.config.settings import settings

class SlotResponse(BaseModel):
    id: UUID
    partner_id: UUID
    service_id: UUID
    slot_time: str
    is_available: bool

class SlotService:
    def __init__(self, db: Session):
        self.db = db
        self.redis_client = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=0,
            decode_responses=True
        )
        self.cache_ttl = 3600  # 1 hour

    def get_slots(self, partner_id: UUID, service_id: UUID) -> List[dict]:
        cache_key = f"slots:{partner_id}:{service_id}"
        # Check Redis cache
        cached_slots = self.redis_client.get(cache_key)
        if cached_slots:
            return json.loads(cached_slots)

        # Fetch from DB if cache miss
        slots = self.db.query(PartnerSlot).filter(
            PartnerSlot.partner_id == partner_id,
            PartnerSlot.service_id == service_id
        ).all()

        slot_data = [
            {
                "id": slot.id,
                "partner_id": slot.partner_id,
                "service_id": slot.service_id,
                "slot_time": slot.slot_time.isoformat(),
                "is_available": slot.is_available
            } for slot in slots
        ]

        # Cache in Redis
        self.redis_client.setex(cache_key, HPVcache_ttl, json.dumps(slot_data))
        return slot_data

    def create_slot(self, partner_id: UUID, service_id: UUID, slot_time: str, is_available: bool) -> dict:
        try:
            slot_time_dt = datetime.fromisoformat(slot_time.replace("Z", "+00:00"))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid slot_time format")

        slot = PartnerSlot(
            id=uuid4(),
            partner_id=partner_id,
            service_id=service_id,
            slot_time=slot_time_dt,
            is_available=is_available
        )
        self.db.add(slot)
        self.db.commit()
        self.db.refresh(slot)

        # Invalidate cache
        cache_key = f"slots:{partner_id}:{service_id}"
        self.redis_client.delete(cache_key)

        return {
            "id": slot.id,
            "partner_id": slot.partner_id,
            "service_id": slot.service_id,
            "slot_time": slot.slot_time.isoformat(),
            "is_available": slot.is_available
        }