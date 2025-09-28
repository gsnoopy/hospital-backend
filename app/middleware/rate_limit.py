from fastapi import Request, status
from fastapi.responses import JSONResponse

from ..security import rate_limiter
from ..schemas.rate_limit import RATE_LIMITS


# [RATE LIMIT MIDDLEWARE]
# [Middleware que aplica rate limiting por usuário/IP usando Redis, com configurações por endpoint]
# [ENTRADA: request - requisição HTTP, call_next - próximo middleware/handler]
# [SAIDA: JSONResponse com erro 429 se rate limited, ou resposta normal com headers de rate limit]
# [DEPENDENCIAS: rate_limiter, RATE_LIMITS, JSONResponse]
async def rate_limit_middleware(request: Request, call_next):
    
    skip_paths = ["/docs", "/openapi.json", "/redoc", "/favicon.ico"]
    if request.url.path in skip_paths:
        return await call_next(request)
    
    user_id = getattr(request.state, "user_id", None)
    if user_id is None:
        client_ip = request.client.host
        user_id = f"ip_{client_ip}"
    
    path = request.url.path
    method = request.method
    
    endpoint_key = f"{method} {path}"
    rate_config = RATE_LIMITS.get(endpoint_key) or RATE_LIMITS.get(path) or RATE_LIMITS["default"]
    
    limit = rate_config["limit"]
    period = rate_config["period"]
    
    try:

        is_limited = await rate_limiter.is_rate_limited(user_id, path, limit, period)
        
        if is_limited:

            rate_info = await rate_limiter.get_rate_limit_info(user_id, path, period)
            
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": "Rate limit exceeded",
                    "retry_after": rate_info["reset_time"]
                },
                headers={
                    "X-RateLimit-Limit": str(limit),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(rate_info["reset_time"]),
                    "Retry-After": str(rate_info["reset_time"])
                }
            )
        
        rate_info = await rate_limiter.get_rate_limit_info(user_id, path, period)
        remaining = max(0, limit - rate_info["current_requests"])
        
        response = await call_next(request)
        
        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Reset"] = str(rate_info["reset_time"])
        
        return response
        
    except Exception as e:
        return await call_next(request)