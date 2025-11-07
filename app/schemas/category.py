from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from uuid import UUID


# [CATEGORY BASE]
# [Schema base Pydantic com campos comuns para categoria - usado como base para outros schemas]
# [ENTRADA: name, description]
# [SAIDA: instância CategoryBase validada]
# [DEPENDENCIAS: BaseModel]
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None


# [CATEGORY CREATE]
# [Schema Pydantic para criação de categoria - herda campos base]
# [ENTRADA: herda todos campos de CategoryBase (hospital_id vem do usuário logado)]
# [SAIDA: instância CategoryCreate para validação de entrada]
# [DEPENDENCIAS: CategoryBase]
class CategoryCreate(CategoryBase):
    pass


# [CATEGORY UPDATE]
# [Schema Pydantic para atualização de categoria - todos campos opcionais]
# [ENTRADA: name (opcional), description (opcional)]
# [SAIDA: instância CategoryUpdate para validação de entrada]
# [DEPENDENCIAS: BaseModel]
class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


# [CATEGORY RESPONSE]
# [Schema Pydantic para resposta de categoria - inclui dados do banco]
# [ENTRADA: dados completos da categoria do banco]
# [SAIDA: instância CategoryResponse para serialização de saída]
# [DEPENDENCIAS: CategoryBase, UUID, datetime]
class CategoryResponse(CategoryBase):
    public_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# [SUBCATEGORY SIMPLIFIED RESPONSE]
# [Schema simplificado para subcategorias dentro da resposta de categoria]
# [ENTRADA: dados da subcategoria do banco]
# [SAIDA: instância SubCategorySimplifiedResponse]
# [DEPENDENCIAS: BaseModel, UUID, datetime]
class SubCategorySimplifiedResponse(BaseModel):
    public_id: UUID
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# [CATEGORY WITH SUBCATEGORIES RESPONSE]
# [Schema para resposta de categoria com subcategorias aninhadas]
# [ENTRADA: dados da categoria com suas subcategorias]
# [SAIDA: instância CategoryWithSubcategoriesResponse]
# [DEPENDENCIAS: CategoryBase, UUID, datetime, List, SubCategorySimplifiedResponse]
class CategoryWithSubcategoriesResponse(CategoryBase):
    public_id: UUID
    created_at: datetime
    updated_at: datetime
    subcategories: List[SubCategorySimplifiedResponse] = []

    class Config:
        from_attributes = True