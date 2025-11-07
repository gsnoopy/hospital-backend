from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from app.core.timezone import get_current_time
from app.utils.uuid import uuid7_postgres


# [USER MODEL]
# [Modelo SQLAlchemy que representa usuários do sistema com dados pessoais e profissionais]
# [ENTRADA: dados do usuário - name, email, password, phone, role_id]
# [SAIDA: instância User com timestamps automáticos e relacionamentos com Role]
# [DEPENDENCIAS: Base, Column, Integer, String, DateTime, Boolean, ForeignKey, relationship, get_current_time]
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(UUID(as_uuid=True), unique=True, default=uuid7_postgres, index=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=get_current_time)
    updated_at = Column(DateTime, default=get_current_time, onupdate=get_current_time)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    job_title_id = Column(Integer, ForeignKey("job_titles.id"), nullable=True)
    hospital_id = Column(Integer, ForeignKey("hospitals.id"), nullable=True)

    role = relationship("Role", back_populates="users")
    job_title = relationship("JobTitle", back_populates="users")
    hospital = relationship("Hospital", back_populates="users")
    public_acquisitions = relationship("PublicAcquisition", back_populates="user")