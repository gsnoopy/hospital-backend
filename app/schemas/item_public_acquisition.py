from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID


# [ITEM PUBLIC ACQUISITION BASE]
# [Schema base Pydantic para associação item-licitação-fornecedor]
# [ENTRADA: item_id, public_acquisition_id, supplier_id (UUIDs públicos), is_holder (bool)]
# [SAIDA: instância ItemPublicAcquisitionBase validada]
# [DEPENDENCIAS: BaseModel, UUID]
class ItemPublicAcquisitionBase(BaseModel):
    item_id: UUID
    public_acquisition_id: UUID
    supplier_id: UUID
    is_holder: bool = False


# [ITEM PUBLIC ACQUISITION CREATE]
# [Schema Pydantic para criação de associação]
# [ENTRADA: herda todos campos de ItemPublicAcquisitionBase]
# [SAIDA: instância ItemPublicAcquisitionCreate para validação de entrada]
# [DEPENDENCIAS: ItemPublicAcquisitionBase]
class ItemPublicAcquisitionCreate(ItemPublicAcquisitionBase):
    pass


# [ITEM PUBLIC ACQUISITION UPDATE]
# [Schema Pydantic para atualização de associação - supplier_id e is_holder opcionais]
# [ENTRADA: supplier_id (opcional), is_holder (opcional)]
# [SAIDA: instância ItemPublicAcquisitionUpdate para validação de entrada]
# [DEPENDENCIAS: BaseModel, UUID]
class ItemPublicAcquisitionUpdate(BaseModel):
    supplier_id: Optional[UUID] = None
    is_holder: Optional[bool] = None


# [ITEM SIMPLIFIED RESPONSE]
# [Schema simplificado para dados do item na resposta de associação]
# [ENTRADA: dados básicos do item]
# [SAIDA: instância ItemSimplifiedResponse]
# [DEPENDENCIAS: BaseModel, UUID]
class ItemSimplifiedResponse(BaseModel):
    public_id: UUID
    name: str
    similar_names: Optional[list[str]] = None
    description: Optional[str] = None
    internal_code: Optional[str] = None
    presentation: Optional[str] = None

    class Config:
        from_attributes = True


# [PUBLIC ACQUISITION SIMPLIFIED RESPONSE]
# [Schema simplificado para dados da licitação na resposta de associação]
# [ENTRADA: dados básicos da licitação]
# [SAIDA: instância PublicAcquisitionSimplifiedResponse]
# [DEPENDENCIAS: BaseModel, UUID]
class PublicAcquisitionSimplifiedResponse(BaseModel):
    public_id: UUID
    code: str
    title: str
    year: int

    class Config:
        from_attributes = True


# [SUPPLIER SIMPLIFIED RESPONSE]
# [Schema simplificado para dados do fornecedor na resposta de associação]
# [ENTRADA: dados básicos do fornecedor]
# [SAIDA: instância SupplierSimplifiedResponse]
# [DEPENDENCIAS: BaseModel, UUID]
class SupplierSimplifiedResponse(BaseModel):
    public_id: UUID
    name: str
    document_type: str
    document: str
    email: str
    phone: str

    class Config:
        from_attributes = True


# [ITEM PUBLIC ACQUISITION RESPONSE]
# [Schema Pydantic para resposta de associação - inclui dados completos]
# [ENTRADA: dados completos da associação do banco]
# [SAIDA: instância ItemPublicAcquisitionResponse para serialização de saída]
# [DEPENDENCIAS: BaseModel, UUID, datetime]
class ItemPublicAcquisitionResponse(BaseModel):
    public_id: UUID
    item: ItemSimplifiedResponse
    public_acquisition: PublicAcquisitionSimplifiedResponse
    supplier: SupplierSimplifiedResponse
    is_holder: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
