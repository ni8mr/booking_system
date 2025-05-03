from fastapi import FastAPI
from pydantic import BaseModel
from uuid import UUID, uuid4

app = FastAPI(title="Mock Order API", version="1.0.0")

class OrderCreate(BaseModel):
    cart_id: UUID
    total_price: float

class OrderResponse(BaseModel):
    order_id: UUID

@app.post("/orders", response_model=OrderResponse, status_code=201)
async def create_order(order: OrderCreate):
    return {"order_id": uuid4()}