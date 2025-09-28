from abc import ABC, abstractmethod
from typing import Any, Dict, List


# [VALIDATION ERROR]
# [Exceção customizada para erros de validação com mensagem e campo opcional]
# [ENTRADA: message - mensagem do erro, field - campo onde ocorreu o erro]
# [SAIDA: instância ValidationError]
# [DEPENDENCIAS: Exception]
class ValidationError(Exception):
    
    # [INIT]
    # [Construtor que inicializa o erro com mensagem e campo]
    # [ENTRADA: message - mensagem do erro, field - campo opcional]
    # [SAIDA: instância inicializada]
    # [DEPENDENCIAS: super]
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(self.message)


# [VALIDATION RESULT]
# [Classe para armazenar resultado de validação com lista de erros e status]
# [ENTRADA: nenhuma no construtor]
# [SAIDA: instância ValidationResult para acumular erros]
# [DEPENDENCIAS: List, ValidationError]
class ValidationResult:
    
    # [INIT]
    # [Construtor que inicializa resultado com lista vazia de erros e status válido]
    # [ENTRADA: nenhuma]
    # [SAIDA: instância inicializada]
    # [DEPENDENCIAS: List, ValidationError]
    def __init__(self):
        self.errors: List[ValidationError] = []
        self.is_valid: bool = True

    # [ADD ERROR]
    # [Adiciona um erro à lista e marca resultado como inválido]
    # [ENTRADA: message - mensagem do erro, field - campo opcional]
    # [SAIDA: None - modifica estado interno]
    # [DEPENDENCIAS: ValidationError]
    def add_error(self, message: str, field: str = None):
        self.errors.append(ValidationError(message, field))
        self.is_valid = False

    # [GET ERROR MESSAGES]
    # [Retorna lista com todas as mensagens de erro]
    # [ENTRADA: nenhuma]
    # [SAIDA: List[str] - lista de mensagens]
    # [DEPENDENCIAS: self.errors]
    def get_error_messages(self) -> List[str]:
        return [error.message for error in self.errors]

    # [GET ERRORS BY FIELD]
    # [Retorna dict com erros agrupados por campo - erros sem campo ficam em 'general']
    # [ENTRADA: nenhuma]
    # [SAIDA: Dict[str, List[str]] - erros organizados por campo]
    # [DEPENDENCIAS: self.errors]
    def get_errors_by_field(self) -> Dict[str, List[str]]:
        errors_by_field = {}
        for error in self.errors:
            field = error.field or "general"
            if field not in errors_by_field:
                errors_by_field[field] = []
            errors_by_field[field].append(error.message)
        return errors_by_field


# [BASE VALIDATOR]
# [Classe abstrata base para implementação de validadores customizados]
# [ENTRADA: data - dados a serem validados (tipo genérico)]
# [SAIDA: ValidationResult - resultado da validação]
# [DEPENDENCIAS: ABC, abstractmethod, ValidationResult]
class BaseValidator(ABC):
    
    # [VALIDATE]
    # [Método abstrato que deve ser implementado pelas classes filhas para validar dados]
    # [ENTRADA: data - dados a serem validados]
    # [SAIDA: ValidationResult - resultado da validação]
    # [DEPENDENCIAS: ValidationResult]
    @abstractmethod
    def validate(self, data: Any) -> ValidationResult:
        pass