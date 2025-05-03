from typing import Dict, Any
from uuid import UUID
from pydantic import BaseModel
from fastapi import HTTPException

class MockSlotResponse(BaseModel):
    id: UUID
    partner_id: UUID
    service_id: UUID
    slot_time: str
    is_available: bool

class MockOrderResponse(BaseModel):
    order_id: UUID

class MockHttpClient:
    def __init__(self):
        self.responses = {
            "slots": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440007",
                    "partner_id": "550e8400-e29b-41d4-a716-446655440008",
                    "service_id": "550e8400-e29b-41d4-a716-446655440005",
                    "slot_time": "2025-05-04T10:00:00Z",
                    "is_available": True
                }
            ],
            "orders": {
                "order_id": "550e8400-e29b-41d4-a716-446655440009"
            }
        }

    async def get(self, url: str) -> Dict[str, Any]:
        if "slots" in url:
            return {"status_code": 200, "json": lambda: self.responses["slots"]}
        raise HTTPException(status_code=404, detail="Mock endpoint not found")

    async def post(self, url: str, json: Dict[str, Any]) -> Dict[str, Any]:
        if "orders" in url:
            return {"status_code": 201, "json": lambda: self.responses["orders"]}
        raise HTTPException(status_code=404, detail="Mock endpoint not found")