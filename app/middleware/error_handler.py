from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
import logging

# [ERROR HANDLER LOGGER]
# [Cria logger específico para o middleware de tratamento de erros]
# [ENTRADA: __name__ - nome do módulo atual]
# [SAIDA: Logger - instância do logger configurada]
# [DEPENDENCIAS: logging.getLogger]
logger = logging.getLogger(__name__)

# [ERROR HANDLER MIDDLEWARE]
# [Middleware global que captura e trata todas as exceções da aplicação, retornando responses JSON padronizados]
# [ENTRADA: request - requisição HTTP, call_next - próximo middleware/handler na cadeia]
# [SAIDA: JSONResponse - resposta JSON com erro tratado ou resposta normal se sem erro]
# [DEPENDENCIAS: JSONResponse, logger, HTTPException, SQLAlchemyError, ValueError, Exception]
async def error_handler_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except HTTPException as e:
        logger.warning(f"HTTP Exception: {e.status_code} - {e.detail}")

        # Handle structured validation errors
        if isinstance(e.detail, dict):
            return JSONResponse(
                status_code=e.status_code,
                content=e.detail
            )

        # Handle regular HTTPException
        return JSONResponse(
            status_code=e.status_code,
            content={
                "error": True,
                "message": e.detail,
                "status_code": e.status_code
            }
        )
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "error": True,
                "message": "Database error occurred",
                "status_code": 500
            }
        )
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return JSONResponse(
            status_code=422,
            content={
                "error": True,
                "message": f"Validation error: {str(e)}",
                "status_code": 422
            }
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "error": True,
                "message": "Internal server error",
                "status_code": 500
            }
        )