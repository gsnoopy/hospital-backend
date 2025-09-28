from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID

# [HOSPITAL BASE]
# [Schema base Pydantic com campos comuns para hospital - usado como base para outros schemas]
# [ENTRADA: name, nationality, document_type, document, email, phone, city]
# [SAIDA: instância HospitalBase validada]
# [DEPENDENCIAS: BaseModel]
class HospitalBase(BaseModel):
    name: str
    nationality: str
    document_type: str
    document: str
    email: str
    phone: str
    city: str


# [HOSPITAL CREATE]
# [Schema Pydantic para criação de hospital - herda campos base]
# [ENTRADA: herda todos campos de HospitalBase]
# [SAIDA: instância HospitalCreate para validação de entrada]
# [DEPENDENCIAS: HospitalBase]
class HospitalCreate(HospitalBase):
    pass


# [HOSPITAL UPDATE]
# [Schema Pydantic para atualização de hospital - todos os campos opcionais]
# [ENTRADA: campos opcionais para atualização]
# [SAIDA: instância HospitalUpdate para validação de entrada]
# [DEPENDENCIAS: BaseModel, Optional]
class HospitalUpdate(BaseModel):
    name: Optional[str] = None
    nationality: Optional[str] = None
    document_type: Optional[str] = None
    document: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None


# [HOSPITAL RESPONSE]
# [Schema Pydantic para resposta de hospital - inclui campos de auditoria e public_id]
# [ENTRADA: name, nationality, document_type, document, email, phone, city, public_id, created_at, updated_at]
# [SAIDA: instância HospitalResponse para resposta da API]
# [DEPENDENCIAS: BaseModel, datetime, UUID]
class HospitalResponse(BaseModel):
    name: str
    nationality: str
    document_type: str
    document: str
    email: str
    phone: str
    city: str
    public_id: UUID
    created_at: datetime
    updated_at: datetime

    # [CONFIG]
    # [Configuração do Pydantic para permitir conversão de atributos SQLAlchemy]
    # [ENTRADA: nenhuma]
    # [SAIDA: configuração from_attributes=True]
    # [DEPENDENCIAS: nenhuma]
    class Config:
        from_attributes = True