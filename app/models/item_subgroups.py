from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from app.core.timezone import get_current_time
from app.utils.uuid import uuid7_postgres


# [ITEM SUBGROUP MODEL]
# [Modelo SQLAlchemy que representa subgrupos de itens pertencentes a um grupo]
# [ENTRADA: dados do subgrupo - name, description, group_id]
# [SAIDA: instância ItemSubGroup com timestamps automáticos e relacionamento com ItemGroup]
# [DEPENDENCIAS: Base, Column, Integer, String, DateTime, Boolean, ForeignKey, relationship, get_current_time]
class ItemSubGroup(Base):
    __tablename__ = "item_subgroups"

    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(UUID(as_uuid=True), unique=True, default=uuid7_postgres, index=True, nullable=False)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=get_current_time)
    updated_at = Column(DateTime, default=get_current_time, onupdate=get_current_time)

    # Foreign Key para ItemGroup
    group_id = Column(Integer, ForeignKey("item_groups.id", ondelete="CASCADE"), nullable=False, index=True)

    # Relacionamento Many-to-One: muitos subgrupos pertencem a 1 grupo
    group = relationship("ItemGroup", back_populates="subgroups")