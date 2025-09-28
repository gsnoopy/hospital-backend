from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID


# [ROLE BASE]
# [Schema base Pydantic com campos comuns para role - usado como base para outros schemas]
# [ENTRADA: name - nome da role, description - descrição opcional]
# [SAIDA: instância RoleBase validada]
# [DEPENDENCIAS: BaseModel, Optional]
class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None


# [ROLE CREATE]
# [Schema Pydantic para criação de role - herda todos os campos de RoleBase]
# [ENTRADA: herda name e description de RoleBase]
# [SAIDA: instância RoleCreate para validação de entrada]
# [DEPENDENCIAS: RoleBase]
class RoleCreate(RoleBase):
    pass


# [ROLE UPDATE]
# [Schema Pydantic para atualização de role - todos os campos opcionais]
# [ENTRADA: campos opcionais para atualização]
# [SAIDA: instância RoleUpdate para validação de entrada]
# [DEPENDENCIAS: BaseModel, Optional]
class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


# [ROLE RESPONSE]
# [Schema Pydantic para resposta de role - inclui campos de auditoria e public_id]
# [ENTRADA: herda name/description + public_id, created_at, updated_at]
# [SAIDA: instância RoleResponse para resposta da API]
# [DEPENDENCIAS: RoleBase, datetime, UUID]
class RoleResponse(RoleBase):
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