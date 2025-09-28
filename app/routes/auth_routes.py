from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import LoginRequest, Token, TokenWithRefresh, RefreshTokenRequest, TokenVerifyResponse
from app.decorators import require_auth
from app.models.user import User

# [AUTH ROUTER]
# [Router FastAPI para endpoints de autenticação com prefixo /auth]
# [ENTRADA: configurações de rota - prefix e tags]
# [SAIDA: APIRouter configurado para autenticação]
# [DEPENDENCIAS: APIRouter]
router = APIRouter(prefix="/auth", tags=["authentication"])


# [LOGIN USER]
# [Endpoint POST para autenticação de usuário com email e senha]
# [ENTRADA: login_data - credenciais via LoginRequest, db - sessão do banco]
# [SAIDA: TokenWithRefresh - tokens de acesso e refresh JWT]
# [DEPENDENCIAS: AuthService]
@router.post("/", response_model=TokenWithRefresh)
def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    tokens = auth_service.authenticate_user_with_refresh(login_data.email, login_data.password)
    
    if not tokens:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token, refresh_token = tokens
    return {
        "access_token": access_token, 
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# [VERIFY TOKEN]
# [Endpoint GET para verificar se token está válido e obter informações]
# [ENTRADA: request - requisição HTTP, db - sessão do banco]
# [SAIDA: TokenVerifyResponse - informações do token e usuário]
# [DEPENDENCIAS: AuthService]
@router.get("/verify", response_model=TokenVerifyResponse)
def verify_token(request: Request, db: Session = Depends(get_db)):

    authorization = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header"
        )
    
    token = authorization.split(" ")[1]
    
    auth_service = AuthService(db)
    token_info = auth_service.get_token_info(token)
    
    if not token_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    return TokenVerifyResponse(**token_info)


# [REFRESH TOKEN]
# [Endpoint POST para renovar access token usando refresh token]
# [ENTRADA: refresh_data - refresh token via RefreshTokenRequest, db - sessão do banco]
# [SAIDA: Token - novo token de acesso JWT]
# [DEPENDENCIAS: AuthService]
@router.post("/refresh", response_model=Token)
def refresh_token(refresh_data: RefreshTokenRequest, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    new_access_token = auth_service.refresh_access_token(refresh_data.refresh_token)
    
    if not new_access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    return {"access_token": new_access_token, "token_type": "bearer"}