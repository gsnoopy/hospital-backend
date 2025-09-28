from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from app.core.timezone import get_current_time
from app.utils.uuid import uuid7_postgres


# [ITEM GROUP MODEL]
# [Modelo SQLAlchemy que representa grupos de itens com relacionamento one-to-many com subgrupos]
# [ENTRADA: dados do grupo - name, description]
# [SAIDA: instância ItemGroup com timestamps automáticos e relacionamento com ItemSubGroup]
# [DEPENDENCIAS: Base, Column, Integer, String, DateTime, relationship, get_current_time]
class ItemGroup(Base):
    __tablename__ = "item_groups"

    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(UUID(as_uuid=True), unique=True, default=uuid7_postgres, index=True, nullable=False)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=get_current_time)
    updated_at = Column(DateTime, default=get_current_time, onupdate=get_current_time)

    # Relacionamento One-to-Many: 1 grupo tem muitos subgrupos
    subgroups = relationship("ItemSubGroup", back_populates="group", cascade="all, delete-orphan")