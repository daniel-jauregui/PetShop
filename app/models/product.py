from sqlalchemy import Column, Integer, String, Float
from app.db.session import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False, index=True)
    description = Column(String(500), nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    category = Column(String(50), nullable=False, index=True)  # "food", "toys", "accessories", "medicine"
    pet_type = Column(String(50), nullable=False, index=True)  # "dog", "cat", "bird", etc.
