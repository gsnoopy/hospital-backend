from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.auth.auth import verify_password, create_access_token, create_token_pair, verify_token, verify_refresh_token
from datetime import datetime
from typing import Optional, Tuple


# [AUTH SERVICE]
# [Serviço para autenticação de usuários com validação de senha e geração de tokens]
# [ENTRADA: db - sessão do banco SQLAlchemy]
# [SAIDA: instância AuthService configurada]
# [DEPENDENCIAS: UserRepository]
class AuthService:
    
    # [INIT]
    # [Construtor que inicializa o serviço com repository de usuário]
    # [ENTRADA: db - sessão do banco SQLAlchemy]
    # [SAIDA: instância inicializada]
    # [DEPENDENCIAS: UserRepository]
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    # [AUTHENTICATE USER]
    # [Autentica usuário verificando email e senha, gera token JWT se válido e registra métricas]
    # [ENTRADA: email - email do usuário, password - senha em texto plano]
    # [SAIDA: Optional[str] - token JWT se autenticação bem-sucedida, None caso contrário]
    # [DEPENDENCIAS: self.user_repository, verify_password, create_access_token]
    def authenticate_user(self, email: str, password: str) -> Optional[str]:
        user = self.user_repository.get_by_email(email)
        success = user and verify_password(password, user.password)
        
        
        if not success:
            return None
        
        access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
        return access_token

    # [AUTHENTICATE USER WITH REFRESH]
    # [Autentica usuário e retorna par de tokens (access + refresh)]
    # [ENTRADA: email - email do usuário, password - senha em texto plano]
    # [SAIDA: Optional[Tuple[str, str]] - (access_token, refresh_token) se válido, None caso contrário]
    # [DEPENDENCIAS: self.user_repository, verify_password, create_token_pair]
    def authenticate_user_with_refresh(self, email: str, password: str) -> Optional[Tuple[str, str]]:
        user = self.user_repository.get_by_email(email)
        success = user and verify_password(password, user.password)
        
        if not success:
            return None
        
        access_token, refresh_token = create_token_pair(data={"sub": user.email, "user_id": user.id})
        return access_token, refresh_token

    # [VERIFY TOKEN]
    # [Verifica se um token é válido e retorna informações do usuário]
    # [ENTRADA: token - token JWT a ser verificado]
    # [SAIDA: Optional[dict] - dados do token se válido, None caso contrário]
    # [DEPENDENCIAS: verify_token]
    def verify_user_token(self, token: str) -> Optional[dict]:
        payload = verify_token(token)
        if not payload:
            return None
            
        # Verificar se usuário ainda existe
        user_email = payload.get("sub")
        if not user_email:
            return None
            
        user = self.user_repository.get_by_email(user_email)
        if not user:
            return None
            
        return {
            "valid": True,
            "expires_at": datetime.fromtimestamp(payload["exp"]),
            "user_email": user_email,
            "user_id": payload.get("user_id")
        }

    # [REFRESH TOKEN]
    # [Renova access token usando refresh token válido]
    # [ENTRADA: refresh_token - refresh token para renovação]
    # [SAIDA: Optional[str] - novo access token se válido, None caso contrário]
    # [DEPENDENCIAS: verify_refresh_token, create_access_token]
    def refresh_access_token(self, refresh_token: str) -> Optional[str]:
        payload = verify_refresh_token(refresh_token)
        if not payload:
            return None
            
        user_email = payload.get("sub")
        if not user_email:
            return None
            
        user = self.user_repository.get_by_email(user_email)
        if not user:
            return None
            
        new_access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
        return new_access_token

    # [GET TOKEN INFO]
    # [Obtém informações detalhadas de um token incluindo data de expiração]
    # [ENTRADA: token - token JWT para extrair informações]
    # [SAIDA: Optional[dict] - informações do token incluindo expires_at, None se inválido]
    # [DEPENDENCIAS: verify_token, datetime]
    def get_token_info(self, token: str) -> Optional[dict]:
        payload = verify_token(token)
        if not payload:
            return None
            
        user_email = payload.get("sub")
        if not user_email:
            return None
            
        user = self.user_repository.get_by_email(user_email)
        if not user:
            return None
            
        expires_at = None
        if "exp" in payload:
            expires_at = datetime.fromtimestamp(payload["exp"])
            
        return {
            "valid": True,
            "expires_at": expires_at,
            "user_email": user_email,
            "user_id": payload.get("user_id")
        }