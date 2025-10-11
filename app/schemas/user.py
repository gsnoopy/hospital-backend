from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID
from .role import RoleResponse
from .job_title import JobTitleResponse
from .hospital import HospitalResponse

# [USER BASE]
# [Schema base Pydantic com campos comuns para usuário - usado como base para outros schemas]
# [ENTRADA: name, email, phone, role_id, job_title_id, hospital_id]
# [SAIDA: instância UserBase validada]
# [DEPENDENCIAS: BaseModel, UUID]
class UserBase(BaseModel):
    name: str
    email: str
    phone: str
    role_id: UUID
    job_title_id: Optional[UUID] = None
    hospital_id: Optional[UUID] = None


# [USER CREATE]
# [Schema Pydantic para criação de usuário - herda campos base + adiciona password]
# [ENTRADA: herda todos campos de UserBase + password]
# [SAIDA: instância UserCreate para validação de entrada]
# [DEPENDENCIAS: UserBase]
class UserCreate(UserBase):
    password: str


# [USER UPDATE]
# [Schema Pydantic para atualização de usuário - todos os campos opcionais]
# [ENTRADA: campos opcionais para atualização]
# [SAIDA: instância UserUpdate para validação de entrada]
# [DEPENDENCIAS: BaseModel, Optional, UUID]
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    role_id: Optional[UUID] = None
    job_title_id: Optional[UUID] = None
    hospital_id: Optional[UUID] = None


# [USER RESPONSE]
# [Schema Pydantic para resposta de usuário - inclui campos de auditoria, public_id e relacionamentos]
# [ENTRADA: name, email, phone, public_id, is_active, created_at, updated_at, role, job_title, hospital]
# [SAIDA: instância UserResponse para resposta da API]
# [DEPENDENCIAS: BaseModel, RoleResponse, JobTitleResponse, HospitalResponse, datetime, UUID]
class UserResponse(BaseModel):
    name: str
    email: str
    phone: str
    is_active: bool
    public_id: UUID
    created_at: datetime
    updated_at: datetime
    role: RoleResponse
    job_title: Optional[JobTitleResponse] = None
    hospital: Optional[HospitalResponse] = None

    # [CONFIG]
    # [Configuração do Pydantic para permitir conversão de atributos SQLAlchemy]
    # [ENTRADA: nenhuma]
    # [SAIDA: configuração from_attributes=True]
    # [DEPENDENCIAS: nenhuma]
    class Config:
        from_attributes = True