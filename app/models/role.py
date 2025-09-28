from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from app.core.timezone import get_current_time
from app.utils.uuid import uuid7_postgres


# [ROLE MODEL]
# [Modelo SQLAlchemy que representa roles/funções de usuário no sistema]
# [ENTRADA: dados da role - name, description]
# [SAIDA: instância Role com timestamps automáticos e relacionamento com User]
# [DEPENDENCIAS: Base, Column, Integer, String, DateTime, relationship, get_current_time]
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(UUID(as_uuid=True), unique=True, default=uuid7_postgres, index=True, nullable=False)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=get_current_time)
    updated_at = Column(DateTime, default=get_current_time, onupdate=get_current_time)
    
    users = relationship("User", back_populates="role")