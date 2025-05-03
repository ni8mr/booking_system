from fastapi import FastAPI
from src.api.slots import router as slots_router

app = FastAPI(title="Slot Service", version="1.0.0")

app.include_router(slots_router, prefix="/slots", tags=["Slots"])