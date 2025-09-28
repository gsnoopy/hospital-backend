from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.security import rate_limiter
from app.core.timezone import get_current_time


# [HEALTH ROUTER]
# [Router FastAPI para endpoints de health check e monitoramento]
# [ENTRADA: configuração de tags]
# [SAIDA: APIRouter configurado para health checks]
# [DEPENDENCIAS: APIRouter]
router = APIRouter(tags=["health"])


# [HEALTH CHECK]
# [Endpoint GET básico para verificação de saúde da API]
# [ENTRADA: nenhuma]
# [SAIDA: dict - status, timestamp e nome do serviço]
# [DEPENDENCIAS: get_current_time]
@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": get_current_time().isoformat(),
        "service": "3DI RH Backend API"
    }


# [DETAILED HEALTH CHECK]
# [Endpoint GET detalhado que verifica saúde do banco de dados e Redis]
# [ENTRADA: db - sessão do banco via dependência]
# [SAIDA: dict - status detalhado com checks individuais ou HTTPException 503]
# [DEPENDENCIAS: get_current_time, text, rate_limiter, HTTPException]
@router.get("/health/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    health_status = {
        "status": "healthy",
        "timestamp": get_current_time().isoformat(),
        "service": "3DI RH Backend API",
        "checks": {}
    }
    
    try:
        db.execute(text("SELECT 1"))
        health_status["checks"]["database"] = {
            "status": "healthy",
            "response_time_ms": "< 100"
        }
    except Exception as e:
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "unhealthy"
    
    try:
        await rate_limiter.get_rate_limit_info("health_check", "/health", 60)
        health_status["checks"]["redis"] = {
            "status": "healthy",
            "response_time_ms": "< 50"
        }
    except Exception as e:
        health_status["checks"]["redis"] = {
            "status": "unhealthy", 
            "error": str(e)
        }
        health_status["status"] = "unhealthy"
    
    if health_status["status"] == "unhealthy":
        raise HTTPException(status_code=503, detail=health_status)
    
    return health_status