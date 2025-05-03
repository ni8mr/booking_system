from fastapi import FastAPI
from src.api.slots import router as slots_router
import os

app = FastAPI(title="Slot Service", version="1.0.0")

JWT_PUBLIC_KEY = os.getenv("JWT_PUBLIC_KEY")
if not JWT_PUBLIC_KEY:
    raise ValueError("JWT_PUBLIC_KEY environment variable is not set")
JWT_PUBLIC_KEY = JWT_PUBLIC_KEY.replace("\\n", "\n")  # Convert \n to newlines
print("Loaded JWT_PUBLIC_KEY:", JWT_PUBLIC_KEY[:50] + "...")  # Debug

app.include_router(slots_router, prefix="/slots", tags=["Slots"])