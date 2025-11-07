from pydantic import BaseModel
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from app.schemas.user import UserResponse


# [PUBLIC ACQUISITION BASE]
# [Schema base Pydantic com campos comuns para public_acquisition - usado como base para outros schemas]
# [ENTRADA: code, title, year, user_id (Pregoeiro) - hospital_id vem do contexto]
# [SAIDA: instância PublicAcquisitionBase validada]
# [DEPENDENCIAS: BaseModel, UUID]
class PublicAcquisitionBase(BaseModel):
    code: str
    title: str
    year: int
    user_id: UUID


# [PUBLIC ACQUISITION CREATE]
# [Schema Pydantic para criação de public_acquisition - herda campos base (hospital_id vem do usuário logado)]
# [ENTRADA: herda todos campos de PublicAcquisitionBase]
# [SAIDA: instância PublicAcquisitionCreate para validação de entrada]
# [DEPENDENCIAS: PublicAcquisitionBase]
class PublicAcquisitionCreate(PublicAcquisitionBase):
    pass


# [PUBLIC ACQUISITION UPDATE]
# [Schema Pydantic para atualização de public_acquisition - todos campos opcionais]
# [ENTRADA: code (opcional), title (opcional), year (opcional), user_id (opcional)]
# [SAIDA: instância PublicAcquisitionUpdate para validação de entrada]
# [DEPENDENCIAS: BaseModel, UUID]
class PublicAcquisitionUpdate(BaseModel):
    code: Optional[str] = None
    title: Optional[str] = None
    year: Optional[int] = None
    user_id: Optional[UUID] = None


# [USER SIMPLIFIED RESPONSE]
# [Schema simplificado para dados do usuário Pregoeiro na resposta de licitação]
# [ENTRADA: dados básicos do usuário]
# [SAIDA: instância UserSimplifiedResponse]
# [DEPENDENCIAS: BaseModel, UUID, datetime]
class UserSimplifiedResponse(BaseModel):
    public_id: UUID
    name: str
    email: str
    phone: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# [PUBLIC ACQUISITION RESPONSE]
# [Schema Pydantic para resposta de public_acquisition - inclui dados do banco e usuário]
# [ENTRADA: dados completos da licitação do banco]
# [SAIDA: instância PublicAcquisitionResponse para serialização de saída]
# [DEPENDENCIAS: BaseModel, UUID, datetime, UserSimplifiedResponse]
class PublicAcquisitionResponse(BaseModel):
    public_id: UUID
    code: str
    title: str
    year: int
    user: UserSimplifiedResponse
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
