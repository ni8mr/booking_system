from fastapi import FastAPI
from src.api.categories import router as categories_router
from src.api.subcategories import router as subcategories_router
from src.api.services import router as services_router

app = FastAPI(title="Catalog Service", version="1.0.0")

app.include_router(categories_router, prefix="/categories", tags=["Categories"])
app.include_router(subcategories_router, prefix="/subcategories", tags=["Subcategories"])
app.include_router(services_router, prefix="/services", tags=["Services"])