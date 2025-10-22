from fastapi import Depends, HTTPException, status
from typing import List, Union, Callable
from app.decorators.auth import require_auth
from app.models.user import User
from app.core.hospital_context import HospitalContext


# [REQUIRE DEVELOPER]
# [Decorator simplificado para rotas exclusivas de Desenvolvedor]
# [ENTRADA: nenhuma]
# [SAIDA: Callable - função que retorna HospitalContext]
# [DEPENDENCIAS: require_auth, User, HTTPException, HospitalContext]
# [USO: Use em rotas que só Desenvolvedor pode acessar (ex: criar roles, seed, etc)]
def require_developer() -> Callable:
    
    def dependency(current_user: User = Depends(require_auth)) -> HospitalContext:
        user_role = current_user.role.name if current_user.role else None

        if user_role != "Desenvolvedor":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Only Desenvolvedor can access this resource."
            )

        return HospitalContext(current_user)

    return dependency


# [REQUIRE ROLE]
# [Decorator factory que valida role e retorna HospitalContext com filtros automáticos]
# [ENTRADA: allowed_roles - string ou lista de roles permitidas]
# [SAIDA: Callable - função que retorna HospitalContext com lógica de hospital]
# [DEPENDENCIAS: require_auth, User, HTTPException, HospitalContext]
# [USO: Use em TODAS as rotas que precisam validar role - sempre retorna context com hospital]
def require_role(allowed_roles: Union[str, List[str]]) -> Callable:

    if isinstance(allowed_roles, str):
        allowed_roles = [allowed_roles]

    def dependency(current_user: User = Depends(require_auth)) -> HospitalContext:
        user_role = current_user.role.name if current_user.role else None

        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join(allowed_roles)}"
            )

        if user_role != "Desenvolvedor" and not current_user.hospital_id:
            raise HTTPException(
                status_code=403,
                detail="User is not associated with any hospital"
            )

        return HospitalContext(current_user)

    return dependency
