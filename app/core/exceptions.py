"""
Exceções customizadas para padronização do tratamento de erros na aplicação.
Define exceções específicas para diferentes tipos de erros de negócio e validação.
"""

from typing import Dict, List, Any, Optional


class ValidationException(Exception):
    """
    Exceção para erros de validação de dados de entrada.

    Args:
        errors: Dicionário com erros organizados por campo
        message: Mensagem principal do erro (opcional)
    """

    def __init__(self, errors: Dict[str, List[str]], message: str = "Validation failed"):
        self.errors = errors
        self.message = message
        super().__init__(message)


class BusinessRuleException(Exception):
    """
    Exceção para violações de regras de negócio.

    Args:
        message: Mensagem descritiva do erro
        code: Código do erro para identificação (opcional)
        details: Detalhes adicionais sobre o erro (opcional)
    """

    def __init__(self, message: str, code: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(message)


class ResourceNotFoundException(Exception):
    """
    Exceção para recursos não encontrados.

    Args:
        resource_type: Tipo do recurso (ex: "User", "Hospital")
        identifier: Identificador usado na busca
        message: Mensagem customizada (opcional)
    """

    def __init__(self, resource_type: str, identifier: Any, message: Optional[str] = None):
        self.resource_type = resource_type
        self.identifier = identifier
        self.message = message or f"{resource_type} not found with identifier: {identifier}"
        super().__init__(self.message)


class DuplicateResourceException(Exception):
    """
    Exceção para recursos duplicados.

    Args:
        resource_type: Tipo do recurso (ex: "User", "Hospital")
        field: Campo que causou a duplicação
        value: Valor duplicado
        message: Mensagem customizada (opcional)
    """

    def __init__(self, resource_type: str, field: str, value: Any, message: Optional[str] = None):
        self.resource_type = resource_type
        self.field = field
        self.value = value
        self.message = message or f"{resource_type} with {field} '{value}' already exists"
        super().__init__(self.message)


class AuthenticationException(Exception):
    """
    Exceção para falhas de autenticação.

    Args:
        message: Mensagem do erro de autenticação
        code: Código específico do erro (opcional)
    """

    def __init__(self, message: str = "Authentication failed", code: Optional[str] = None):
        self.message = message
        self.code = code
        super().__init__(message)


class AuthorizationException(Exception):
    """
    Exceção para falhas de autorização.

    Args:
        message: Mensagem do erro de autorização
        required_permission: Permissão necessária (opcional)
    """

    def __init__(self, message: str = "Insufficient permissions", required_permission: Optional[str] = None):
        self.message = message
        self.required_permission = required_permission
        super().__init__(message)


class DatabaseException(Exception):
    """
    Exceção para erros de banco de dados que devem ser expostos ao usuário.

    Args:
        message: Mensagem amigável ao usuário
        original_error: Erro original do banco (opcional, para logs)
    """

    def __init__(self, message: str = "Database operation failed", original_error: Optional[Exception] = None):
        self.message = message
        self.original_error = original_error
        super().__init__(message)