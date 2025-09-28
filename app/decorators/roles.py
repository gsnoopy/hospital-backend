from fastapi import Depends, HTTPException, status
from typing import List, Union, Callable
from app.decorators.auth import require_auth
from app.models.user import User


# [REQUIRE ROLES]
# [Decorator factory que cria dependency para verificar se o usuário tem uma das roles permitidas]
# [ENTRADA: allowed_roles - string ou lista de strings com roles permitidas]
# [SAIDA: Callable - função dependency que valida role do usuário]
# [DEPENDENCIAS: require_auth, HTTPException, status]
def require_roles(allowed_roles: Union[str, List[str]]) -> Callable:

    if isinstance(allowed_roles, str):
        allowed_roles = [allowed_roles]
    
    # [ROLE DEPENDENCY]
    # [Dependency interna que valida se o usuário autenticado tem role permitida]
    # [ENTRADA: user - usuário autenticado via require_auth]
    # [SAIDA: User - usuário validado com role permitida]
    # [DEPENDENCIAS: HTTPException, status]
    def dependency(user: User = Depends(require_auth)) -> User:
        user_role = user.role.name if user.role else None
        
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join(allowed_roles)}"
            )
        
        return user
    
    return dependency