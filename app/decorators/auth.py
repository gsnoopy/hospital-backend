from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth import verify_token
from app.services.user_service import UserService
from app.models.user import User
from fastapi import HTTPException

# [HTTP BEARER SECURITY]
# [Define esquema de segurança HTTPBearer para autenticação via token]
# [ENTRADA: nenhuma]
# [SAIDA: HTTPBearer - esquema de segurança para FastAPI]
# [DEPENDENCIAS: HTTPBearer]
security = HTTPBearer()

# [REQUIRE AUTH]
# [Dependency que exige autenticação via token Bearer e retorna o usuário atual validado]
# [ENTRADA: credentials - token Bearer do header, db - sessão do banco]
# [SAIDA: User - usuário autenticado e ativo]
# [DEPENDENCIAS: verify_token, UserService, InvalidCredentialsException]
def require_auth(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:

    payload = verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    email: str = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    user_service = UserService(db)
    user = user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")    
    
    return user