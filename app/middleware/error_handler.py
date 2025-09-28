from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.core.exceptions import (
    ValidationException,
    BusinessRuleException,
    ResourceNotFoundException,
    DuplicateResourceException,
    AuthenticationException,
    AuthorizationException,
    DatabaseException
)

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

    # Custom exceptions - handled first for better control
    except ValidationException as e:
        logger.warning(f"Validation error: {e.message}")
        return JSONResponse(
            status_code=422,
            content={
                "error": True,
                "message": e.message,
                "validation_errors": e.errors,
                "status_code": 422
            }
        )

    except ResourceNotFoundException as e:
        logger.warning(f"Resource not found: {e.message}")
        return JSONResponse(
            status_code=404,
            content={
                "error": True,
                "message": e.message,
                "resource_type": e.resource_type,
                "identifier": str(e.identifier),
                "status_code": 404
            }
        )

    except DuplicateResourceException as e:
        logger.warning(f"Duplicate resource: {e.message}")
        return JSONResponse(
            status_code=409,
            content={
                "error": True,
                "message": e.message,
                "resource_type": e.resource_type,
                "field": e.field,
                "value": str(e.value),
                "status_code": 409
            }
        )

    except AuthenticationException as e:
        logger.warning(f"Authentication failed: {e.message}")
        return JSONResponse(
            status_code=401,
            content={
                "error": True,
                "message": e.message,
                "code": e.code,
                "status_code": 401
            }
        )

    except AuthorizationException as e:
        logger.warning(f"Authorization failed: {e.message}")
        return JSONResponse(
            status_code=403,
            content={
                "error": True,
                "message": e.message,
                "required_permission": e.required_permission,
                "status_code": 403
            }
        )

    except BusinessRuleException as e:
        logger.warning(f"Business rule violation: {e.message}")
        return JSONResponse(
            status_code=400,
            content={
                "error": True,
                "message": e.message,
                "code": e.code,
                "details": e.details,
                "status_code": 400
            }
        )

    except DatabaseException as e:
        logger.error(f"Database exception: {e.message}")
        if e.original_error:
            logger.error(f"Original error: {str(e.original_error)}")
        return JSONResponse(
            status_code=500,
            content={
                "error": True,
                "message": e.message,
                "status_code": 500
            }
        )

    # FastAPI HTTPException - for backward compatibility
    except HTTPException as e:
        logger.warning(f"HTTP Exception: {e.status_code} - {e.detail}")

        # Handle structured validation errors (legacy support)
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

    # Database errors - SQLAlchemy
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "error": True,
                "message": "A database error occurred. Please try again later.",
                "status_code": 500
            }
        )

    # Generic validation errors
    except ValueError as e:
        logger.error(f"Value error: {str(e)}")
        return JSONResponse(
            status_code=422,
            content={
                "error": True,
                "message": f"Invalid value: {str(e)}",
                "status_code": 422
            }
        )

    # Catch-all for unexpected errors
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": True,
                "message": "An unexpected error occurred. Please try again later.",
                "status_code": 500
            }
        )