from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from app.core.timezone import get_current_time
from app.utils.uuid import uuid7_postgres


# [CATEGORY MODEL]
# [Modelo SQLAlchemy que representa categorias principais de itens]
# [ENTRADA: dados da categoria - name, description, hospital_id]
# [SAIDA: instância Category com timestamps automáticos e relacionamentos]
# [DEPENDENCIAS: Base, Column, Integer, String, DateTime, ForeignKey, relationship, get_current_time]
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(UUID(as_uuid=True), unique=True, default=uuid7_postgres, index=True, nullable=False)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=get_current_time)
    updated_at = Column(DateTime, default=get_current_time, onupdate=get_current_time)
    hospital_id = Column(Integer, ForeignKey("hospitals.id", ondelete="CASCADE"), nullable=False, index=True)

    hospital = relationship("Hospital", back_populates="categories", lazy="joined")
    subcategories = relationship("SubCategory", back_populates="category", cascade="all, delete-orphan", lazy="noload")