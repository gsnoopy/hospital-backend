from fastapi import Depends, HTTPException
from app.decorators.auth import require_auth
from app.models.user import User


# [REQUIRE HOSPITAL]
# [Dependency que retorna o hospital_id do usuário autenticado]
# [ENTRADA: current_user - usuário autenticado via require_auth]
# [SAIDA: int - ID interno do hospital do usuário]
# [DEPENDENCIAS: require_auth, User]
def require_hospital(
    current_user: User = Depends(require_auth)
) -> int:
    
    if not current_user.hospital_id:
        raise HTTPException(
            status_code=403,
            detail="User is not associated with any hospital"
        )

    return current_user.hospital_id
