from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID


# [SUPPLIER BASE]
# [Schema base Pydantic com campos comuns para supplier - usado como base para outros schemas]
# [ENTRADA: name, document_type, document, email, phone (hospital_id vem do usuário logado)]
# [SAIDA: instância SupplierBase validada]
# [DEPENDENCIAS: BaseModel]
class SupplierBase(BaseModel):
    name: str
    document_type: str
    document: str
    email: str
    phone: str


# [SUPPLIER CREATE]
# [Schema Pydantic para criação de supplier - herda campos base (hospital_id vem do usuário logado)]
# [ENTRADA: herda todos campos de SupplierBase]
# [SAIDA: instância SupplierCreate para validação de entrada]
# [DEPENDENCIAS: SupplierBase]
class SupplierCreate(SupplierBase):
    pass


# [SUPPLIER UPDATE]
# [Schema Pydantic para atualização de supplier - todos campos opcionais]
# [ENTRADA: name (opcional), document_type (opcional), document (opcional), email (opcional), phone (opcional)]
# [SAIDA: instância SupplierUpdate para validação de entrada]
# [DEPENDENCIAS: BaseModel]
class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    document_type: Optional[str] = None
    document: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


# [SUPPLIER RESPONSE]
# [Schema Pydantic para resposta de supplier - inclui dados do banco]
# [ENTRADA: dados completos do supplier do banco]
# [SAIDA: instância SupplierResponse para serialização de saída]
# [DEPENDENCIAS: BaseModel, UUID, datetime]
class SupplierResponse(BaseModel):
    public_id: UUID
    name: str
    document_type: str
    document: str
    email: str
    phone: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
