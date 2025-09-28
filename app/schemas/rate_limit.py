import re
from typing import Dict

# [SANITIZE PATH]
# [Remove parâmetros dinâmicos do path para criar chave de rate limiting consistente]
# [ENTRADA: path - caminho da URL com parâmetros dinâmicos]
# [SAIDA: str - path sanitizado com placeholders para IDs e UUIDs]
# [DEPENDENCIAS: re]
def sanitize_path(path: str) -> str:
    sanitized = re.sub(r'/\d+', '/{id}', path)
    sanitized = re.sub(r'/[a-f0-9-]{36}', '/{uuid}', sanitized)
    return sanitized

# [RATE LIMITS CONFIGURATION]
# [Dicionário com configurações de rate limiting por endpoint - limite de requests e período em segundos]
# [ENTRADA: endpoints como chaves, dicts com limit e period como valores]
# [SAIDA: Dict mapeando endpoints para configurações de rate limit]
# [DEPENDENCIAS: Dict typing]
RATE_LIMITS: Dict[str, Dict[str, int]] = {

    "/auth": {"limit": 5, "period": 300},

    "/users": {"limit": 100, "period": 60},
    "/users/{id}": {"limit": 50, "period": 60},
    "POST /users": {"limit": 10, "period": 300},
    
    "/roles": {"limit": 80, "period": 60},
    "/roles/{id}": {"limit": 40, "period": 60},
    "POST /roles": {"limit": 15, "period": 300},
    "PUT /roles/{id}": {"limit": 20, "period": 300},
    "DELETE /roles/{id}": {"limit": 10, "period": 300},
    
    "/health": {"limit": 500, "period": 60},
    "/health/detailed": {"limit": 100, "period": 60},
    "/health/ready": {"limit": 1000, "period": 60},  
    "/health/live": {"limit": 1000, "period": 60}, 
    
    
    "default": {"limit": 200, "period": 60} 
}