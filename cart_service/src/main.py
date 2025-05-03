from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from src.models.cart import Cart, CartItem, get_db
from src.services.cart_service import CartService
from src.utils.auth import verify_jwt_token, User

app = FastAPI(title="Cart Service", version="1.0.0")

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="http://auth-service/authorize",
    tokenUrl="http://auth-service/token"
)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    user = verify_jwt_token(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return user

class CartItemCreate(BaseModel):
    service_id: UUID
    partner_id: UUID
    slot_id: UUID
    quantity: int
    unit_price: float

class CartCreate(BaseModel):
    user_id: UUID

class CartResponse(BaseModel):
    id: UUID
    user_id: UUID
    items: List[CartItemCreate]
    created_at: str

class CheckoutResponse(BaseModel):
    booking_id: UUID
    order_id: UUID
    total_price: float

@app.post("/carts", response_model=CartResponse, status_code=status.HTTP_201_CREATED)
async def create_cart(cart: CartCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.role != "customer" and user.sub != str(cart.user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    cart_service = CartService(db)
    return cart_service.create_cart(cart.user_id)

@app.get("/carts/{cart_id}", response_model=CartResponse)
async def get_cart(cart_id: UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart_service = CartService(db)
    cart = cart_service.get_cart(cart_id)
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
    if user.role != "admin" and user.sub != str(cart.user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return cart

@app.put("/carts/{cart_id}", response_model=CartResponse)
async def update_cart(cart_id: UUID, items: List[CartItemCreate], user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart_service = CartService(db)
    cart = cart_service.get_cart(cart_id)
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
    if user.role != "customer" and user.sub != str(cart.user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return cart_service.update_cart(cart_id, items)

@app.delete("/carts/{cart_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cart(cart_id: UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart_service = CartService(db)
    cart = cart_service.get_cart(cart_id)
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
    if user.role != "customer" and user.sub != str(cart.user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    cart_service.delete_cart(cart_id)
    return None

@app.post("/carts/{cart_id}/checkout", response_model=CheckoutResponse)
async def checkout_cart(cart_id: UUID, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart_service = CartService(db)
    cart = cart_service.get_cart(cart_id)
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
    if user.role != "customer" and user.sub != str(cart.user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return await cart_service.checkout(cart_id)