from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from app.core.timezone import get_current_time
from app.utils.uuid import uuid7_postgres


# [SUBCATEGORY MODEL]
# [Modelo SQLAlchemy que representa subcategorias que pertencem a uma categoria]
# [ENTRADA: dados da subcategoria - name, description, category_id]
# [SAIDA: instância SubCategory com timestamps automáticos e relacionamentos]
# [DEPENDENCIAS: Base, Column, Integer, String, DateTime, Boolean, ForeignKey, relationship, get_current_time]
class SubCategory(Base):
    __tablename__ = "subcategories"

    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(UUID(as_uuid=True), unique=True, default=uuid7_postgres, index=True, nullable=False)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=get_current_time)
    updated_at = Column(DateTime, default=get_current_time, onupdate=get_current_time)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False, index=True)

    category = relationship("Category", back_populates="subcategories")
    items = relationship("Item", back_populates="subcategory")