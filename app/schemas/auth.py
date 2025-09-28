from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# [LOGIN REQUEST]
# [Schema Pydantic para validar dados de requisição de login]
# [ENTRADA: email - email do usuário, password - senha em texto plano]
# [SAIDA: instância LoginRequest validada]
# [DEPENDENCIAS: BaseModel]
class LoginRequest(BaseModel):
    email: str
    password: str


# [TOKEN]
# [Schema Pydantic para resposta de autenticação com token JWT]
# [ENTRADA: access_token - token JWT, token_type - tipo do token (bearer)]
# [SAIDA: instância Token para resposta da API]
# [DEPENDENCIAS: BaseModel]
class Token(BaseModel):
    access_token: str
    token_type: str


# [TOKEN WITH REFRESH]
# [Schema Pydantic para resposta de autenticação com token JWT e refresh token]
# [ENTRADA: access_token - token JWT, refresh_token - token para renovação, token_type - tipo do token (bearer)]
# [SAIDA: instância TokenWithRefresh para resposta da API]
# [DEPENDENCIAS: BaseModel]
class TokenWithRefresh(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


# [REFRESH TOKEN REQUEST]
# [Schema Pydantic para validar dados de requisição de refresh token]
# [ENTRADA: refresh_token - token de refresh para renovação]
# [SAIDA: instância RefreshTokenRequest validada]
# [DEPENDENCIAS: BaseModel]
class RefreshTokenRequest(BaseModel):
    refresh_token: str


# [TOKEN VERIFY RESPONSE]
# [Schema Pydantic para resposta de verificação de token]
# [ENTRADA: valid - se o token é válido, expires_at - quando expira, user_email - email do usuário]
# [SAIDA: instância TokenVerifyResponse para resposta da API]
# [DEPENDENCIAS: BaseModel, datetime, Optional]
class TokenVerifyResponse(BaseModel):
    valid: bool
    expires_at: Optional[datetime] = None
    user_email: Optional[str] = None
    user_id: Optional[int] = None