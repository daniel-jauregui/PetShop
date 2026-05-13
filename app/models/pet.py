from sqlalchemy import Column, Integer, String
from app.db.session import Base


class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
