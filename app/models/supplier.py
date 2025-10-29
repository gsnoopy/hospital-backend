from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from app.core.timezone import get_current_time
from app.utils.uuid import uuid7_postgres


# [SUPPLIER MODEL]
# [Modelo SQLAlchemy que representa fornecedores dentro de um hospital]
# [ENTRADA: dados do fornecedor - name, document_type, document, email, phone, hospital_id]
# [SAIDA: instância Supplier com timestamps automáticos]
# [DEPENDENCIAS: Base, Column, Integer, String, DateTime, ForeignKey, relationship, get_current_time]
class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(UUID(as_uuid=True), unique=True, default=uuid7_postgres, index=True, nullable=False)
    name = Column(String, nullable=False, index=True)
    document_type = Column(String, nullable=False)
    document = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, index=True)
    phone = Column(String, nullable=False)
    created_at = Column(DateTime, default=get_current_time)
    updated_at = Column(DateTime, default=get_current_time, onupdate=get_current_time)
    hospital_id = Column(Integer, ForeignKey("hospitals.id", ondelete="RESTRICT"), nullable=False, index=True)

    hospital = relationship("Hospital", back_populates="suppliers", lazy="joined")
