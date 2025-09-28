from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
from app.core.timezone import get_current_time
from app.utils.uuid import uuid7_postgres


# [JOB TITLE MODEL]
# [Modelo SQLAlchemy que representa cargos dentro de uma empresa]
# [ENTRADA: dados do cargo - title, department, seniority_level]
# [SAIDA: instância JobTitle com timestamps automáticos]
# [DEPENDENCIAS: Base, Column, Integer, String, DateTime, Boolean, ForeignKey, relationship, get_current_time]
class JobTitle(Base):
    __tablename__ = "job_titles"

    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(UUID(as_uuid=True), unique=True, default=uuid7_postgres, index=True, nullable=False)
    title = Column(String, nullable=False)
    department = Column(String, nullable=False)
    seniority_level = Column(String, nullable=False)
    created_at = Column(DateTime, default=get_current_time)
    updated_at = Column(DateTime, default=get_current_time, onupdate=get_current_time)
    
    users = relationship("User", back_populates="job_title")