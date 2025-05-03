from fastapi import FastAPI
from src.api.categories import router as categories_router
from src.api.subcategories import router as subcategories_router
from src.api.services import router as services_router
import os

app = FastAPI(title="Catalog Service", version="1.0.0")

JWT_PUBLIC_KEY = os.getenv("JWT_PUBLIC_KEY")
if not JWT_PUBLIC_KEY:
    raise ValueError("JWT_PUBLIC_KEY environment variable is not set")
JWT_PUBLIC_KEY = JWT_PUBLIC_KEY.replace("\\n", "\n")  # Convert \n to newlines
print("Loaded JWT_PUBLIC_KEY:", JWT_PUBLIC_KEY[:50] + "...")  # Debug

app.include_router(categories_router, prefix="/categories", tags=["Categories"])
app.include_router(subcategories_router, prefix="/subcategories", tags=["Subcategories"])
app.include_router(services_router, prefix="/services", tags=["Services"])