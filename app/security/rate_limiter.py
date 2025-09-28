from datetime import UTC, datetime
from typing import Optional
import logging

from redis.asyncio import ConnectionPool, Redis

from ..schemas.rate_limit import sanitize_path

# [RATE LIMITER LOGGER]
# [Cria logger específico para o rate limiter]
# [ENTRADA: __name__ - nome do módulo atual]
# [SAIDA: Logger - instância do logger configurada]
# [DEPENDENCIAS: logging.getLogger]
logger = logging.getLogger(__name__)


# [RATE LIMITER]
# [Classe singleton para gerenciar rate limiting usando Redis - implementa sliding window]
# [ENTRADA: configuração via initialize() - redis_url]
# [SAIDA: instância singleton RateLimiter]
# [DEPENDENCIAS: Redis, ConnectionPool, sanitize_path, logger]
class RateLimiter:
    _instance: Optional["RateLimiter"] = None
    pool: Optional[ConnectionPool] = None
    client: Optional[Redis] = None

    # [NEW]
    # [Método especial que implementa padrão singleton - garante uma única instância]
    # [ENTRADA: cls - classe RateLimiter]
    # [SAIDA: RateLimiter - única instância da classe]
    # [DEPENDENCIAS: nenhuma]
    def __new__(cls) -> "RateLimiter":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # [INITIALIZE]
    # [Método de classe para inicializar conexão Redis com pool de conexões]
    # [ENTRADA: redis_url - URL de conexão com Redis]
    # [SAIDA: None - configura pool e client na instância]
    # [DEPENDENCIAS: ConnectionPool, Redis]
    @classmethod
    def initialize(cls, redis_url: str) -> None:
        instance = cls()
        if instance.pool is None:
            instance.pool = ConnectionPool.from_url(redis_url)
            instance.client = Redis(connection_pool=instance.pool)

    # [GET CLIENT]
    # [Método de classe para obter cliente Redis inicializado]
    # [ENTRADA: nenhuma]
    # [SAIDA: Redis - cliente Redis configurado ou Exception se não inicializado]
    # [DEPENDENCIAS: logger]
    @classmethod
    def get_client(cls) -> Redis:
        instance = cls()
        if instance.client is None:
            logger.error("Redis client is not initialized.")
            raise Exception("Redis client is not initialized.")
        return instance.client

    # [IS RATE LIMITED]
    # [Verifica se usuário excedeu limite de requests usando sliding window com Redis]
    # [ENTRADA: user_id - ID do usuário, path - endpoint, limit - limite de requests, period - período em segundos]
    # [SAIDA: bool - True se rate limited, False caso contrário]
    # [DEPENDENCIAS: get_client, sanitize_path, datetime, logger]
    async def is_rate_limited(self, user_id: int, path: str, limit: int, period: int) -> bool:
        client = self.get_client()
        current_timestamp = int(datetime.now(UTC).timestamp())
        window_start = current_timestamp - (current_timestamp % period)

        sanitized_path = sanitize_path(path)
        key = f"ratelimit:{user_id}:{sanitized_path}:{window_start}"

        try:
            current_count = await client.incr(key)
            if current_count == 1:
                await client.expire(key, period)

            if current_count > limit:
                return True

        except Exception as e:
            logger.exception(f"Error checking rate limit for user {user_id} on path {path}: {e}")
            raise e

        return False

    # [GET RATE LIMIT INFO]
    # [Obtém informações atuais do rate limit para usuário - requests atuais e tempo de reset]
    # [ENTRADA: user_id - ID do usuário, path - endpoint, period - período em segundos]
    # [SAIDA: dict - current_requests e reset_time]
    # [DEPENDENCIAS: get_client, sanitize_path, datetime, logger]
    async def get_rate_limit_info(self, user_id: int, path: str, period: int) -> dict:
        client = self.get_client()
        current_timestamp = int(datetime.now(UTC).timestamp())
        window_start = current_timestamp - (current_timestamp % period)
        
        sanitized_path = sanitize_path(path)
        key = f"ratelimit:{user_id}:{sanitized_path}:{window_start}"
        
        try:
            current_count = await client.get(key)
            ttl = await client.ttl(key)
            
            return {
                "current_requests": int(current_count) if current_count else 0,
                "reset_time": current_timestamp + ttl if ttl > 0 else window_start + period
            }
        except Exception as e:
            logger.exception(f"Error getting rate limit info for user {user_id} on path {path}: {e}")
            return {"current_requests": 0, "reset_time": window_start + period}


# [RATE LIMITER INSTANCE]
# [Instância global singleton do rate limiter para uso na aplicação]
# [ENTRADA: nenhuma - usa singleton]
# [SAIDA: RateLimiter - instância global]
# [DEPENDENCIAS: RateLimiter]
rate_limiter = RateLimiter()