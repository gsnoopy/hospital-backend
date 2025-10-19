from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from uuid import UUID


# [CATALOG BASE]
# [Schema base Pydantic com campos comuns para catalog - usado como base para outros schemas]
# [ENTRADA: name, similar_names, description, full_description, presentation]
# [SAIDA: instância CatalogBase validada]
# [DEPENDENCIAS: BaseModel]
class CatalogBase(BaseModel):
    name: str
    similar_names: Optional[List[str]] = None
    description: Optional[str] = None
    full_description: Optional[str] = None
    presentation: Optional[str] = None


# [CATALOG CREATE]
# [Schema Pydantic para criação de catalog - herda campos base]
# [ENTRADA: herda todos campos de CatalogBase]
# [SAIDA: instância CatalogCreate para validação de entrada]
# [DEPENDENCIAS: CatalogBase]
class CatalogCreate(CatalogBase):
    pass


# [CATALOG UPDATE]
# [Schema Pydantic para atualização de catalog - todos campos opcionais]
# [ENTRADA: name (opcional), similar_names (opcional), description (opcional), full_description (opcional), presentation (opcional)]
# [SAIDA: instância CatalogUpdate para validação de entrada]
# [DEPENDENCIAS: BaseModel]
class CatalogUpdate(BaseModel):
    name: Optional[str] = None
    similar_names: Optional[List[str]] = None
    description: Optional[str] = None
    full_description: Optional[str] = None
    presentation: Optional[str] = None


# [CATALOG RESPONSE]
# [Schema Pydantic para resposta de catalog - inclui dados do banco]
# [ENTRADA: dados completos do catalog do banco]
# [SAIDA: instância CatalogResponse para serialização de saída]
# [DEPENDENCIAS: CatalogBase, UUID, datetime]
class CatalogResponse(CatalogBase):
    public_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True