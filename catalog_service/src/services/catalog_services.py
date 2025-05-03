from sqlalchemy.orm import Session
from src.models.catalog import Category, Subcategory, Service
from uuid import UUID, uuid4
from fastapi import HTTPException

class CatalogService:
    def __init__(self, db: Session):
        self.db = db

    def list_categories(self) -> list:
        categories = self.db.query(Category).all()
        return [{"id": c.id, "name": c.name} for c in categories]

    def create_category(self, name: str) -> dict:
        category = Category(id=uuid4(), name=name)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return {"id": category.id, "name": category.name}

    def list_subcategories(self, category_id: UUID) -> list:
        subcategories = self.db.query(Subcategory).filter(Subcategory.category_id == category_id).all()
        return [{"id": s.id, "name": s.name, "category_id": s.category_id} for s in subcategories]

    def create_subcategory(self, name: str, category_id: UUID) -> dict:
        category = self.db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        subcategory = Subcategory(id=uuid4(), name=name, category_id=category_id)
        self.db.add(subcategory)
        self.db.commit()
        self.db.refresh(subcategory)
        return {"id": subcategory.id, "name": subcategory.name, "category_id": subcategory.category_id}

    def list_services(self, subcategory_id: UUID) -> list:
        services = self.db.query(Service).filter(Service.subcategory_id == subcategory_id).all()
        return [
            {
                "id": s.id,
                "name": s.name,
                "subcategory_id": s.subcategory_id,
                "price": s.price,
                "duration": s.duration
            } for s in services
        ]

    def get_service(self, service_id: UUID) -> dict:
        service = self.db.query(Service).filter(Service.id == service_id).first()
        if not service:
            return None
        return {
            "id": service.id,
            "name": service.name,
            "subcategory_id": service.subcategory_id,
            "price": service.price,
            "duration": service.duration
        }

    def create_service(self, name: str, subcategory_id: UUID, price: float, duration: int) -> dict:
        subcategory = self.db.query(Subcategory).filter(Subcategory.id == subcategory_id).first()
        if not subcategory:
            raise HTTPException(status_code=404, detail="Subcategory not found")
        service = Service(id=uuid4(), name=name, subcategory_id=subcategory_id, price=price, duration=duration)
        self.db.add(service)
        self.db.commit()
        self.db.refresh(service)
        return {
            "id": service.id,
            "name": service.name,
            "subcategory_id": service.subcategory_id,
            "price": service.price,
            "duration": service.duration
        }