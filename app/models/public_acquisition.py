from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from app.core.timezone import get_current_time
from app.utils.uuid import uuid7_postgres


# [PUBLIC ACQUISITION MODEL]
# [Modelo SQLAlchemy que representa licitações públicas dentro de um hospital]
# [ENTRADA: dados da licitação - code, title, year, hospital_id, user_id (Pregoeiro)]
# [SAIDA: instância PublicAcquisition com timestamps automáticos]
# [DEPENDENCIAS: Base, Column, Integer, String, DateTime, ForeignKey, relationship, get_current_time]
class PublicAcquisition(Base):
    __tablename__ = "public_acquisitions"

    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(UUID(as_uuid=True), unique=True, default=uuid7_postgres, index=True, nullable=False)
    code = Column(String, nullable=False, index=True)
    title = Column(String, nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime, default=get_current_time)
    updated_at = Column(DateTime, default=get_current_time, onupdate=get_current_time)
    hospital_id = Column(Integer, ForeignKey("hospitals.id", ondelete="RESTRICT"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)

    hospital = relationship("Hospital", back_populates="public_acquisitions", lazy="joined")
    user = relationship("User", back_populates="public_acquisitions", lazy="joined")
    item_public_acquisitions = relationship("ItemPublicAcquisition", back_populates="public_acquisition")
