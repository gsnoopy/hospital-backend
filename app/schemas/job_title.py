from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID

# [JOB TITLE BASE]
# [Schema base Pydantic com campos comuns para cargo - usado como base para outros schemas]
# [ENTRADA: title]
# [SAIDA: instância JobTitleBase validada]
# [DEPENDENCIAS: BaseModel]
class JobTitleBase(BaseModel):
    title: str


# [JOB TITLE CREATE]
# [Schema Pydantic para criação de cargo - herda campos base]
# [ENTRADA: herda todos campos de JobTitleBase]
# [SAIDA: instância JobTitleCreate para validação de entrada]
# [DEPENDENCIAS: JobTitleBase]
class JobTitleCreate(JobTitleBase):
    pass


# [JOB TITLE UPDATE]
# [Schema Pydantic para atualização de cargo - todos os campos opcionais]
# [ENTRADA: campos opcionais para atualização]
# [SAIDA: instância JobTitleUpdate para validação de entrada]
# [DEPENDENCIAS: BaseModel, Optional]
class JobTitleUpdate(BaseModel):
    title: Optional[str] = None


# [JOB TITLE RESPONSE]
# [Schema Pydantic para resposta de cargo - inclui campos de auditoria e public_id]
# [ENTRADA: title, public_id, created_at, updated_at]
# [SAIDA: instância JobTitleResponse para resposta da API]
# [DEPENDENCIAS: BaseModel, datetime, UUID]
class JobTitleResponse(BaseModel):
    title: str
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
