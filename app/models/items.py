from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSON
from app.core.database import Base
from app.core.timezone import get_current_time
from app.utils.uuid import uuid7_postgres


# [ITEM MODEL]
# [Modelo SQLAlchemy que representa itens do sistema categorizados com informações detalhadas]
# [ENTRADA: dados do item - name, description, full_description, internal_code, presentation, sample_qty, is_catalog, subcategory_id, hospital_id]
# [SAIDA: instância Item com timestamps automáticos e relacionamentos]
# [DEPENDENCIAS: Base, Column, Integer, String, DateTime, Boolean, ForeignKey, relationship, get_current_time]
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(UUID(as_uuid=True), unique=True, default=uuid7_postgres, index=True, nullable=False)
    name = Column(String, nullable=False, index=True)
    similar_names = Column(ARRAY(String), nullable=True)
    description = Column(String, nullable=True)
    full_description = Column(Text, nullable=True)
    internal_code = Column(String, nullable=True, unique=True, index=True)
    presentation = Column(String, nullable=True)
    sample = Column(Integer, nullable=True)
    has_catalog = Column(Boolean, default=False, nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=get_current_time)
    updated_at = Column(DateTime, default=get_current_time, onupdate=get_current_time)
    subcategory_id = Column(Integer, ForeignKey("subcategories.id", ondelete="RESTRICT"), nullable=False, index=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id", ondelete="RESTRICT"), nullable=False, index=True)

    subcategory = relationship("SubCategory", back_populates="items", lazy="joined")
    hospital = relationship("Hospital", back_populates="items", lazy="joined")
    