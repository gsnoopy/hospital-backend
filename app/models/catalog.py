from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from app.core.timezone import get_current_time
from app.utils.uuid import uuid7_postgres


# [CATALOG MODEL]
# [Modelo SQLAlchemy que representa catálogo de itens para busca e referência do admin]
# [ENTRADA: dados do catálogo - name, description, full_description, internal_code, presentation, sample, category_id, subcategory_id]
# [SAIDA: instância Catalog com timestamps automáticos e relacionamentos]
# [DEPENDENCIAS: Base, Column, Integer, String, DateTime, Boolean, ForeignKey, relationship, get_current_time]
class Catalog(Base):
    __tablename__ = "catalog"

    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(UUID(as_uuid=True), unique=True, default=uuid7_postgres, index=True, nullable=False)
    name = Column(String, nullable=False, index=True)
    similar_names = Column(ARRAY(String), nullable=True)
    description = Column(String, nullable=True)
    full_description = Column(Text, nullable=True)
    presentation = Column(String, nullable=True)
    created_at = Column(DateTime, default=get_current_time)
    updated_at = Column(DateTime, default=get_current_time, onupdate=get_current_time)