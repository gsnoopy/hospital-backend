from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from .subcategory import SubCategoryResponse


# [ITEM BASE]
# [Schema base Pydantic com campos comuns para item - usado como base para outros schemas]
# [ENTRADA: name, similar_names, description, full_description, internal_code, presentation, sample, has_catalog, subcategory_id (hospital_id vem do usuário logado)]
# [SAIDA: instância ItemBase validada]
# [DEPENDENCIAS: BaseModel]
class ItemBase(BaseModel):
    name: str
    similar_names: Optional[List[str]] = None
    description: Optional[str] = None
    full_description: Optional[str] = None
    internal_code: Optional[str] = None
    presentation: Optional[str] = None
    sample: Optional[int] = None
    has_catalog: bool = False
    subcategory_id: UUID


# [ITEM CREATE]
# [Schema Pydantic para criação de item - herda campos base (hospital_id vem do usuário logado)]
# [ENTRADA: herda todos campos de ItemBase]
# [SAIDA: instância ItemCreate para validação de entrada]
# [DEPENDENCIAS: ItemBase]
class ItemCreate(ItemBase):
    pass


# [ITEM UPDATE]
# [Schema Pydantic para atualização de item - todos campos opcionais]
# [ENTRADA: name (opcional), similar_names (opcional), description (opcional), full_description (opcional), internal_code (opcional), presentation (opcional), sample (opcional), has_catalog (opcional), subcategory_id (opcional)]
# [SAIDA: instância ItemUpdate para validação de entrada]
# [DEPENDENCIAS: BaseModel]
class ItemUpdate(BaseModel):
    name: Optional[str] = None
    similar_names: Optional[List[str]] = None
    description: Optional[str] = None
    full_description: Optional[str] = None
    internal_code: Optional[str] = None
    presentation: Optional[str] = None
    sample: Optional[int] = None
    has_catalog: Optional[bool] = None
    subcategory_id: Optional[UUID] = None


# [ITEM RESPONSE]
# [Schema Pydantic para resposta de item - inclui dados do banco e relacionamento com subcategory]
# [ENTRADA: dados completos do item do banco]
# [SAIDA: instância ItemResponse para serialização de saída]
# [DEPENDENCIAS: BaseModel, UUID, datetime, SubCategoryResponse]
class ItemResponse(BaseModel):
    name: str
    similar_names: Optional[List[str]] = None
    description: Optional[str] = None
    full_description: Optional[str] = None
    internal_code: Optional[str] = None
    presentation: Optional[str] = None
    sample: Optional[int] = None
    has_catalog: bool
    public_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    subcategory: SubCategoryResponse

    class Config:
        from_attributes = True
