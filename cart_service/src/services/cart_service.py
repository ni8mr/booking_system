from sqlalchemy.orm import Session
from src.models.cart import Cart, CartItem
from uuid import UUID, uuid4
import httpx
from fastapi import HTTPException
from pydantic import BaseModel
from typing import List

class CartItemCreate(BaseModel):
    service_id: UUID
    partner_id: UUID
    slot_id: UUID
    quantity: int
    unit_price: float

class CartService:
    def __init__(self, db: Session):
        self.db = db
        self.slot_service_url = "http://slot-service:8000/slots"
        self.order_api_url = "http://mock-order-api:8000/orders"

    def create_cart(self, user_id: UUID) -> dict:
        cart = Cart(id=uuid4(), user_id=user_id)
        self.db.add(cart)
        self.db.commit()
        self.db.refresh(cart)
        return {
            "id": cart.id,
            "user_id": cart.user_id,
            "items": [],
            "created_at": cart.created_at.isoformat()
        }

    def get_cart(self, cart_id: UUID) -> dict:
        cart = self.db.query(Cart).filter(Cart.id == cart_id).first()
        if not cart:
            return None
        items = [
            {
                "service_id": item.service_id,
                "partner_id": item.partner_id,
                "slot_id": item.slot_id,
                "quantity": item.quantity,
                "unit_price": item.unit_price
            } for item in cart.items
        ]
        return {
            "id": cart.id,
            "user_id": cart.user_id,
            "items": items,
            "created_at": cart.created_at.isoformat()
        }

    def update_cart(self, cart_id: UUID, items: List[CartItemCreate]) -> dict:
        cart = self.db.query(Cart).filter(Cart.id == cart_id).first()
        if not cart:
            return None
        # Clear existing items
        self.db.query(CartItem).filter(CartItem.cart_id == cart_id).delete()
        # Add new items
        for item in items:
            cart_item = CartItem(
                id=uuid4(),
                cart_id=cart_id,
                service_id=item.service_id,
                partner_id=item.partner_id,
                slot_id=item.slot_id,
                quantity=item.quantity,
                unit_price=item.unit_price
            )
            self.db.add(cart_item)
        self.db.commit()
        return self.get_cart(cart_id)

    def delete_cart(self, cart_id: UUID):
        cart = self.db.query(Cart).filter(Cart.id == cart_id).first()
        if cart:
            self.db.delete(cart)
            self.db.commit()

    async def checkout(self, cart_id: UUID) -> dict:
        cart = self.db.query(Cart).filter(Cart.id == cart_id).first()
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")

        # Check slot availability
        async with httpx.AsyncClient() as client:
            for item in cart.items:
                response = await client.get(f"{self.slot_service_url}/{item.partner_id}/{item.service_id}")
                if response.status_code != 200 or not response.json().get("is_available"):
                    raise HTTPException(status_code=400, detail=f"Slot {item.slot_id} not available")

            # Calculate total with 10% discount
            total_price = sum(item.unit_price * item.quantity for item in cart.items)
            discounted_price = total_price * 0.9  # 10% flat discount

            # Call mocked Order API
            order_response = await client.post(self.order_api_url, json={"cart_id": str(cart_id), "total_price": discounted_price})
            if order_response.status_code != 201:
                raise HTTPException(status_code=503, detail="Order API unavailable")
            order_id = order_response.json().get("order_id")

        # Save booking (simplified, assumes booking table exists)
        booking = {
            "id": uuid4(),
            "cart_id": cart_id,
            "order_id": UUID(order_id),
            "user_id": cart.user_id,
            "total_price": discounted_price,
            "created_at": "CURRENT_TIMESTAMP"
        }
        self.db.execute("INSERT INTO cart.booking (id, cart_id, order_id, user_id, total_price, created_at) VALUES (:id, :cart_id, :order_id, :user_id, :total_price, :created_at)", booking)
        self.db.commit()

        return {
            "booking_id": booking["id"],
            "order_id": booking["order_id"],
            "total_price": discounted_price
        }