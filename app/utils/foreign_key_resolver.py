from uuid import UUID
from typing import Dict, Any
from fastapi import HTTPException, status

# [FOREIGN KEY RESOLVER]
# [Classe utilitária para resolver public_id UUIDs em IDs internos para relacionamentos de chave estrangeira]
# [ENTRADA: update_data e foreign_key_mappings]
# [SAIDA: dados com foreign keys resolvidas ou HTTPException se entidade não encontrada]
# [DEPENDENCIAS: UUID, Dict, Any, HTTPException, status]
class ForeignKeyResolver:
    
    # [RESOLVE FOREIGN KEYS]
    # [Resolve public_id UUIDs para IDs internos em campos de chave estrangeira]
    # [ENTRADA: update_data - dict com dados para atualizar, foreign_key_mappings - mapeamento field_name para (repository, error_message)]
    # [SAIDA: Dict[str, Any] - dados com foreign keys resolvidas (UUIDs substituídos por IDs internos)]
    # [DEPENDENCIAS: isinstance, UUID, HTTPException, status]
    @staticmethod
    def resolve_foreign_keys(
        update_data: Dict[str, Any],
        foreign_key_mappings: Dict[str, tuple]
    ) -> Dict[str, Any]:
        resolved_data = update_data.copy()
        
        for field_name, (repository, error_message) in foreign_key_mappings.items():
            if field_name in resolved_data:
                public_id = resolved_data[field_name]
                if isinstance(public_id, UUID):
                    entity = repository.get_by_public_id(public_id)
                    if not entity:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=error_message
                        )
                    resolved_data[field_name] = entity.id
        
        return resolved_data