from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from app.core.timezone import get_current_time
from app.utils.uuid import uuid7_postgres


# [HOSPITAL MODEL]
# [Modelo SQLAlchemy que representa hospitais do sistema com dados relevantes]
# [ENTRADA: dados do hospital - name, nationality, document, email, phone, city]
# [SAIDA: instância Hospital com timestamps automáticos]
# [DEPENDENCIAS: Base, Column, Integer, String, DateTime, LargeBinary, ForeignKey, relationship, get_current_time]
class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(UUID(as_uuid=True), unique=True, default=uuid7_postgres, index=True, nullable=False)
    name = Column(String, nullable=False)
    nationality = Column(String, nullable=False)
    document_type = Column(String, index=True, nullable=False)
    document = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    city = Column(String, nullable=False)
    image = Column(LargeBinary, nullable=True)
    created_at = Column(DateTime, default=get_current_time)
    updated_at = Column(DateTime, default=get_current_time, onupdate=get_current_time)

    users = relationship("User", back_populates="hospital", lazy="noload")
    categories = relationship("Category", back_populates="hospital", cascade="all, delete-orphan", lazy="noload")
    subcategories = relationship("SubCategory", back_populates="hospital", cascade="all, delete-orphan", lazy="noload")
    items = relationship("Item", back_populates="hospital", lazy="noload")