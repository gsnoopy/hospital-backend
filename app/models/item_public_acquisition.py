from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from app.core.timezone import get_current_time
from app.utils.uuid import uuid7_postgres


# [ITEM PUBLIC ACQUISITION MODEL]
# [Modelo SQLAlchemy que representa associação entre itens e licitações com fornecedor responsável]
# [ENTRADA: item_id, public_acquisition_id, supplier_id, is_holder]
# [SAIDA: instância ItemPublicAcquisition com timestamps automáticos]
# [DEPENDENCIAS: Base, Column, Integer, DateTime, Boolean, ForeignKey, relationship, get_current_time]
class ItemPublicAcquisition(Base):
    __tablename__ = "items_public_acquisitions"

    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(UUID(as_uuid=True), unique=True, default=uuid7_postgres, index=True, nullable=False)
    is_holder = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=get_current_time)
    updated_at = Column(DateTime, default=get_current_time, onupdate=get_current_time)

    item_id = Column(Integer, ForeignKey("items.id", ondelete="RESTRICT"), nullable=False, index=True)
    public_acquisition_id = Column(Integer, ForeignKey("public_acquisitions.id", ondelete="RESTRICT"), nullable=False, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id", ondelete="RESTRICT"), nullable=False, index=True)

    item = relationship("Item", back_populates="item_public_acquisitions", lazy="joined")
    public_acquisition = relationship("PublicAcquisition", back_populates="item_public_acquisitions", lazy="joined")
    supplier = relationship("Supplier", back_populates="item_public_acquisitions", lazy="joined")
