from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID


# [SUBCATEGORY BASE]
# [Schema base Pydantic com campos comuns para subcategoria - usado como base para outros schemas]
# [ENTRADA: name, description, category_id]
# [SAIDA: instância SubCategoryBase validada]
# [DEPENDENCIAS: BaseModel]
class SubCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    category_id: UUID  # Public ID da categoria pai


# [SUBCATEGORY CREATE]
# [Schema Pydantic para criação de subcategoria - herda campos base]
# [ENTRADA: herda todos campos de SubCategoryBase]
# [SAIDA: instância SubCategoryCreate para validação de entrada]
# [DEPENDENCIAS: SubCategoryBase]
class SubCategoryCreate(SubCategoryBase):
    pass


# [SUBCATEGORY UPDATE]
# [Schema Pydantic para atualização de subcategoria - todos campos opcionais]
# [ENTRADA: name (opcional), description (opcional), category_id (opcional)]
# [SAIDA: instância SubCategoryUpdate para validação de entrada]
# [DEPENDENCIAS: BaseModel]
class SubCategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[UUID] = None


# [SUBCATEGORY RESPONSE]
# [Schema Pydantic para resposta de subcategoria - inclui dados do banco e categoria]
# [ENTRADA: dados completos da subcategoria do banco]
# [SAIDA: instância SubCategoryResponse para serialização de saída]
# [DEPENDENCIAS: SubCategoryBase, UUID, datetime]
class SubCategoryResponse(BaseModel):
    public_id: UUID
    name: str
    description: Optional[str] = None
    category_id: UUID = Field(alias="category_public_id")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True