from typing import Dict, List, Any, Optional


# [VALIDATION EXCEPTION]
# [Exceção para erros de validação de dados de entrada com múltiplos campos]
# [ENTRADA: errors - dict com erros por campo, message - mensagem principal opcional]
# [SAIDA: exceção com estrutura de erros organizados por campo]
# [DEPENDENCIAS: Dict, List, str, Exception]
class ValidationException(Exception):

    def __init__(self, errors: Dict[str, List[str]], message: str = "Validation failed"):
        self.errors = errors
        self.message = message
        super().__init__(message)


# [BUSINESS RULE EXCEPTION]
# [Exceção para violações de regras de negócio específicas da aplicação]
# [ENTRADA: message - descrição do erro, code - código opcional, details - detalhes opcionais]
# [SAIDA: exceção com informações contextuais sobre a regra violada]
# [DEPENDENCIAS: str, Optional, Dict, Any, Exception]
class BusinessRuleException(Exception):

    def __init__(self, message: str, code: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(message)


# [RESOURCE NOT FOUND EXCEPTION]
# [Exceção para recursos não encontrados no banco de dados]
# [ENTRADA: resource_type - tipo do recurso, identifier - identificador buscado, message - mensagem opcional]
# [SAIDA: exceção com detalhes do recurso não encontrado]
# [DEPENDENCIAS: str, Any, Optional, Exception]
class ResourceNotFoundException(Exception):

    def __init__(self, resource_type: str, identifier: Any, message: Optional[str] = None):
        self.resource_type = resource_type
        self.identifier = identifier
        self.message = message or f"{resource_type} with ID {identifier} not found"
        super().__init__(self.message)


# [DUPLICATE RESOURCE EXCEPTION]
# [Exceção para recursos duplicados que violam constraints únicos]
# [ENTRADA: resource_type - tipo do recurso, field - campo duplicado, value - valor duplicado, message - mensagem opcional]
# [SAIDA: exceção com detalhes da duplicação]
# [DEPENDENCIAS: str, Any, Optional, Exception]
class DuplicateResourceException(Exception):

    def __init__(self, resource_type: str, field: str, value: Any, message: Optional[str] = None):
        self.resource_type = resource_type
        self.field = field
        self.value = value
        self.message = message or f"{resource_type} with {field} '{value}' already exists"
        super().__init__(self.message)


# [AUTHENTICATION EXCEPTION]
# [Exceção para falhas de autenticação - credenciais inválidas ou token expirado]
# [ENTRADA: message - mensagem do erro, code - código específico opcional]
# [SAIDA: exceção com informações sobre falha de autenticação]
# [DEPENDENCIAS: str, Optional, Exception]
class AuthenticationException(Exception):

    def __init__(self, message: str = "Authentication failed", code: Optional[str] = None):
        self.message = message
        self.code = code
        super().__init__(message)


# [AUTHORIZATION EXCEPTION]
# [Exceção para falhas de autorização - usuário sem permissões necessárias]
# [ENTRADA: message - mensagem do erro, required_permission - permissão necessária opcional]
# [SAIDA: exceção com informações sobre falta de permissão]
# [DEPENDENCIAS: str, Optional, Exception]
class AuthorizationException(Exception):

    def __init__(self, message: str = "Insufficient permissions", required_permission: Optional[str] = None):
        self.message = message
        self.required_permission = required_permission
        super().__init__(message)


# [DATABASE EXCEPTION]
# [Exceção para erros de banco de dados que devem ser expostos ao usuário]
# [ENTRADA: message - mensagem amigável, original_error - erro original opcional para logs]
# [SAIDA: exceção com contexto de erro de banco de dados]
# [DEPENDENCIAS: str, Optional, Exception]
class DatabaseException(Exception):

    def __init__(self, message: str = "Database operation failed", original_error: Optional[Exception] = None):
        self.message = message
        self.original_error = original_error
        super().__init__(message)