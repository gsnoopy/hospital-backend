import jwt
import bcrypt
from datetime import datetime, timedelta
from app.core.config import settings
from typing import Optional, Tuple

# [HASH PASSWORD]
# [Gera hash da senha usando bcrypt com salt aleatório para armazenamento seguro]
# [ENTRADA: password: str - senha em texto plano a ser hasheada]
# [SAIDA: str - hash da senha codificado em UTF-8]
# [DEPENDENCIAS: bcrypt]
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


# [VERIFY PASSWORD]
# [Verifica se a senha fornecida corresponde ao hash armazenado usando bcrypt]
# [ENTRADA: plain_password: str - senha em texto plano, hashed_password: str - hash armazenado]
# [SAIDA: bool - True se a senha confere, False caso contrário]
# [DEPENDENCIAS: bcrypt]
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


# [CREATE ACCESS TOKEN]
# [Cria um token JWT de acesso com expiração configurável ou padrão]
# [ENTRADA: data: dict - dados a serem codificados no token, expires_delta: Optional[timedelta] - tempo de expiração customizado]
# [SAIDA: str - token JWT codificado]
# [DEPENDENCIAS: jwt, datetime, settings]
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


# [VERIFY TOKEN]
# [Verifica e decodifica um token JWT validando assinatura e expiração]
# [ENTRADA: token: str - token JWT a ser verificado]
# [SAIDA: Optional[dict] - payload do token se válido, None se inválido ou expirado]
# [DEPENDENCIAS: jwt, settings]
def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


# [CREATE REFRESH TOKEN]
# [Cria um refresh token JWT com expiração mais longa]
# [ENTRADA: data: dict - dados a serem codificados no token]
# [SAIDA: str - refresh token JWT codificado]
# [DEPENDENCIAS: jwt, datetime, settings]
def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=30)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


# [CREATE TOKEN PAIR]
# [Cria par de tokens (access + refresh) para autenticação completa]
# [ENTRADA: data: dict - dados a serem codificados nos tokens]
# [SAIDA: Tuple[str, str] - (access_token, refresh_token)]
# [DEPENDENCIAS: create_access_token, create_refresh_token]
def create_token_pair(data: dict) -> Tuple[str, str]:
    access_token = create_access_token(data)
    refresh_token = create_refresh_token(data)
    return access_token, refresh_token


# [VERIFY REFRESH TOKEN]
# [Verifica se um refresh token é válido e é do tipo correto]
# [ENTRADA: token: str - refresh token a ser verificado]
# [SAIDA: Optional[dict] - payload do token se válido, None se inválido]
# [DEPENDENCIAS: verify_token]
def verify_refresh_token(token: str) -> Optional[dict]:
    payload = verify_token(token)
    if payload and payload.get("type") == "refresh":
        return payload
    return None