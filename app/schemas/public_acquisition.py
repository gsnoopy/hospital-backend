from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID


# [PUBLIC ACQUISITION BASE]
# [Schema base Pydantic com campos comuns para public_acquisition - usado como base para outros schemas]
# [ENTRADA: code, title (hospital_id vem do usuário logado)]
# [SAIDA: instância PublicAcquisitionBase validada]
# [DEPENDENCIAS: BaseModel]
class PublicAcquisitionBase(BaseModel):
    code: str
    title: str


# [PUBLIC ACQUISITION CREATE]
# [Schema Pydantic para criação de public_acquisition - herda campos base (hospital_id vem do usuário logado)]
# [ENTRADA: herda todos campos de PublicAcquisitionBase]
# [SAIDA: instância PublicAcquisitionCreate para validação de entrada]
# [DEPENDENCIAS: PublicAcquisitionBase]
class PublicAcquisitionCreate(PublicAcquisitionBase):
    pass


# [PUBLIC ACQUISITION UPDATE]
# [Schema Pydantic para atualização de public_acquisition - todos campos opcionais]
# [ENTRADA: code (opcional), title (opcional)]
# [SAIDA: instância PublicAcquisitionUpdate para validação de entrada]
# [DEPENDENCIAS: BaseModel]
class PublicAcquisitionUpdate(BaseModel):
    code: Optional[str] = None
    title: Optional[str] = None


# [PUBLIC ACQUISITION RESPONSE]
# [Schema Pydantic para resposta de public_acquisition - inclui dados do banco]
# [ENTRADA: dados completos da licitação do banco]
# [SAIDA: instância PublicAcquisitionResponse para serialização de saída]
# [DEPENDENCIAS: BaseModel, UUID, datetime]
class PublicAcquisitionResponse(BaseModel):
    public_id: UUID
    code: str
    title: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
